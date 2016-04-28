var app = angular.module("purpleApp",[]);
app.controller('purpleController',function($scope,lockClaimerService,formSenderService,keySenderService){
  $scope.failure = false;
  $scope.noLock = false;
  $scope.invalidMessage = false;
  $scope.locker = false;
  $scope.claimLock = false;

  $scope.succes = false;
  $scope.unlock = false;
  $scope.superlock_password = 'Password';
  $scope.moveLeft = 0;
  $scope.moveRight = 0;
  $scope.moveDown = 0;
  $scope.moveUp = 0;
  $scope.straightDistance = 50;
  $scope.invalidStraightDistance = false;
  $scope.circRadius = 50;
  $scope.invalidCircRaidus = false;
  $scope.squareSide = 50;
  $scope.invalidSquareSide = false;
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
  $scope.getSuperlock = function(){
    hide_all_messages();
    var promise = lockClaimerService.claimSuperlock($scope.superlock_password);
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
  }
  $scope.getSuperunlock = function(){
    hide_all_messages();
    var promise = lockClaimerService.claimSuperunlock($scope.superlock_password);
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
  }
  $scope.getUnlock = function(){
    hide_all_messages();
    var promise = lockClaimerService.claimUnlock();

    promise.success(function(data,status){
          if (data == 'OK'){
            $scope.unlock = true;
          }
          else{
            $scope.claimLock = true;
          }
      });
    promise.error(function(data,status){
        $scope.failure = true;
      });

  };
  $scope.keyDown = function(e){
    console.log('Keypresed');
      switch (e.which) {
        case 37:
          $scope.keyLeftPressed();
          break;
        case 38:
          $scope.keyUpPressed();
          break;
        case 39:
          $scope.keyRightPressed();
          break;
        case 40:
          $scope.keyDownPressed();
          break;
      }
  }
  $scope.keyUp = function(e){
      switch (e.which) {
        case 37:
          $scope.keyLeftReleased();
          break;
        case 38:
          $scope.keyUpReleased();
          break;
        case 39:
          $scope.keyRightReleased();
          break;
        case 40:
          $scope.keyDownReleased();
          break;
      }
    e.preventDefault();
  }
  $scope.keyLeftPressed = function() {
    if ($scope.moveLeft == 0){
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
    $scope.moveLeft = 1;
    }
  }
  $scope.keyRightPressed = function (){
    if ($scope.moveRight == 0){
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
    $scope.moveRight = 1;
    }
  }
  $scope.keyDownPressed = function(){
    if ($scope.moveDown == 0){
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
      $scope.moveDown = 1;
    }

  }

  $scope.keyUpPressed = function(){
    if ($scope.moveUp == 0){
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
      $scope.moveUp = 1;
    }

  }
  $scope.keyLeftReleased = function(){
    $scope.moveLeft = 0;
    $(".driveLeft").removeClass('succesfulpressed');
    $(".driveLeft").removeClass('failurepressed');
    $(".driveLeft").addClass('not_pressed');
    var promise = keySenderService.sendData('LStop');
  }
  $scope.keyRightReleased = function(){
    $scope.moveRight = 0;
    $(".driveRight").removeClass('succesfulpressed');
    $(".driveRight").removeClass('failurepressed');
    $(".driveRight").addClass('not_pressed');
    var promise = keySenderService.sendData('RStop');
  }
  $scope.keyDownReleased = function (){
    $scope.moveDown = 0;
    $(".driveReverse").removeClass('succesfulpressed');
    $(".driveReverse").removeClass('failurepressed');
    $(".driveReverse").addClass('not_pressed');
    var promise = keySenderService.sendData('BStop');
  }
  $scope.keyUpReleased = function(){
    $scope.moveUp = 0;
    $(".driveForward").removeClass('succesfulpressed');
    $(".driveForward").removeClass('failurepressed');
    $(".driveForward").addClass('not_pressed');
    var promise = keySenderService.sendData('FStop');
  }
  $scope.straightSubmit = function(){
    if ($scope.straightDistance< 20  || $scope.straightDistance>600){
      $scope.invalidStraightDistance = true;
    }
    else{
      $scope.invalidStraightDistance = false;
      hide_all_messages();
      var promise = formSenderService.sendData('STRAIGHT',[$scope.straightDistance])
      promise.success(function(data,status){
            if (data == 'OK'){
              $scope.success = true;
            }
            else if (data == 'FAILURE'){
              $scope.failure = true;
            }
            else{
              $scope.claimLock = true;
            }
        });
      promise.error(function(data,status){
          $scope.failure = true;
        });
    }
  }
  $scope.circSubmit = function(){
    if ($scope.circRadius< 20  || $scope.circRadius>100){
      $scope.invalidCircRaidus = true;
    }
    else{
      $scope.invalidCircRaidus = false;
      hide_all_messages();
      var promise = formSenderService.sendData('CIRC',[$scope.circRadius])
      promise.success(function(data,status){
            if (data == 'OK'){
              $scope.success = true;
            }
            else if (data == 'FAILURE'){
              $scope.failure = true;
            }
            else{
              $scope.claimLock = true;
            }
        });
      promise.error(function(data,status){
          $scope.failure = true;
        });
    }
  }
  $scope.squareSubmit = function(){
    if ($scope.squareSide< 20  || $scope.squareSide>100){
      $scope.invalidSquareSide = true;
    }
    else{
      $scope.invalidSquareSide = false;
      hide_all_messages();
      var promise = formSenderService.sendData('SQUARE',[$scope.squareSide])
      promise.success(function(data,status){
            if (data == 'OK'){
              $scope.success = true;
            }
            else if (data == 'FAILURE'){
              $scope.failure = true;
            }
            else{
              $scope.claimLock = true;
            }
        });
      promise.error(function(data,status){
          $scope.failure = true;
        });
    }
  }
  $scope.parcoursSubmit = function(){
    hide_all_messages();
    var valid_commands = ['Left','Right','Distance'];
    var str = $scope.parcours;
    /*
    var steps = str.split(',');
    var parsed_steps = []
    for (var i = 0; i < steps.length-1; i++){
      console.log(steps[i]);
      var number = steps[i].match(/\(([^)]+)\)/)[1];
      var command = steps[i].match(/(.*)\(/)[1];
      if ($.inArray(command, valid_commands) && !isNaN(number)){
        console.log('Idioot')
        parsed_steps.push([command[0],parseInt(number)]);
      }
      console.log(arrayObj.join('\n'));
    }
    */
    var promise = formSenderService.sendData({'parcours':str});
    promise.success(function(data,status){
        if (data == 'OK'){
          $scope.succes = true;
        }
        if (data == 'FAILURE'){
          $scope.failure = true;
        }
        else{
          $scope.claimLock = true;
        }
    });
    promise.error(function(data,status){
      $scope.failure = true;
    });
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
  lockClaimer.claimSuperlock = function(passw){
    var promise = $http({method:'POST',
                          url:'/superlock',
                          data:JSON.stringify({'passw':passw}),
                          headers: {'Content-Type': 'application/json'}});
    return promise;
  }
  lockClaimer.claimSuperunlock = function(passw){
    var promise = $http({method:'POST',
                          url:'/superunlock',
                          data:JSON.stringify({'passw':passw}),
                          headers: {'Content-Type': 'application/json'}});
    return promise;
  }
  return lockClaimer;
});
app.factory('formSenderService',function($http){
  var formSender = {};
  formSender.sendData = function(command,arguments){
    var promise = $http({method:'POST',url:'/drive',
      data:JSON.stringify({'command':command,'arguments':arguments}),
      headers: {'Content-Type': 'application/json'}
      });
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
