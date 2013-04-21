$(function() {
	
	var $graph = $('.graph_content');

	var data = [100, 200, 150, 230, 100, 200, 100, 200, 150, 230, 100, 200],

	w = $graph.parent().width();
	h = $graph.parent().width() / 2,
	margin = 16,
	y = d3.scale.linear().domain([0, d3.max(data)]).range([0 + margin, h - margin]),
	x = d3.scale.linear().domain([0, data.length]).range([0 + margin, w - margin]);

	var vis = d3.select('.graph_content')
	  .append("svg:svg")
	  .attr("width", w)
	  .attr("height", h);

	var g = vis.append("svg:g")
	  .attr("transform", "translate("+ margin +", "+ (h+margin)  +")");

  var line = d3.svg.line()
    .x(function(d,i) { return x(i); })
    .y(function(d) { return -1 * y(d); });

  g.append("svg:path").attr("d", line(data));

});