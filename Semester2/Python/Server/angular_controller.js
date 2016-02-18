var app = angular.module("purpleApp",[]);
app.controller('purpleController',function($scope,lockClaimerService,formSenderService){
  $scope.failure = false;
  $scope.noLock = false;
  $scope.invalidMessage = false;
  $scope.lock = false;
  $scope.claimLock = false;
  $scope.succes = false;
  $scope.unlock = false;
  hide_all_messages = function(){
    $scope.failure = false;
    $scope.noLock = false;
    $scope.invalidMessage = false;
    $scope.lock = false;
    $scope.claimLock = false;
    $scope.succes = false;
    $scope.unlock = false;
  }
  $scope.getLock = function(){
    hide_all_messages();
    var promise = lockClaimerService.claimLock()
    promise.success(function(data,status){
          if (data.lock == 'OK'){
            $scope.lock = true;
          }
          else{
            $scope.noLock = true;
          }
      });
    promise.error(function(data,status){
        $scope.failure = true;
      });
  };
  $scope.getUnlock = function(){
    hide_all_messages();
    var promise = lockClaimerService.claimUnlock()

    promise.success(function(data,status){
          if (data.unlock == 'OK'){
            $scope.unlock = true;
          }
          else{
            $scope.noLock = true;
          }
      });
    promise.error(function(data,status){
        $scope.failure = true;
      });

  };
  $scope.sendData = function(formName){
    if ('formName' == 'straight'){
      formSenderService.sendData()
    }
  };
});
app.factory('lockClaimerService',function($http){
  var lockClaimer = {};
  lockClaimer.claimLock = function(){
    var promise = $http({method: 'GET',url:'/lock'});
    return promise;
  };
  lockClaimer.claimUnlock = function(){
    var promise = $http({method: 'GET',url:'/unlock'});
    return promise;
  };
  return lockClaimer;
});
app.factory('formSenderService',function($http){
  var formSender = {};
  formSender.sendData = function(theData){
    var promise = $http({method:'GET',url:'/data',data:theData});
    return promise;
  };
  return formSender;
});
