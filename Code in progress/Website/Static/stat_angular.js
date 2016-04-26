var app = angular.module("statApp",[]);
app.controller('statController',function($scope,dataService){
	  $scope.teams = [];
	  $scope.showTeamInfo = false;
	  $scope.selectedTeam = "";
	  $scope.deliveries = [];
	  $scope.positions = [];
	  $scope.loadingTeamInfo = false;
		$scope.errorTeamInfo = false;
	  $scope.lastReload = Date.now();
	  /*
	  Method used when a new team is selected.
	  */
	  $scope.new_team_selected = function(){
			console.log('new team');
			$scope.showTeamInfo = false;
			$scope.errorTeamInfo = false;
			if ($scope.selectedTeam != ""){
		  	$scope.loadingTeamInfo = true;
		  	var promise = dataService.getData($scope.selectedTeam);
		  	promise.success(function(returndata){
					$scope.deliveries = returndata.deliveries;
					$scope.positions = returndata.positions;
					$scope.draw_team_chart($scope.parce_deliveries($scope.deliveries))
					$scope.lastReload = Date.now();
					$scope.loadingTeamInfo = false;
					$scope.showTeamInfo = true;
		  	});
				promise.error(function(){
					$scope.errorTeamInfo = true;
					$scope.loadingTeamInfo = false;
				});
			}
	  }

	  $scope.parce_deliveries = function(){

	  }
	  $scope.update_team_data = function(){


	  }
  $scope.draw_team_chart = function(initial_labels,intial_deliveries){
    var data = {
      labels: initial_labels,
      datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: intial_deliveries
          },
        ]
	};
	var options = {
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
		datasetFill : true,
		//String - A legend template
		legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
	};
	var ctx = document.getElementById("myChart").getContext("2d");
	var myLineChart = new Chart(ctx).Line(data, options);
}

	$scope.get_global_data = function(fn){
		teams = [];
		delivered_parcels = [];
		distance_driven = [];
		var promise = dataService.getData(null);
		promise.success(function(returndata){
			$.each(returndata.data, function(i, obj) {
				console.log(i, obj);
				teams.push(obj.name);
				delivered_parcels.push(obj.delivered);
				distance_driven.push(obj.distance);
			});
		console.log(teams);
		fn(teams,delivered_parcels,distance_driven);
		});
	}

$scope.loop = function(){
	console.log('update');
	$scope.get_global_data($scope.update_chart);
	setTimeout ($scope.loop,10000 );
}

$scope.draw_chart = function(teams,delivered_parcels,distance_driven){
    //Get the context of the canvas element we want to select
    $scope.teams = teams;
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
  $scope.update_chart = function (teams,delivered_parcels,distance_driven){
    for (i = 0; i < teams.length; i++) {
      ind = $scope.teams.indexOf(teams[i]);
      if (ind == -1){
        $scope.teams.push(teams[i]);
        radarChart.addData([delivered_parcels[i], distance_driven[i]], teams[i]);
      }
      else{
        radarChart.datasets[0].points[ind].value = delivered_parcels[i];
        radarChart.datasets[1].points[ind].value = distance_driven[i];
      }
    }
    radarChart.update()
  }

});

app.factory('dataService',function($http){
    var dataGetter = {};

    dataGetter.getData = function(team){
		var url = '/stats/data';
		if (team != null){
			url += '/'+team
		}
		var promise = $http({'method':'GET','url':url});
		return promise;
	};
	return dataGetter;
});
