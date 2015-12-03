// Get context with jQuery - using jQuery's .get() method.
var ctx = $("#myChart").get(0).getContext("2d");
// This will get the first returned node in the jQuery collection.

var data = {
labels: [],
datasets: [
  {
      label: "Speedleft",
      fillColor: "rgba(220,220,220,0.2)",
      strokeColor: "rgba(220,220,220,1)",
      pointColor: "rgba(220,220,220,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(220,220,220,1)",
      data: []
  },
  {
      label: "Speedright",
      fillColor: "rgba(151,187,205,0.2)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(151,187,205,1)",
      data: []
  }
]
};
var option = {

///Boolean - Whether grid lines are shown across the chart
scaleShowGridLines : true,

//String - Colour of the grid lines
scaleGridLineColor : "rgba(0,0,0,.05)",

//Number - Width of the grid lines
scaleGridLineWidth : 1,

//Boolean - Whether to show horizontal lines (except X axis)
scaleShowHorizontalLines: true,

//Boolean - Whether to show vertical lines (except Y axis)
scaleShowVerticalLines: true,

//Boolean - Whether the line is curved between points
bezierCurve : true,

//Number - Tension of the bezier curve between points
bezierCurveTension : 0.4,

//Boolean - Whether to show a dot for each point
pointDot : true,

//Number - Radius of each point dot in pixels
pointDotRadius : 4,

//Number - Pixel width of point dot stroke
pointDotStrokeWidth : 1,

//Number - amount extra to add to the radius to cater for hit detection outside the drawn point
pointHitDetectionRadius : 20,

//Boolean - Whether to show a stroke for datasets
datasetStroke : true,

//Number - Pixel width of dataset stroke
datasetStrokeWidth : 2,

//Boolean - Whether to fill the dataset with a colour
datasetFill : false,

//String - A legend template
legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

};

var myLineChart = new Chart(ctx).Line(data,option);
window.setInterval(function(){
load_data();
}, 3000);

function load_data(){
$.getJSON( "data.json", function( data ) {
console.log(data);
var items = [];
$.each( data, function( key, val ) {
items.push(val);
});
var dt = new Date();
var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
myLineChart.addData(items[2:], time);
if (myLineChart.labels.length >= 8){
  myLineChart.removeData();
}
myLineChart.update();});
}
