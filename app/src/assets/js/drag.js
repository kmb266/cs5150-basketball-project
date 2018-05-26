
function dragify() {
    console.log("DEBUG: in dragify()");
    var tableDragger = require('table-dragger');
    var el = document.getElementById('players-table');
    var dragger = tableDragger(el, {
      mode: 'column',
      dragHandler: '.handle',
      onlyBody: true,
      animation: 300
    });

}