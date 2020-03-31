function barGraph(dates,sData,aData,nData,state) {
	$('#barChart').remove(); // this is my <canvas> element
  $('#ChartContainer').append('<canvas id="barChart" width="1300" height="800"></canvas>');
var densityCanvas = document.getElementById("barChart");

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 14;

var stateData = {
  label: state + ' Cases',
  data: sData,
  backgroundColor: 'rgba(230, 0, 0, 1)',
  borderWidth: 0,
  yAxisID: "y-axis-home",
  fill: false
};

var newData = {
  label: 'All India New Cases',
  data: nData,
  backgroundColor: 'rgba(118, 165, 64, 1)',
  borderWidth: 0,
  fill: false
  //yAxisID: "y-axis-away"
};

var allData = {
  label: 'All India Total Cases',
  data: aData,
  backgroundColor: 'rgba(225, 125, 25, 1)',
  borderWidth: 0,
  fill: false
  //yAxisID: "y-axis-away"
};

var chartData = {
  labels: dates,
  
  datasets: [stateData,newData,allData] 
};

var chartOptions = {
  scales: {
    xAxes: [{
      barPercentage: 1,
	    gridLines: {
                display:false
            },
      categoryPercentage: 1.0
    }],
    yAxes: [{
      id: "y-axis-home",
	    gridLines: {
                display:false
            },
	  ticks:{
              beginAtZero:true,
			  stepSize: 100
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
  type: 'bar',
  data: chartData,
  options: chartOptions
});
}
