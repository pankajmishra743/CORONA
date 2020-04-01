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
  
function mygetData(country, day) {
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
					if(day != "All Days"){
					    AllDates = AllDates.slice(AllDates.length - day, AllDates.length);
						confData = confData.slice(confData.length - day, confData.length);
						recvData = recvData.slice(recvData.length - day, recvData.length);
						deathData = deathData.slice(deathData.length - day, deathData.length);
					}
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
        mygetData(stateList[0],"All Days");
    })
}
function myoptionChanged(country) {
    // Fetch new data each time a new sample is selected
	document.getElementById("selDate").selectedIndex = 0;
    mygetData(country,"All Days");
}
function dayChanged(day, coun) {
    // Fetch new data each time a new sample is selected
	var x = document.getElementById('selDate');
	var days = x.options[day-1].text;
    mygetData(coun, days);
}
function init() {
    mygetOptions();
}
// Initialize the dashboard
init();
/**
* BONUS Solution
**/
