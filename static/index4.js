function Graph(dates,confData,recvData,deathData,day,country) {
	$('#lineChart').remove(); // this is my <canvas> element
  $('#myChartContainer').append('<canvas id="lineChart" width="1300" height="800"></canvas>');
var densityCanvas = document.getElementById("lineChart");

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 14;

var day_Label;
if(day != "All Days")
	day_Label = ' in ' + day + ' Days';
else
	day_Label = "";
var confirmData = {
  label: 'Total Cases in ' + country,
  data: confData,
  backgroundColor: 'rgba(225, 125, 25, 1)',
  borderWidth: 0,
  yAxisID: "y-axis-home",
  fill: false
};

var recoveryData = {
  label: 'Total Recoveries in ' + country,
  data: recvData,
  backgroundColor: 'rgba(118, 165, 64, 1)',
  borderWidth: 0,
  fill: false
  //yAxisID: "y-axis-away"
};

var deathData = {
  label: 'Total Deceased in ' + country,
  data: deathData,
  backgroundColor: 'rgba(230, 0, 0, 1)',
  borderWidth: 0,
  fill: false
  //yAxisID: "y-axis-away"
};

var chartData = {
  labels: dates,
  
  datasets: [confirmData,recoveryData,deathData] 
};

var chartOptions = {
  scales: {
    xAxes: [{
      barPercentage: 1,
      categoryPercentage: .5,
	  gridLines: {
                display:false
            },
	  ticks:{
        beginAtZero:true
    }
	}],
    yAxes: [{
      id: "y-axis-home",
	  gridLines: {
                display:false
            },
	  ticks:{
              beginAtZero:true
	  }
    }
	    //, {
      //id: "y-axis-away",
	//  ticks:{
          ///    beginAtZero:true
	  //}
    //}
	   ]
  }
};


   
var barChart = new Chart(densityCanvas, {
  type: 'line',
  data: chartData,
  options: chartOptions,
  
});
}
