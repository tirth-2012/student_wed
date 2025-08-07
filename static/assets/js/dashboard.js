(function ($) {
  'use strict';
  if ($("#visit-sale-chart").length) {
    const ctx = document.getElementById('visit-sale-chart');
    const graphGradient1 = ctx.getContext("2d");
    const graphGradient2 = ctx.getContext("2d");
    const graphGradient3 = ctx.getContext("2d");

    const gradientStrokeViolet = graphGradient1.createLinearGradient(0, 0, 0, 181);
    gradientStrokeViolet.addColorStop(0, 'rgba(218, 140, 255, 1)');
    gradientStrokeViolet.addColorStop(1, 'rgba(154, 85, 255, 1)');

    const gradientStrokeBlue = graphGradient2.createLinearGradient(0, 0, 0, 360);
    gradientStrokeBlue.addColorStop(0, 'rgba(54, 215, 232, 1)');
    gradientStrokeBlue.addColorStop(1, 'rgba(177, 148, 250, 1)');

    const gradientStrokeRed = graphGradient3.createLinearGradient(0, 0, 0, 300);
    gradientStrokeRed.addColorStop(0, 'rgba(255, 191, 150, 1)');
    gradientStrokeRed.addColorStop(1, 'rgba(254, 112, 150, 1)');

    const bgColor1 = ["rgba(218, 140, 255, 1)"];
    const bgColor2 = ["rgba(54, 215, 232, 1)"];
    const bgColor3 = ["rgba(255, 191, 150, 1)"];

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: studentLabels,
        datasets: [{
          label: "Monthly Admissions",
          borderColor: gradientStrokeBlue,
          backgroundColor: gradientStrokeBlue,
          fillColor: bgColor3,
          hoverBackgroundColor: gradientStrokeBlue,
          pointRadius: 0,
          fill: false,
          borderWidth: 1,
          fill: 'origin',
          data: studentCounts,
          barPercentage: 0.5,
          categoryPercentage: 0.5,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        elements: {
          line: { tension: 0.4 },
        },
        scales: {
          y: {
            display: false,
            grid: { display: true, drawOnChartArea: true, drawTicks: false },
          },
          x: {
            display: true,
            grid: { display: false },
          }
        },
        plugins: {
          legend: { display: false }
        }
      },
      plugins: [{
        afterDatasetUpdate: function (chart, args, options) {
          const chartId = chart.canvas.id;
          const legendId = `${chartId}-legend`;
          const ul = document.createElement('ul');
          const dataset = chart.data.datasets[0];


          ul.innerHTML = `
          <li>
            <span style="background-color: ${dataset.backgroundColor}"></span>
            ${dataset.label}
          </li>
        `;

          const legendEl = document.getElementById(legendId);
          if (legendEl) {
            legendEl.innerHTML = "";
            legendEl.appendChild(ul);
          }
        }
      }]
    });
  }


  // chart for course count
  if ($("#course-count-chart").length) {
    const ctx = document.getElementById('course-count-chart');
    const graphGradient1 = ctx.getContext("2d");
    const graphGradient2 = ctx.getContext("2d");
    const graphGradient3 = ctx.getContext("2d");

    const gradientStrokeViolet = graphGradient1.createLinearGradient(0, 0, 0, 181);
    gradientStrokeViolet.addColorStop(0, 'rgba(218, 140, 255, 1)');
    gradientStrokeViolet.addColorStop(1, 'rgba(154, 85, 255, 1)');

    const gradientStrokeBlue = graphGradient2.createLinearGradient(0, 0, 0, 360);
    gradientStrokeBlue.addColorStop(0, 'rgba(54, 215, 232, 1)');
    gradientStrokeBlue.addColorStop(1, 'rgba(177, 148, 250, 1)');

    const gradientStrokeRed = graphGradient3.createLinearGradient(0, 0, 0, 300);
    gradientStrokeRed.addColorStop(0, 'rgba(255, 191, 150, 1)');
    gradientStrokeRed.addColorStop(1, 'rgba(254, 112, 150, 1)');

    const bgColor1 = ["rgba(218, 140, 255, 1)"];
    const bgColor2 = ["rgba(54, 215, 232, 1)"];
    const bgColor3 = ["rgba(255, 191, 150, 1)"];

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: courseLabels,
        datasets: [{
          label: "Course Statistics",
          borderColor: gradientStrokeBlue,
          backgroundColor: gradientStrokeBlue,
          fillColor: bgColor3,
          hoverBackgroundColor: gradientStrokeBlue,
          pointRadius: 0,
          fill: false,
          borderWidth: 1,
          fill: 'origin',
          data: courseCounts,
          barPercentage: 0.5,
          categoryPercentage: 0.5,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        elements: {
          line: { tension: 0.4 },
        },
        scales: {
          y: {
            display: false,
            grid: { display: true, drawOnChartArea: true, drawTicks: false },
          },
          x: {
            display: true,
            grid: { display: false },
          }
        },
        plugins: {
          legend: { display: false }
        }
      },
      plugins: [{
        afterDatasetUpdate: function (chart, args, options) {
          const chartId = chart.canvas.id;
          const legendId = `${chartId}-legend`;
          const ul = document.createElement('ul');
          const dataset = chart.data.datasets[0];


          ul.innerHTML = `
          <li>
            <span style="background-color: ${dataset.backgroundColor}"></span>
            ${dataset.label}
          </li>
        `;

          const legendEl = document.getElementById(legendId);
          if (legendEl) {
            legendEl.innerHTML = "";
            legendEl.appendChild(ul);
          }
        }
      }]
    });
  }




  if ($("#traffic-chart").length) {
    const ctx = document.getElementById('traffic-chart');

    var graphGradient1 = document.getElementById("traffic-chart").getContext('2d');
    var graphGradient2 = document.getElementById("traffic-chart").getContext('2d');
    var graphGradient3 = document.getElementById("traffic-chart").getContext('2d');

    var gradientStrokeBlue = graphGradient1.createLinearGradient(0, 0, 0, 181);
    gradientStrokeBlue.addColorStop(0, 'rgba(54, 215, 232, 1)');
    gradientStrokeBlue.addColorStop(1, 'rgba(177, 148, 250, 1)');
    var gradientLegendBlue = 'rgba(54, 215, 232, 1)';

    var gradientStrokeRed = graphGradient2.createLinearGradient(0, 0, 0, 50);
    gradientStrokeRed.addColorStop(0, 'rgba(255, 191, 150, 1)');
    gradientStrokeRed.addColorStop(1, 'rgba(254, 112, 150, 1)');
    var gradientLegendRed = 'rgba(254, 112, 150, 1)';

    var gradientStrokeGreen = graphGradient3.createLinearGradient(0, 0, 0, 300);
    gradientStrokeGreen.addColorStop(0, 'rgba(6, 185, 157, 1)');
    gradientStrokeGreen.addColorStop(1, 'rgba(132, 217, 210, 1)');
    var gradientLegendGreen = 'rgba(6, 185, 157, 1)';

    // const bgColor1 = ["rgba(54, 215, 232, 1)"];
    // const bgColor2 = ["rgba(255, 191, 150, 1"];
    // const bgColor3 = ["rgba(6, 185, 157, 1)"];

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: yearLabels,
        datasets: [{
          data: yearCounts,
          backgroundColor: [gradientStrokeRed, gradientStrokeGreen, gradientStrokeBlue,],
          hoverBackgroundColor: [
            gradientStrokeRed,
            gradientStrokeGreen,
            gradientStrokeBlue,
          ],
          borderColor: [
            gradientStrokeRed,
            gradientStrokeGreen,
            gradientStrokeBlue,
          ],
          legendColor: [
            gradientLegendRed,
            gradientLegendGreen,
            gradientLegendBlue,
          ]
        }]
      },
      options: {
        cutout: 50,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        responsive: true,
        maintainAspectRatio: true,
        showScale: true,
        legend: false,
        plugins: {
          legend: {
            display: false,
          }
        }
      },
      plugins: [{
        afterDatasetUpdate: function (chart, args, options) {
          const chartId = chart.canvas.id;
          var i;
          const legendId = `${chartId}-legend`;
          const ul = document.createElement('ul');
          for (i = 0; i < chart.data.datasets[0].data.length; i++) {
            ul.innerHTML += `
                <li>
                  <span style="background-color: ${chart.data.datasets[0].legendColor[i]}"></span>
                  ${chart.data.labels[i]}
                </li>
              `;
          }
          return document.getElementById(legendId).appendChild(ul);
        }
      }]
    });
  }



  if ($("#inline-datepicker").length) {
    $('#inline-datepicker').datepicker({
      enableOnReadonly: true,
      todayHighlight: true,
    });
  }
  if ($.cookie('purple-pro-banner') != "true") {
    document.querySelector('#proBanner').classList.add('d-flex');
    document.querySelector('.navbar').classList.remove('fixed-top');
  } else {
    document.querySelector('#proBanner').classList.add('d-none');
    document.querySelector('.navbar').classList.add('fixed-top');
  }

  if ($(".navbar").hasClass("fixed-top")) {
    document.querySelector('.page-body-wrapper').classList.remove('pt-0');
    document.querySelector('.navbar').classList.remove('pt-5');
  } else {
    document.querySelector('.page-body-wrapper').classList.add('pt-0');
    document.querySelector('.navbar').classList.add('pt-5');
    document.querySelector('.navbar').classList.add('mt-3');

  }
  document.querySelector('#bannerClose').addEventListener('click', function () {
    document.querySelector('#proBanner').classList.add('d-none');
    document.querySelector('#proBanner').classList.remove('d-flex');
    document.querySelector('.navbar').classList.remove('pt-5');
    document.querySelector('.navbar').classList.add('fixed-top');
    document.querySelector('.page-body-wrapper').classList.add('proBanner-padding-top');
    document.querySelector('.navbar').classList.remove('mt-3');
    var date = new Date();
    date.setTime(date.getTime() + 24 * 60 * 60 * 1000);
    $.cookie('purple-pro-banner', "true", {
      expires: date
    });
  });
})(jQuery);