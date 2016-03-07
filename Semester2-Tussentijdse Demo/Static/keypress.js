
var adress = '/keys';

window.addEventListener("keydown", function(e) {
// space and arrow keys
if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
            console.log('Pieter')
            e.preventDefault();
          }
        }, false);

$("body").keyup(function(e) {
  $scope.$apply(function(){
    console.log($("#collapseTwo").attr('aria-expanded'));
    if ($("#collapseTwo").attr('aria-expanded')){
    switch (e.which) {
      case 37:
        console.log('KeyPressed')
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
  });

});
$("body").keydown(function(e) {
    $scope.$apply(function(){
  console.log($("#collapseTwo").attr('aria-expanded'));
  if ($("#collapseTwo").attr('aria-expanded') == 'true'){
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
});
});
