var width = parseInt(d3.select('#scatter')
    .style("width"));

var margin = 10;
var padding = 45;
var labelArea = 110;
var height = width * 2/3;

var svg = d3.select("#scatter")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "chart");


svg.append("g").attr("class", "xText");
var xText = d3.select(".xText");

var Y_bottom_text = height - margin - padding;
var X_bottom_text =  (width - labelArea)/2 + labelArea;

xText.attr("transform",`translate(
    ${X_bottom_text}, 
    ${Y_bottom_text})`
    );

xText.append("text")
    .attr("y", -20)
    .attr("data-name", "Total_Cases")
    .attr("data-axis", "x")
    .attr("class","aText active x")
    .text("Total Cases");

xText.append("text")
    .attr("y", 0)
    .attr("data-name", "New_Cases")
    .attr("data-axis", "x")
    .attr("class","aText inactive x")
    .text("New Cases");

xText.append("text")
    .attr("y", 20)
    .attr("data-name", "Total_Deaths")
    .attr("data-axis", "x")
    .attr("class","aText inactive x")
    .text("Total Death");

// y-axis 
svg.append("g").attr("class", "yText");
var yText = d3.select(".yText");

var X_left_text =  margin + padding;
var Y_left_text = (height + labelArea) / 2 - labelArea;
yText.attr("transform",`translate(
    ${X_left_text}, 
    ${Y_left_text}
    )rotate(-90)`
    );

yText .append("text")
    .attr("y", -22)
    .attr("data-name", "Total_Recovered")
    .attr("data-axis", "y")
    .attr("class", "aText active y")
    .text("Recovered");

yText .append("text")
    .attr("y", 0)
    .attr("data-name", "Active_Cases")
    .attr("data-axis", "y")
    .attr("class", "aText inactive y")
    .text("Active Cases");

/*yText .append("text")
    .attr("y", 22)
    .attr("data-name", "1stcase")
    .attr("data-axis", "y")
    .attr("class", "aText inactive y")
    .text("1st Case");*/
    
var radius_of_circle;
function adjustRadius() {
  if (width <= 550) {
    radius_of_circle = 8;}
  else { 
    radius_of_circle = 11;}
}
adjustRadius();

d3.csv("static/assets/data/file1.csv").then(function(csv_data) {
    showPlot(csv_data);
});



















