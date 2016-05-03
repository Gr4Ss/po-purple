//
// MJPEG
//
var mjpeg_img;
var halted = 0;
var mjpeg_mode = 0;

function reload_img () {
  if(!halted)
    {
      mjpeg_img.src = 'http://pipurple/cam.jpg?time=' + new Date().getTime();
    }//setTimeout("mjpeg_img.src = 'http://192.168.0.98/cam.jpg?time=' + new Date().getTime()", 100);
  else
    {
      setTimeout("reload_img()", 100);
    }

}

function error_img () {
  mjpeg_img.onload = null;
  mjpeg_img.src = "/images/streaming.jpg";
  setTimeout("mjpeg_img.onload=reload_img();mjpeg_img.src = 'http://pipurple/cam.jpg?time=' + new Date().getTime()", 10000);
}

//
// Init
//
function init(mjpeg, video_fps, divider) {

  mjpeg_img = document.getElementById("mjpeg_dest");
     mjpeg_img.onload = reload_img;
     mjpeg_img.onerror = error_img;
     reload_img();
}
