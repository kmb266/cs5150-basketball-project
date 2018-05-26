
function hideCol(el) {
  var classname = el.id;
  var thisElem = document.getElementById(classname);
  var thisHeader = document.getElementById(classname+"_header")
  // console.log(isShown);
  // console.log(isShown.style.display);
  var classes = document.getElementsByClassName(classname);
  var checkFirst = classes[0].style.display;
  if (checkFirst === 'none') {
    for (var i = 0; i < classes.length; i++) {
      classes[i].style.display = "inline";
    }
    thisElem.innerHTML = "-";
    thisElem.style.color = "red";
    thisHeader.style.width = "inherit";
  }
  else {
    for (var i = 0; i < classes.length; i++) {
      classes[i].style.display = "none";
    }
    thisElem.innerHTML = "+";
    thisElem.style.color = "green";
    thisHeader.style.width = "5px";
  }



}
