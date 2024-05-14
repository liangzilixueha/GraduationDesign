var x = 0;
function 查验真伪() {
  var container = document.getElementsByClassName("upload-container")[0];
  if (x == 0) {
    //设置其周边散发红光
    container.style.boxShadow = "0 0 20px 20px rgba(255,0,0,0.5)";
    x = 1;
  } else {
    //设置其周边散发绿光
    container.style.boxShadow = "0 0 20px 20px rgba(0,255,0,0.5)";
    x = 0;
  }
}
