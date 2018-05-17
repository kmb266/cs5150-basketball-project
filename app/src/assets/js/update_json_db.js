// constants
const {BrowserWindow} = require('electron');
const path = require('path');
const Store = require('electron-store');
const store = new Store();

const IN_PROGRESS = 'in-progress';
const DONE = 'done';
const FAILURE = 'failure';

let win;

// set user metadata
// var oldDate = store.get('lastOpen');
var date = new Date();
// store.set('lastOpen', date);

var last_updated_start = store.get('update.json.start_date');
last_updated_start = new Date(last_updated_start);
var last_update_did_succeed = store.get('update.json.success');

function createUpdateDbWindow() {
  const modalPath = path.join('file://', __dirname, '../../templates/updatingDb.html');
  win = new BrowserWindow({
    width: 500,
    height: 400,
    frame: false,
    backgroundColor: '#fff',
    minWidth: 500,
    minHeight: 400,
    x: 0,
    y: 0
  });
  win.on('close', () => { win = null });
  // win.setAlwaysOnTop(true, "floating", 1);
  win.loadURL(modalPath);
  win.focus();
}

// set user metadata
// var oldDate = store.get('lastOpen');
var date = new Date();
// store.set('lastOpen', date);

var last_updated_start = store.get('update.json.start_date');
last_updated_start = new Date(last_updated_start);
var last_update_did_succeed = store.get('update.json.success');


function updateJsonDB(today, callback) {
  /*
    Makes a call to the backend to update the basketball_json db with new data
  */

  // set json updating status to in progress and update other data
  store.set('update.json.start_date', today);
  store.delete('update.json.end_date');
  store.set('update.json.status',IN_PROGRESS);
  store.set('update.json.success', false);

  var path_to_exe = path.join(__dirname, '../../python', 'middle_stack', 'espn_to_db'),
      py = require('child_process').execFile(path_to_exe),
      data = {'lastOpen': date},
      dataString = '';
  // console.log(path_to_exe);
  // console.log(require('fs').existsSync(path_to_exe));

  // retrieve the data from the auto_complete.py
  py.stdout.on('data', function(data){
    dataString += data.toString();
  });

  // print the data when the child process ends
  py.stdout.on('end', function(){
    // console.log(dataString)
  });

  // if there is an error, print it out
  py.on('error', function(err) {
    console.log("Failed to start child. " + err);
    store.set('update.json.status', FAILURE);
    store.set('update.json.success', false);
  });

  py.on('exit', function(code){
    console.log('Exit code: ', code)
    if (code == 0) {
      callback(dataString)
    }
    else {
      store.set('update.json.status', FAILURE);
      store.set('update.json.success', false);
    }
  })

  // py.stdin.write(JSON.stringify(data));
  py.stdin.end();
}

function finshedJsonDbBUpdate(stdout) {
  console.log(stdout);
  // set json updating status to complete and update other data
  var end_date = new Date();
  store.set('update.json.end_date', end_date);
  store.set('update.json.status', DONE);
  store.set('update.json.success', true);
  win.webContents.send('update_status', {msg:DONE});
}


console.log('previous store:', store.store);

if (store.get('update.json.status') == 'in-progress') {
  console.log('The ESPN data is currently being updated.');
}
else if (last_updated_start != undefined
          && last_updated_start.toLocaleDateString() == date.toLocaleDateString()
          && last_update_did_succeed) {
  console.log("Your ESPN data should be up to date!");
}
else {
  console.log('starting jsonDB update');
  createUpdateDbWindow();
  updateJsonDB(date, finshedJsonDbBUpdate);
}

console.log('Trying to update xml files')
var path_to_exe = path.join(__dirname, '../../python', 'middle_stack', 'xml_downloader'),
    py = require('child_process').execFile(path_to_exe)
console.log('Finished updating XML files')

