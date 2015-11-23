var moveLeft = 0;
var moveRight = 0;
var moveDown = 0;
var moveUp = 0;

window.addEventListener("keydown", function(e) {
// space and arrow keys
if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
          }
        }, false);

        $(function() {
          $("body").keyup(function(e) {
    	  switch (e.which) {
            case 37:
              moveLeft = 0;
              $(".driveLeft").css("background-color", "white");
              $(".driveLeft").css("color", "black");
              break;
            case 38:
              moveUp = 0;
              $(".driveForward").css("background-color", "white");
              $(".driveForward").css("color", "black");
              break;
            case 39:
              moveRight = 0;
              $(".driveRight").css("background-color", "white");
              $(".driveRight").css("color", "black");
              break;
            case 40:
              moveDown = 0;
              $(".driveReverse").css("background-color", "white");
              $(".driveReverse").css("color", "black");
              break;
          }
          e.preventDefault();
          });
          $("body").keydown(function(e) {
    	  switch (e.which) {
            case 37:
              moveLeft = 1;
              console.log("left");
              $(".driveLeft").css("background-color", "green");
              $(".driveLeft").css("color", "white");
              break;
            case 38:
              moveUp = 1;
              $(".driveForward").css("background-color", "green");
              $(".driveForward").css("color", "white");
              break;
            case 39:
              moveRight = 1;
              $(".driveRight").css("background-color", "green");
              $(".driveRight").css("color", "white");
              break;
            case 40:
              moveDown = 1;
              $(".driveReverse").css("background-color", "green");
              $(".driveReverse").css("color", "white");
              break;
          }
          });
        });

        var funcfunc = function() {
          console.log("executing");
        }
