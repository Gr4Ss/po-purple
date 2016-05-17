//
// MJPEG
//
var mjpeg_img;
var halted = 0;
var mjpeg_mode = 0;
var error_count = 0;
function reload_img () {
  if(!halted)
    {
      r = Math.floor((Math.random() * 1000) + 1);
      setTimeout("mjpeg_img.src = 'http://10.42.0.23/cam.jpg?time=' + new Date().getTime() + r.toString(16)", 100);
    }//
  else
    {
      setTimeout("reload_img()", 100);
    }

}

function error_img () {
  if (error_count > 5){
    mjpeg_img.onload = null;
    mjpeg_img.src = "/Images/streaming.jpg";
    r = Math.floor((Math.random() * 1000) + 1);
    $('#mjpeg_dest').css({'width':'720px','height':'400px'})
    setTimeout("mjpeg_img.onload=reload_img;mjpeg_img.src = 'http://10.42.0.23/cam.jpg?time=' + new Date().getTime() + r.toString(16)", 10000);
    error_count = 0;
  }
  else{
    error_count += 1;
    setTimeout("reload_img()", 100);
  }
}

function pause_stream(){
  halted = (halted + 1)%2;
  if (halted){
    $("#pauseIcon").removeClass("glyphicon-pause");
    $("#pauseIcon").addClass("glyphicon-play");
    $("#pauseImage").css('display','block');
  }
  else{
    $("#pauseIcon").removeClass("glyphicon-play");
    $("#pauseIcon").addClass("glyphicon-pause");
    $("#pauseImage").css('display','none');
  }
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
