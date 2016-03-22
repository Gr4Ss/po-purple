
var adress = '/keys';

window.addEventListener("keydown", function(e) {
// space and arrow keys
if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
            console.log('Pieter')
            e.preventDefault();
          }
        }, false);

$("body").keyup(function(e) {
  console.log($("#collapseTwo").attr('aria-expanded'));
  if ($("#collapseTwo").attr('aria-expanded')){
  switch (e.which) {
    case 37:
      console.log('KeyPressed')
      keyLeftReleased();
      break;
    case 38:
      keyUpReleased();
      break;
    case 39:
      keyRightReleased();
      break;
    case 40:
      keyDownReleased();
      break;
    }
  e.preventDefault();
}
});
$("body").keydown(function(e) {
  console.log($("#collapseTwo").attr('aria-expanded'));
  if ($("#collapseTwo").attr('aria-expanded') == 'true'){
switch (e.which) {
    case 37:
      keyLeftPressed();
      break;
    case 38:
      keyUpPressed();
      break;
    case 39:
      keyRightPressed();
      break;
    case 40:
      keyDownPressed();
      break;
  }
}
});
