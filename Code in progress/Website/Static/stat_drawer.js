var radarChart;
var labels;
function get_data(fn){
  teams = [];
  delivered_parcels = [];
  distance_driven = [];
  $.getJSON( "stats/data",function(returndata){
    $.each(returndata.data, function(i, obj) {
        console.log(obj);
        teams.push(obj.name);
        delivered_parcels.push(obj.delivered);
        distance_driven.push(obj.distance);
      });
  fn(teams,delivered_parcels,distance_driven);
  });
}
function loop(){
  console.log('update');
  get_data(update_chart);
  setTimeout ( "loop()", 10000 );
}
function update_chart(teams,delivered_parcels,distance_driven){
  for (i = 0; i < teams.length; i++) {
    ind = labels.indexOf(teams[i]);
    if (ind == -1){
      labels.push(teams[i]);
      radarChart.addData([delivered_parcels[i], distance_driven[i]], team);
    }
    else{
      radarChart.datasets[0].points[ind].value = delivered_parcels[i];
      radarChart.datasets[1].points[ind].value = distance_driven[i];
    }
  }
  radarChart.update()
}
function draw_chart(teams,delivered_parcels,distance_driven){
  //Get the context of the canvas element we want to select
  labels = teams;
  var data = {
        labels: teams,
        datasets: [
          {
            label: "Delivered parcels",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: delivered_parcels
          },
          {
            label: "Distance driven",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: distance_driven
          }
        ]
    };


    var options = {
      //Boolean - Whether to show lines for each scale point
      scaleShowLine : true,

      //Boolean - Whether we show the angle lines out of the radar
      angleShowLineOut : true,

      //Boolean - Whether to show labels on the scale
      scaleShowLabels : false,

      // Boolean - Whether the scale should begin at zero
      scaleBeginAtZero : true,

      //String - Colour of the angle line
      angleLineColor : "rgba(0,0,0,.1)",

      //Number - Pixel width of the angle line
      angleLineWidth : 1,

      //String - Point label font declaration
      pointLabelFontFamily : "'Arial'",

      //String - Point label font weight
      pointLabelFontStyle : "normal",

      //Number - Point label font size in pixels
      pointLabelFontSize : 10,

      //String - Point label font colour
      pointLabelFontColor : "#666",

      //Boolean - Whether to show a dot for each point
      pointDot : true,

      //Number - Radius of each point dot in pixels
      pointDotRadius : 3,

      //Number - Pixel width of point dot stroke
      pointDotStrokeWidth : 1,

      //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
      pointHitDetectionRadius : 20,

      //Boolean - Whether to show a stroke for datasets
      datasetStroke : true,

      //Number - Pixel width of dataset stroke
      datasetStrokeWidth : 2,

      //Boolean - Whether to fill the dataset with a colour
      datasetFill : true,

      //String - A legend template
      legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
    }
    var ctx = $("#myChart").get(0).getContext("2d");
    radarChart = new Chart(ctx).Radar(data, options);

}
