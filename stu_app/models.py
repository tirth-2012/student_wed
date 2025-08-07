from django.db import models

# Create your models here.

class Student(models.Model):
    Male='Male'
    Female='Female'
    gender=(
        (Male,'Male'),
        (Female,'Female')
    )
    users = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='students')
    firstname=models.CharField(max_length=200)
    middlename=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    gender=models.CharField(max_length=200,choices=gender,default=Male)
    email=models.EmailField(max_length=200)
    phone=models.CharField(max_length=12)
    house_society_name = models.CharField(max_length=255, null=True, blank=True)
    landmark_area = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10)
    birthday = models.DateField(null=True, blank=True) 
    courses=models.CharField(max_length=50)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateField(null=True, blank=True)
    image=models.ImageField(upload_to='student_image', null=True, blank=True)
    
    def __str__(self):
        return self.firstname
    
    def save(self, *args, **kwargs):
        def to_camel_case(text):
            words = text.replace('_', ' ').split()
            camel = ""
            for w in words:
                if w:
                    camel = camel + w.capitalize()
            return camel

        if self.firstname:
            self.firstname = to_camel_case(self.firstname)
        if self.middlename:
            self.middlename = to_camel_case(self.middlename)
        if self.lastname:
            self.lastname = to_camel_case(self.lastname)
        if self.house_society_name:
            self.house_society_name = to_camel_case(self.house_society_name)
        if self.landmark_area:
            self.landmark_area = to_camel_case(self.landmark_area)
        if self.city:
            self.city = to_camel_case(self.city)
        super().save(*args, **kwargs)
    
class Fees(models.Model):
    Cash='Cash'
    Online='Online'
    Card='Card'
    pay_method=(
        (Cash,'Cash'),
        (Online,'Online'),
        (Card,'Card')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    paid_date=models.DateField()
    take=models.CharField(max_length=50)
    pay_method=models.CharField(max_length=50,choices=pay_method)
    
    def __str__(self):
        return self.take
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('P', 'Present'), ('A', 'Absent')])

    def __str__(self):
        return self.status
    
    
