function showPlot(csvData) {
   var xMin;
   var xMax;
   var yMin;
   var yMax;

   var current_X = "Total_Cases";
   var current_Y = "Total_Recovered";

   var tooltip = d3.tip()
      .attr("class", "d3-tip")
      .offset([40, -60])
      .html(function(d) {
            var stateLine = `<div>${d.Country}</div>`;
            var yLine = `<div>${current_Y}: ${d[current_Y]}</div>`;
            if (current_X === "Total_Cases") {
                xLine = `<div>${current_X}: ${d[current_X]}</div>`}          
            else {
                xLine = `<div>${current_X}: ${parseFloat(d[current_X]).toLocaleString("en")}</div>`;}             
            return stateLine + xLine + yLine  
        });

    svg.call(tooltip);
    function  labelUpdation(axis, clickText) {
        d3.selectAll(".aText")
            .filter("." + axis)
            .filter(".active")
            .classed("active", false)
            .classed("inactive", true);
        
        // switch the text clicked to active
        clickText.classed("inactive", false).classed("active", true);
        }

    //  max & min values for scaling
    function xMinMax() {
      xMin = d3.min(csvData, function(d) {
        return parseFloat(d[current_X]) * 0.85;
      });
      xMax = d3.max(csvData, function(d) {
        return parseFloat(d[current_X]) * 1.15;
      });     
    }

    function yMinMax() {
      yMin = d3.min(csvData, function(d) {
        return parseFloat(d[current_Y]) * 0.85;
      });
      yMax = d3.max(csvData, function(d) {
        return parseFloat(d[current_Y]) * 1.15;
      }); 
    }

    // Scatter plot on X and Y axis 
    xMinMax();
    yMinMax();

    var xScale = d3 
        .scaleLinear()
        .domain([xMin, xMax])
        .range([margin + labelArea, width - margin])

    var yScale = d3
        .scaleLinear()
        .domain([yMin, yMax])
        .range([height - margin - labelArea, margin])

    var xAxis = d3.axisBottom(xScale);
    var yAxis = d3.axisLeft(yScale);

    function tickCount() {
      if (width <= 550) {
         xAxis.ticks(5);
         yAxis.ticks(5);
      }
      else {
          xAxis.ticks(10);
          yAxis.ticks(10);
      }        
    }
    tickCount();

    svg.append("g")
        .call(xAxis)
        .attr("class", "xAxis")
        .attr("transform", `translate(
            0, 
            ${height - margin - labelArea})`
        );

    svg.append("g")
        .call(yAxis)
        .attr("class", "yAxis")
        .attr("transform", `translate(
            ${margin + labelArea}, 
            0 )`
        );

    var allCircles = svg.selectAll("g allCircles").data(csvData).enter();

    allCircles.append("circle")
        .attr("cx", function(d) {
            return xScale(d[current_X]);
        })
        .attr("cy", function(d) {
            return yScale(d[current_Y]);
        })
        .attr("r", radius_of_circle)
        .attr("class", function(d) {
            return "stateCircle " + d.Abbr;
        })
        .on("mouseover", function(d) {
            tooltip.show(d, this);
            d3.select(this).style("stroke", "#323232");
        })
        .on("mouseout", function (d) {
            tooltip.hide(d);
            d3.select(this).style("stroke", "#e3e3e3")
        });

        allCircles
            .append("text")
            .attr("font-size", radius_of_circle)
            .attr("class", "stateText")
            .attr("dx", function(d) {
               return xScale(d[current_X]);
            })
            .attr("dy", function(d) {
              return yScale(d[current_Y]) + radius_of_circle /3;
            })
            .text(function(d) {
                return d.Abbr;
              })

            .on("mouseover", function(d) {
                tooltip.show(d);
                d3.select("." + d.Abbr).style("stroke", "#323789");
            })

            .on("mouseout", function(d) {
                tooltip.hide(d);
                d3.select("." + d.Abbr).style("stroke", "#e3e3e3");
            });

          d3.selectAll(".aText").on("click", function() {
              var self = d3.select(this)

              if (self.classed("inactive")) {
                var axis = self.attr("data-axis")
                var name = self.attr("data-name")

                if (axis === "x") {
                  current_X = name;
                  xMinMax();
                  xScale.domain([xMin, xMax]);
                  svg.select(".xAxis")
                        .transition().duration(750)
                        .call(xAxis);
                  
                  d3.selectAll("circle").each(function() {
                    d3.select(this)
                        .transition().duration(750)
                        .attr("cx", function(d) {
                            return xScale(d[current_X])                
                        });
                  });   

                  d3.selectAll(".stateText").each(function() {
                    d3.select(this)
                        .transition().duration(750)
                        .attr("dx", function(d) {
                            return xScale(d[current_X])                          
                        });
                  });          
                  labelUpdation(axis, self);
                }

                else {
                  current_Y = name;
                  yMinMax();
                  yScale.domain([yMin, yMax]);

                  svg.select(".yAxis")
                        .transition().duration(750)
                        .call(yAxis);

                  d3.selectAll("circle").each(function() {
                    d3.select(this)
                        .transition().duration(750)
                        .attr("cy", function(d) {
                            return yScale(d[current_Y])                
                        });                       
                  });   

                  d3.selectAll(".stateText").each(function() {
                      d3.select(this)
                        .transition().duration(750)
                        .attr("dy", function(d) {
                            return yScale(d[current_Y]) + radius_of_circle/3;                          
                        });
                  });

                  labelUpdation(axis, self);
                }
              }
          });
}