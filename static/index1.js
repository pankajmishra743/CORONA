function barGraph(dates,sData,aData,nData,state,day) {
	$('#barChart').remove(); // this is my <canvas> element
  $('#ChartContainer').append('<canvas id="barChart" width="1300" height="800"></canvas>');
var densityCanvas = document.getElementById("barChart");

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 14;

var selected_Label;
if(day != "All Days")
	selected_Label = state + ' Cases';
else
	selected_Label = state;
var stateData = {
  label: selected_Label,
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
		gridLines: {
                display:false
            },
      barPercentage: 1,
      categoryPercentage: 1.0
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
  type: 'bar',
  data: chartData,
  options: chartOptions
});
}
