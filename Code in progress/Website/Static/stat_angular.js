var app = angular.module("statApp",[]);
app.controller('statController',function($scope,dataService){
	  $scope.teams = [];
	  $scope.showTeamInfo = false;
	  $scope.loadingTeamInfo = false;
		$scope.errorTeamInfo = false;
		$scope.selectedTeam = "";
		$scope.selectedCurrentParcel = null;
		$scope.selectedNbDeliveredParcels = null;
		$scope.selectedCurrentPosition = null;
	  $scope.selectedLastReload = Date.now();
	  /*
	  Method used when a new team is selected.
	  */
	  $scope.load_team_data = function(){
			console.log('new team');
			$scope.showTeamInfo = false;
			$scope.errorTeamInfo = false;
			if ($scope.selectedTeam != ""){
		  	$scope.loadingTeamInfo = true;
		  	var promise = dataService.getData($scope.selectedTeam);
		  	promise.success(function(returndata){
					$scope.selectedCurrentParcel = returndata.current_parcel;
					$scope.selectedCurrentPosition = returndata.current_position;
					$scope.selectedNbDeliveredParcels = returndata.deliveries;
					$scope.selectedLastReload = Date.now();
					$scope.loadingTeamInfo = false;
					$scope.showTeamInfo = true;
		  	});
				promise.error(function(){
					$scope.errorTeamInfo = true;
					$scope.loadingTeamInfo = false;
				});
			}
	  }
		$scope.get_global_data = function(fn){
			teams= [];
			delivered_parcels = [];
			var promise = dataService.getData(null);
			promise.success(function(returndata){
				$.each(returndata, function(i, obj) {
					teams.push(obj.name);
					delivered_parcels.push(obj.deliveries);
				});
			console.log(teams);
			console.log(delivered_parcels);
			fn(teams,delivered_parcels);
			});
		}

	$scope.loop = function(){
		console.log('update');
		$scope.get_global_data($scope.update_chart);
		setTimeout ($scope.loop,5000 );
	}

	$scope.draw_chart = function(teams,delivered_parcels){
		console.log('Draw chart')
		$scope.teams = teams;
		var ctx = document.getElementById("myChart").getContext("2d");
		var data = {
    labels: teams,
    datasets: [
        {
            label: "Number delivered parcels",
            backgroundColor: "rgba(255,99,132,0.2)",
            borderColor: "rgba(255,99,132,1)",
            borderWidth: 1,
            hoverBackgroundColor: "rgba(255,99,132,0.4)",
            hoverBorderColor: "rgba(255,99,132,1)",
            data: delivered_parcels,
        }
    ]
		};
		barChart = new Chart(ctx).Bar(data);
  }
  $scope.update_chart = function (teams,delivered_parcels){
    for (i = 0; i < teams.length; i++) {
      ind = $scope.teams.indexOf(teams[i]);
      if (ind == -1){
        $scope.teams.push(teams[i]);
        barChart.addData([distance_driven[i]], teams[i]);
      }
      else{
				console.log(barChart.datasets[0]);
        barChart.datasets[0].bars[ind].value = delivered_parcels[i];
      }
    }
    barChart.update()
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
