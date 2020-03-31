function barGraph1(Data, state) {
	$('#barChart1').remove(); // this is my <canvas> element
  $('#ChartContainer1').append('<canvas id="barChart1" width="400" height="500"></canvas>');
var densityCanvas = document.getElementById("barChart1");

Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 14;

var stateData = {
  label: state,
  data: Data,
  backgroundColor: ["yellow", "red", "green", "blue"],
  borderWidth: 0,
  yAxisID: "y-axis-home"
};



var chartData = {
  labels: ["Active Cases", "Deaths", "Recoveries", "TOTAL"],
  datasets: [stateData]
};

var chartOptions = {
  scales: {
    xAxes: [{
      barPercentage: 1,
      categoryPercentage: 0.6
    }],
    yAxes: [{
      id: "y-axis-home",
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
