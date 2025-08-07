from collections import defaultdict
from django.shortcuts import render,redirect, get_object_or_404
from .models import Student,Fees,Attendance
from datetime import date, timedelta, datetime
from django.db.models import Q,F,Sum,Count
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import tempfile,random
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    step = request.session.get("step", "form")
    print(step, 'step')

    if request.method == "POST":
        if step == "form":
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect("register")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect("register")

            otp = generate_otp()
            email_send = EmailMessage(
                subject='Verify Your Email with This OTP Code',
                body=f"""
            Hi {username},

            Your One-Time Password (OTP) for verifying your email address is:

            {otp}

            This code is valid for 10 minutes. Please do not share it with anyone.

            If you did not request this code, please ignore this email or contact our support team.

            Best regards,  
            TCIT
            """,
                from_email='admin@yourdomain.com',
                to=[email],
            )
            email_send.send()

            request.session["reg_data"] = {
                "username": username,
                "email": email,
                "password": password,
                "otp": otp,
            }
            request.session["step"] = "otp"
            messages.info(request, "OTP sent to your email.")
            return redirect("register")

        elif step == "otp":
            entered_otp = request.POST.get("otp")
            reg_data = request.session.get("reg_data")

            if reg_data and entered_otp == reg_data["otp"]:
                user = User.objects.create_user(
                    username=reg_data["username"],
                    email=reg_data["email"],
                    password=reg_data["password"],
                )
                user.save()
                messages.success(request, "Account created successfully! Please log in.")
                request.session.flush()  # Clear session
                return redirect("index")
            else:
                messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "register.html", {"step": request.session.get("step", "form")})

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             messages.error(request, "Invalid username or password!")
#             return redirect(login_view)

#     return render(request, "login.html")

def login_view(request):
    if request.method == "POST":
        # Step 2: OTP verification
        if 'otp' in request.POST:
            print("hyy")
            entered_otp = request.POST.get('otp')
            session_otp = request.session.get('otp')
            pending_user_id = request.session.get('pending_user_id')

            if entered_otp and str(session_otp) == entered_otp:
                # Get user
                user = get_user_model().objects.get(id=pending_user_id)

                # Specify backend (pick your default one)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                # Clear session
                request.session.pop('otp', None)
                request.session.pop('pending_user_id', None)

                return redirect('index')
            else:
                messages.error(request, "Invalid OTP! Please try again.")
                return render(request, "login.html", {"otp_stage": True})


        # Step 1: Username & password authentication
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Generate OTP
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['pending_user_id'] = user.id

                # Send OTP email
                email_subject = 'Verify Your Email with This OTP Code'
                email_body = f"""
                    <html>
                      <body>
                        <p>Hi {username},</p>

                        <p>Your One-Time Password (OTP) for verifying your email address is:</p>

                        <p style="font-size:15px;">
                            <strong>{otp}</strong>
                        </p>

                        <p>
                          This code is valid for 10 minutes. Please do not share it with anyone.
                        </p>

                        <p>
                          If you did not request this code, please ignore this email or contact our support team.
                        </p>

                        <p>Best regards,<br>TCIT</p>
                      </body>
                    </html>
                    """

                email_send = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email='admin@yourdomain.com',
                    to=[user.email],
                )
                email_send.content_subtype = "html"  # ✅ This makes the email HTML
                email_send.send()

                messages.info(request, "OTP sent to your email. Please verify.")
                return render(request, "login.html", {"otp_stage": True})

            else:
                messages.error(request, "Invalid username or password!")
                return redirect('login_view')

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required(login_url='login_view')
def index(request):
    student_count = Student.objects.count()
    students = Student.objects.all().order_by('created_at')  
    today = date.today()
    
    stu = Student.objects.filter(
    birthday__month=today.month,
    birthday__day=today.day
    )
 
    male_count = Student.objects.filter(gender__iexact='Male').count()
    female_count = Student.objects.filter(gender="Female").count()

    current_year = date.today().year

    monthly_data = defaultdict(int)
    for student in students:
        if student.created_at and student.created_at.year == current_year:
            key = student.created_at.strftime("%b %Y")  # e.g., "Jul 2025"
            monthly_data[key] += 1
    
    labels = list(monthly_data.keys())
    counts = list(monthly_data.values()) 
    
    current_year = date.today().year
    start_year = current_year - 2
    end_year = current_year
    years = Student.objects.filter(created_at__year__range=(start_year, end_year))
    yearly_data = defaultdict(int)
    for student in years:
        if student.created_at:
            year = student.created_at.year
            yearly_data[year] += 1
            
    year_labels = sorted(yearly_data.keys())
    year_counts = [yearly_data[year] for year in year_labels]
    
    

    return render(request, 'index.html', {
        'labels': labels,
        'counts': counts,
        'student_count':student_count,
        'male_count':male_count,
        'female_count':female_count,
        'stu':stu,
        'year_labels':year_labels,
        'year_counts':year_counts,
    })

