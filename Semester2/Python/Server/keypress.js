var moveLeft = 0;
var moveRight = 0;
var moveDown = 0;
var moveUp = 0;

var adress = '/keys';

window.addEventListener("keydown", function(e) {
// space and arrow keys
if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
          }
        }, false);

$("body").keyup(function(e) {
  if ($("#collapseTwo").attr('aria-expanded') == 'true'){
  switch (e.which) {
    case 37:
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
  if ($("#collapseSix").attr('aria-expanded') == 'true'){
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

function keyLeftPressed(){
  if (moveLeft == 0){
    $(".driveLeft").removeClass('not_pressed');
    $(".driveLeft").addClass('pressed');
    $.post(adress,{
      command: "LStart"
    });
  moveLeft = 1;
  }
}
function keyRightPressed(){
  if (moveRight == 0){
    $(".driveRight").removeClass('not_pressed');
    $(".driveRight").addClass('pressed');
    $.post(adress,{
      command: "RStart"
    });
  moveRight = 1;
  }
}
function keyDownPressed(){
  if (moveDown == 0){
    $(".driveReverse").removeClass('not_pressed');
    $(".driveReverse").addClass('pressed');
    $.post(adress,{
        command: "BStart"
      });
      moveDown = 1;
    }
}

function keyUpPressed(){
  if (moveUp == 0){
    $(".driveForward").removeClass('not_pressed');
    $(".driveForward").addClass('pressed');
    $.post(adress,{
        command: "FStart"
    });
  moveUp = 1;
  }
}
function keyLeftReleased(){
  moveLeft = 0;
  $(".driveLeft").removeClass('pressed');
  $(".driveLeft").addClass('not_pressed');
  $.post(adress,{
      command: "LStop"
    });
}
function keyRightReleased(){
  moveRight = 0;
  $(".driveRight").removeClass('pressed');
  $(".driveRight").addClass('not_pressed');
  $.post(adress,{
      command: "RStop"
    });
}
function keyDownReleased(){
  moveDown = 0;
  $(".driveReverse").removeClass('pressed');
  $(".driveReverse").addClass('not_pressed');
  $.post(adress,{
        command : "BStop"
    });
}
function keyUpReleased(){
  moveUp = 0;
  $(".driveForward").removeClass('pressed');
  $(".driveForward").addClass('not_pressed');
  $.post(adress,{
      command: "FStop"
    });
}

var funcfunc = function() {
  console.log("executing");
};
