
function dragify() {
    console.log("DEBUG: in dragify()");
    var tableDragger = require('table-dragger');
    var el = document.getElementById('players-table');
    var dragger = tableDragger(el);

    var stats = document.getElementById('playersadv-table');
    var stat_dragger = tableDragger(stats);
}