@login_required(login_url='login_view')
def addstudent(request):
    if request.method == 'POST':
        s=Student()
        s.users = request.user
        s.firstname=request.POST.get('firstname')
        s.middlename=request.POST.get('middlename')
        s.lastname=request.POST.get('lastname')
        s.gender=request.POST.get('gender')
        s.email=request.POST.get('email')
        s.phone=request.POST.get('phone')
        s.house_society_name=request.POST.get('society')
        s.landmark_area=request.POST.get('area')
        s.city=request.POST.get('city')
        s.pin_code=request.POST.get('pin')
        s.birthday=request.POST.get('birthday')
        s.courses=request.POST.get('courses')
        s.amount=request.POST.get('amount')
        s.created_at=request.POST.get('admission')
        s.image=request.FILES.get('image')
        s.save()
        email = EmailMessage(
            subject='Welcome',
            body=f"Welcome to TCIT, {s.firstname} {s.lastname}!",
            from_email='admin@yourdomain.com',
            to=[s.email],
        )
        email.send()
        return redirect(studentlist)
    else:
        return render(request,'addstudent.html')
    
def editstudent(request,pk):
    s=get_object_or_404(Student,pk=pk)
    if request.method == 'POST':
        s.firstname=request.POST.get('fname')
        s.middlename=request.POST.get('mname')
        s.lastname=request.POST.get('lname')
        s.gender=request.POST.get('gender')
        s.email=request.POST.get('email')
        s.phone=request.POST.get('phone')
        s.house_society_name=request.POST.get('address')
        s.landmark_area=request.POST.get('address')
        s.city=request.POST.get('city')
        s.pin_code=request.POST.get('address')
        s.birthday=request.POST.get('coures')
        s.courses=request.POST.get('coures')
        s.amount=request.POST.get('amount')
        s.created_at=request.POST.get('admission_date')
        if request.FILES.get('image'):
            s.image = request.FILES.get('image')
        s.save()
        return redirect(studentlist)
    else:
        posts=Student.objects.all()
        return render(request,'editstudent.html',{'s':s,'posts':posts})

def deletestudent(request,pk):
    s=get_object_or_404(Student,pk=pk)
    s.delete()
    return redirect(studentlist)

@login_required(login_url='login_view')
def studentlist(request):
    student = Student.objects.all().order_by('firstname','lastname')
    return render(request,'studentlist.html',{'student':student})

@login_required(login_url='login_view')
def course_report(request):
    course_data = (
        Student.objects
        .values('courses')
        .annotate(total=Count('id'))
        .order_by('courses')
    )
    course_labels = [c['courses'] for c in course_data]
    course_counts = [c['total'] for c in course_data]
    
    return render(request, 'course_report.html',{
        'course_labels': course_labels,
        'course_counts': course_counts
    })

@login_required(login_url='login_view')
def report_view(request):
    labels = []
    counts = []
    course_labels = []
    course_counts = []

    if 'start_date' in request.GET and 'end_date' in request.GET:
        try:
            # Parse date range
            start_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d')

            # Filter students in range
            students = Student.objects.filter(created_at__range=(start_date, end_date)).order_by('created_at')

            # Monthly student count
            monthly_data = defaultdict(int)
            for student in students:
                month = student.created_at.strftime('%b %Y')
                monthly_data[month] += 1

            sorted_months = sorted(monthly_data.keys(), key=lambda x: datetime.strptime(x, "%b %Y"))
            labels = sorted_months
            counts = [monthly_data[m] for m in sorted_months]

            # Course-wise student count
            course_data = (
                students
                .values('courses')  # if your model field is `courses`
                .annotate(total=Count('id'))
                .order_by('courses')
            )

            course_labels = [item['courses'] for item in course_data]
            course_counts = [item['total'] for item in course_data]

        except ValueError:
            pass  # Handle bad date
    else:
        current_year = date.today().year
        students = Student.objects.filter(created_at__year=current_year).order_by('created_at')

        monthly_data = defaultdict(int)
        for student in students:
            if student.created_at:
                key = student.created_at.strftime("%b %Y")
                monthly_data[key] += 1

        labels = list(monthly_data.keys())
        counts = list(monthly_data.values())
        
        course_data = (
            students
            .values('courses')
            .annotate(total=Count('id'))
            .order_by('courses')
            )
        course_labels = [c['courses'] for c in course_data]
        course_counts = [c['total'] for c in course_data]

    return render(request, 'report.html', {
        'students':students,
        'labels': labels,
        'counts': counts,
        'course_labels': course_labels,
        'course_counts': course_counts,
    })
    
