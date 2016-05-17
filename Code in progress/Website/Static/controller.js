var app = angular.module("controllerApp",[]);
app.controller('controllerController',function($scope,lockClaimerService,formSenderService,keySenderService){
  $scope.failure = false;
  $scope.noLock = false;
  $scope.invalidMessage = false;
  $scope.locker = false;
  $scope.claimLock = false;
  $scope.completedParcours = [];
  $scope.toDoParcours = [];
  $scope.str_parcours = "";
  $scope.parcoursLeft;
  $scope.parcoursRight;
  $scope.succes = false;
  $scope.unlock = false;
  $scope.superlock_password = 'PieterIsDeBeste';
  $scope.moveLeft = 0;
  $scope.moveRight = 0;
  $scope.moveDown = 0;
  $scope.moveUp = 0;
  $scope.straightDistance = null;
  $scope.invalidStraightDistance = false;
  $scope.circRadius = null;
  $scope.invalidCircRaidus = false;
  $scope.squareSide = null;
  $scope.invalidSquareSide = false;
  $scope.packetDeliveryPosition = null;
  $scope.parcoursPaused = false;
  $scope.pauseString = "Pause";
  $scope.parcoursSubmited = false;
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
    if ($("#collapseSix").attr('aria-expanded') == 'true'){
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
  }
  $scope.keyUp = function(e){
    if ($("#collapseSix").attr('aria-expanded') == 'true'){
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
            console.log(data);
            if (data == 'OK'){
              $scope.succes = true;
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
              $scope.succes = true;
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
              $scope.succes = true;
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
    var pat = /(\w+)\((\d+)\)/g;
    $scope.completedParcours = [];
    $scope.toDoParcours = [];
    var match = pat.exec($scope.str_parcours);
    var ind = 0;
    while (match != null){
      $scope.toDoParcours.push({'index':ind,'direction':match[1],'count':match[2],'toDo':match[2]});
      match = pat.exec($scope.str_parcours);
      ind++;
    }
    var promise = formSenderService.sendParcours($scope.toDoParcours);
    promise.success(function(data,status){
        if (data == 'OK'){
          $scope.succes = true;
          $scope.parcoursSubmited = true;
          $scope.parcoursPaused = false;
          $scope.pauseString = "Pause";
          $scope.getParcoursUpdate();
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
  $scope.removeFromParcours =function(obj){
    for (var i=0;i<$scope.toDoParcours.length;i++){
      console.log(obj.index);
      console.log()
      if(obj.index == $scope.toDoParcours[i].index){
        $scope.toDoParcours.splice(i,1);
      }
    }
  }
  $scope.arraymove = function(arr, fromIndex, toIndex) {
    var element = arr[fromIndex];
    arr[fromIndex] = arr[toIndex];
    arr[toIndex] = element;
  }
  $scope.moveUpParcours = function(obj){
    for (var i=1;i<$scope.toDoParcours.length;i++){
      if(obj.index == $scope.toDoParcours[i].index){
        $scope.arraymove($scope.toDoParcours,i,i-1);
      }
    }
  }
  $scope.moveDownParcours=function(obj){
    for(var i=$scope.toDoParcours.length-2;i>-1;i--){
      if(obj.index == $scope.toDoParcours[i].index){
        $scope.arraymove($scope.toDoParcours,i,i+1);

      }
    }
  }
  $scope.updateParcours=function(){
    hide_all_messages();
    var promise = formSenderService.sendParcours($scope.toDoParcours);
    promise.success(function(data,status){
        if (data == 'OK'){
          $scope.succes = true;
          $scope.parcoursPaused = false;
          $scope.pauseString = "Pause";
          $scope.getParcoursUpdate();
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
  $scope.getParcoursUpdate=function(){
    if ($scope.toDoParcours != []){
      var promise = formSenderService.getParcoursUpdate();
      promise.success(function (data) {
          console.log(data);
          if (data.data != []){
            for (var i=0;i<data.data.length;i++){
              if(data.data[i]=='straight'){
                $scope.toDoParcours[0].toDo -= 1;
              }
              else{
                var t = $scope.toDoParcours.shift();
                $scope.completedParcours.push(t);
              }
            }
          }
          if ($scope.toDoParcours.length >0){
            setTimeout($scope.getParcoursUpdate,1000);
          }
      });

    }
  }
  $scope.parcoursReset = function(){
    $scope.str_parcours = "";
  }
  $scope.parcoursAppend = function(appendix){
    $scope.str_parcours = $scope.str_parcours.concat(appendix);
  }
  $scope.parcoursPause = function(){
    console.log('Pause');
    hide_all_messages();
    var promise = formSenderService.pauseParcours($scope.parcoursPaused);
    promise.success(function(data,status){
        if (data == 'OK'){
          $scope.parcoursPaused = !($scope.parcoursPaused);
          if ($scope.parcoursPaused){
            $scope.pauseString = "Restart"
          }
          else{
            $scope.pauseString = "Pause"
          }
        }
    });
    promise.error(function(data,status){
      $scope.failure = true;
    });
  }
  $scope.parsePosition = function(string){
    var pat = /(\d+)/g;
    var position = [0,0];
    position[0] = pat.exec(string)[0];
    position[1] = pat.exec(string)[0];
    return position;
  }

  $scope.startPacketDelivery = function(){
    console.log('start');
    hide_all_messages();
    var pos = $scope.parsePosition($scope.packetDeliveryPosition);
    console.log(pos);
    var promise = formSenderService.startPacketDelivery(pos);
    promise.success(function(data,status){
      if (data == 'OK'){
        $scope.succes = true;
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
  formSender.sendParcours = function(arguments){
    var promise = $http({method:'POST',url:'/parcours',
    data:JSON.stringify({'parcours':arguments}),
    headers: {'Content-Type':'application/json'}
    });
    return promise;
  }
  formSender.pauseParcours = function(paused){
    if (!paused){
      pause = 'PAUSE';
    }
    else{
      pause = 'RESTART';
    }
    console.log(pause)
    var promise = $http({method:'POST',url:'/parcours',
    data:JSON.stringify({'parcours':pause}),
    headers: {'Content-Type':'application/json'}
    });
    return promise;
  }
  formSender.startPacketDelivery = function(pos){
    console.log(pos);
    var promise = $http({method:'POST',url:'/packet_delivery',
    data:JSON.stringify({'position':pos}),
    headers: {'Content-Type':'application/json'}
    });
    return promise;
  }
  formSender.getParcoursUpdate = function(){
    var promise = $http({method:'POST',url:'/parcours/update'});
    return promise;
  }
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
