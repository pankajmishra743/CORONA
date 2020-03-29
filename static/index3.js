function myupdateMetaData(data) {
    // Reference to Panel element for sample metadata
    var PANEL = document.getElementById("country-metadata");
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
  
function mygetData(country) {
    var dates;
    // Use a request to grab the json data needed for all charts
    Plotly.d3.json(`/wmetadata/${country}`, function(error, wmetaData) {
        if (error) return console.warn(error);
        myupdateMetaData(wmetaData);
        
    });
    
    Plotly.d3.json(`/wdates`, function(error, AllDates) {
        if (error) return console.warn(error);
		Plotly.d3.json(`/${country}/conf`, function(error, confData) {
			if (error) return console.warn(error);
			Plotly.d3.json(`/${country}/recv`, function(error, recvData) {
				if (error) return console.warn(error);
					Plotly.d3.json(`/${country}/death`, function(error, deathData) {
					if (error) return console.warn(error);
					Graph(AllDates, confData, recvData, deathData);	
				});
			});
		});
    });
	

	
    
     
}
function mygetOptions() {
    // Grab a reference to the dropdown select element
    var selDataset = document.getElementById('wselDataset');
    // Use the list of sample names to populate the select options
    Plotly.d3.json('/wcnames', function(error, stateList) {
        for (var i = 0; i < stateList.length; i++) {
            var currentOption = document.createElement('option');
            currentOption.text = stateList[i];
            currentOption.value = stateList[i]
            selDataset.appendChild(currentOption);
        }
        mygetData(stateList[0]);
    })
}
function myoptionChanged(country) {
    // Fetch new data each time a new sample is selected
    mygetData(country);
}
function init() {
    mygetOptions();
}
// Initialize the dashboard
init();
/**
* BONUS Solution
**/