@login_required(login_url='login_view')
def generate_pdf_report(request):
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        current_year = date.today().year
        
        if start_date == "" and end_date == "":
            students = Student.objects.filter(created_at__year=current_year)
            template_path = 'report_pdf_template.html'
            context = {'students': students}

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'
            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        else:
            students = []
            if start_date and end_date:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                students = Student.objects.filter(created_at__range=(start, end))

            template_path = 'report_pdf_template.html'
            context = {'students': students}

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'
            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    return redirect(report_view)

@login_required(login_url='login_view')
def fees(request):
    if request.method == "POST":
        fee = Fees()
        stu = request.POST.get('student')
        student = get_object_or_404(Student, pk=stu)
        fee.student = student
        fee.amount = request.POST.get('amount')
        fee.paid_date = request.POST.get('date')
        fee.take = request.POST.get('take')
        fee.pay_method = request.POST.get('method')
        fee.save()
        stu_name = Student.objects.filter(id=stu)
        
        html_content = render_to_string('fee_receipt.html', {
            'student': stu_name,
            'fee': fee
        })

        # Convert to PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pisa.CreatePDF(html_content, dest=tmp_file)
            tmp_file.seek(0)
            pdf_data = tmp_file.read()

        # Send email
        email = EmailMessage(
            subject='Your Fee Receipt',
            body='Please find your fee receipt attached.',
            from_email='admin@yourdomain.com',
            to=[student.email],
        )
        email.attach('receipt.pdf', pdf_data, 'application/pdf')
        email.send()
        
        return redirect(fees_list)
    else:
        student = Student.objects.annotate(
            total_paid=Sum('fees__amount')
        ).filter(
            Q(total_paid__lt=F('amount')) | Q(total_paid__isnull=True)
        )
    return render(request,'fees.html',{'student':student})

@login_required(login_url='login_view')
def fees_list(request):
    fee = Fees.objects.all()
    return render(request,'feeslist.html',{'fee':fee})

@login_required(login_url='login_view')
def attendance(request):
    if request.method == 'POST':
        select_stu = request.POST.getlist('student')
        date = request.POST.get('date')
        
        all_student = Student.objects.all()
        
        for student in all_student:
            if str(student.id) in select_stu:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={"status": "P"}
                )
            else:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={"status": "A"}
                )
        return redirect('attendance_list')
    student = Student.objects.all()
    return render(request,'attendance.html',{'student':student})

@login_required(login_url='login_view')
def attendance_list(request):
    if 'start_date' in request.GET and 'end_date' in request.GET:
        start_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()

        
        date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        students = Student.objects.all()

        records = Attendance.objects.filter(date__range=(start_date, end_date))
        status_lookup = defaultdict(dict)
        for r in records:
            status_lookup[r.student_id][r.date] = r.status

        attendance_matrix = []
        for student in students:
            row = [status_lookup[student.id].get(day, '') for day in date_list]
            attendance_matrix.append((student, row))

        context = {
            'date_list': date_list,
            'attendance_matrix': attendance_matrix,
        }
    else:
        today = date.today()
        start = today - timedelta(days=14)  
        end = today

        date_list = [start + timedelta(days=i) for i in range((end - start).days + 1)]

        students = Student.objects.all()
        records = Attendance.objects.filter(date__range=(start, end))

        status_lookup = defaultdict(dict)
        for r in records:
            status_lookup[r.student_id][r.date] = r.status

        attendance_matrix = []
        for student in students:
            row = [status_lookup[student.id].get(day, '') for day in date_list]
            attendance_matrix.append((student, row))

        context = {
            'date_list': date_list,
            'attendance_matrix': attendance_matrix,
        }

    return render(request,"attendancelist.html", context)



    
