var app = angular.module("purpleApp",[]);
app.controller('purpleController',function($scope,lockClaimerService,formSenderService,keySenderService){
  $scope.failure = false;
  $scope.noLock = false;
  $scope.invalidMessage = false;
  $scope.locker = false;
  $scope.claimLock = false;
  $scope.succes = false;
  $scope.unlock = false;
  $scope.moveLeft = 0;
  $scope.moveRight = 0;
  $scope.moveDown = 0;
  $scope.moveUp = 0;

  hide_all_messages = function(){
    $scope.failure = false;
    $scope.noLock = false;
    $scope.invalidMessage = false;
    $scope.locker = false;
    $scope.claimLock = false;
    $scope.succes = false;
    $scope.unlock = false;
  }
  $scope.getLock = function(){
    hide_all_messages();
    var promise = lockClaimerService.claimLock()
    promise.success(function(data,status){
          if (data == 'OK'){
            $scope.locker = true;
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
    var promise = lockClaimerService.claimUnlock();

    promise.success(function(data,status){
          if (data == 'OK'){
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
  $scope.keyLeftPressed = function() {
    if (moveLeft == 0){
      $(".driveLeft").removeClass('not_pressed');
      var promise = keySenderService.sendData('LStart');
      promise.success(function(data,status){
          if (data == 'OK'){
            $(".driveLeft").addClass('succesfulpressed');
          }
          else{
            $(".driveLeft").addClass('failurepressed');
          }
      });
      promise.error(function(data,status){
        $(".driveLeft").addClass('failurepressed');
      });
    moveLeft = 1;
    }
  }
  $scope.keyRightPressed = function (){
    if (moveRight == 0){
      $(".driveRight").removeClass('not_pressed');
      var promise = keySenderService.sendData('RStart');
      promise.success(function(data,status){
          if (data == 'OK'){
            $(".driveRight").addClass('succesfulpressed');
          }
          else{
            $(".driveRight").addClass('failurepressed');
          }
      });
      promise.error(function(data,status){
        $(".driveRight").addClass('failurepressed');
      });
    moveRight = 1;
    }
  }
  $scope.keyDownPressed = function(){
    if (moveDown == 0){
      $(".driveReverse").removeClass('not_pressed');
      var promise = keySenderService.sendData('BStart');
      promise.success(function(data,status){
          if (data == 'OK'){
            $(".driveReverse").addClass('succesfulpressed');
          }
          else{
            $(".driveReverse").addClass('failurepressed');
          }
      });
      promise.error(function(data,status){
        $(".driveReverse").addClass('failurepressed');
      });
    }
  }

  $scope.keyUpPressed = function(){
    if (moveUp == 0){
      $(".driveForward").removeClass('not_pressed');
      var promise = keySenderService.sendData('FStart');
      promise.success(function(data,status){
          if (data == 'OK'){
            $(".driveForward").addClass('succesfulpressed');
          }
          else{
            $(".driveForward").addClass('failurepressed');
          }
      });
      promise.error(function(data,status){
        $(".driveForward").addClass('failurepressed');
      });
    }
  }
  $scope.keyLeftReleased = function(){
    moveLeft = 0;
    $(".driveLeft").removeClass('succesfulpressed');
    $(".driveLeft").removeClass('failurepressed');
    $(".driveLeft").addClass('not_pressed');
    var promise = keySenderService.sendData('LStop');
  }
  $scope.keyRightReleased = function(){
    moveRight = 0;
    $(".driveRight").removeClass('succesfulpressed');
    $(".driveRight").removeClass('failurepressed');
    $(".driveRight").addClass('not_pressed');
    var promise = keySenderService.sendData('RStop');
  }
  $scope.keyDownReleased = function (){
    moveDown = 0;
    $(".driveReverse").removeClass('succesfulpressed');
    $(".driveReverse").removeClass('failurepressed');
    $(".driveReverse").addClass('not_pressed');
    var promise = keySenderService.sendData('BStop');
  }
  $scope.keyUpReleased = function(){
    moveUp = 0;
    $(".driveForward").removeClass('succesfulpressed');
    $(".driveForward").removeClass('failurepressed');
    $(".driveForward").addClass('not_pressed');
    var promise = keySenderService.sendData('FStop');
  }
  $scope.commandSubmit = function(){
    
  }
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
    var promise = $http({method:'POST',url:'/data',data:theData});
    return promise;
  };
  return formSender;
});
app.factory('keySenderService',function($http){
  var keySender = {};
  keySender.sendData = function(keyData){
    var promise = $http({
              method:'POST',
              url:'/keys',
              data:JSON.stringify({'command':keyData}),
              headers: {'Content-Type': 'application/json'}
            });
    return promise;
  };
  return keySender;
});
