function Graph(dates,confData,recvData,deathData) {
	$('#lineChart').remove(); // this is my <canvas> element
  $('#myChartContainer').append('<canvas id="lineChart" width="1300" height="650"></canvas>');
var densityCanvas = document.getElementById("lineChart");

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 14;

var confirmData = {
  label: 'Total Cases',
  data: confData,
  backgroundColor: 'rgba(225, 125, 25, 1)',
  borderWidth: 0,
  yAxisID: "y-axis-home",
  fill: false
};

var recoveryData = {
  label: 'Total Recoveries',
  data: recvData,
  backgroundColor: 'rgba(118, 165, 64, 1)',
  borderWidth: 0,
  fill: false
  //yAxisID: "y-axis-away"
};

var deathData = {
  label: 'Total Deceased',
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
	    gridLines: {
                display:false
            },
      categoryPercentage: .5,
	  ticks:{
        display: true,
        autoSkip: true,
        maxTicksLimit: dates.length/10
    }
	}],
    yAxes: [{
      id: "y-axis-home",
	    gridLines: {
                display:false
            },
	  ticks:{
              beginAtZero:true,
			  stepSize: 10000
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
  options: chartOptions
});
}
