function updateMetaData(data) {
    // Reference to Panel element for sample metadata
    var PANEL = document.getElementById("year-metadata");
    // Clear any existing metadata
    PANEL.innerHTML = '';
    // Loop through all of the keys in the json response and
    // create new metadata tags
    for(var key in data) {
        h4tag = document.createElement("h4");
        h4Text = document.createTextNode(`${key}: ${data[key]}`);
        h4tag.append(h4Text);
        PANEL.appendChild(h4tag);
    }
}
  
function getData(state) {
    var dates;
    // Use a request to grab the json data needed for all charts
    Plotly.d3.json(`/metadata/${state}`, function(error, metaData) {
        if (error) return console.warn(error);
        updateMetaData(metaData);
        
    });
    
    Plotly.d3.json(`/dates`, function(error, AllDates) {
        if (error) return console.warn(error);
		Plotly.d3.json(`/statedata/${state}`, function(error, stateData) {
			if (error) return console.warn(error);
			Plotly.d3.json(`/total`, function(error, allData) {
				if (error) return console.warn(error);
					Plotly.d3.json(`/new`, function(error, newTotal) {
					if (error) return console.warn(error);
					barGraph(AllDates, stateData, allData, newTotal, state);	
				});
			});
		});
    });
	
	Plotly.d3.json(`/mdata/${state}`, function(error, metaData) {
				if (error) return console.warn(error);
				barGraph1(metaData, state);	
	});
	
    
     
}
function getOptions() {
    // Grab a reference to the dropdown select element
    var selDataset = document.getElementById('selDataset');
    // Use the list of sample names to populate the select options
    Plotly.d3.json('/names', function(error, stateList) {
        for (var i = 0; i < stateList.length; i++) {
            var currentOption = document.createElement('option');
            currentOption.text = stateList[i];
            currentOption.value = stateList[i]
            selDataset.appendChild(currentOption);
        }
        getData(stateList[0]);
    })
}
function optionChanged(year) {
    // Fetch new data each time a new sample is selected
    getData(year);
}
function init() {
    getOptions();
}
// Initialize the dashboard
init();
/**
* BONUS Solution
**/
