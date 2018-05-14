// constants
const Store = require('electron-store');
const store = new Store();

const IN_PROGRESS = 'in-progress';
const DONE = 'done';
const FAILURE = 'failure';

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

  // uncomment here if in prod
  // var path_to_exe = path.join(__dirname, 'python', 'backend', 'espn_to_db'),
  //     py = require('child_process').execFile(path_to_exe),
  //     data = {'lastOpen': date},
  //     dataString = '';
  // console.log(path_to_exe);
  // console.log(fs.existsSync(path_to_exe));

  // comment out below if in prod
  var spawn = require('child_process').spawn,
      py = spawn('python', ['./espn_to_db.py']),
      // data = {'lastOpen': oldDate.getTime()},
      dataString = '';

  // retrieve the data from the auto_complete.py
  py.stdout.on('data', function(data){
    dataString += data.toString();
  });

  // print the data when the child process ends
  py.stdout.on('end', function(){
    // console.log(dataString)
    callback(dataString)
  });

  // if there is an error, print it out
  py.on('error', function(err) {
    console.log("Failed to start child. " + err);
    store.set('update.json.status', FAILURE);
    store.set('update.json.success', false);
  });

  py.on('exit', function(code){
    console.log('Exit code: ', code)
    if (code == 0 || code == 1) {
      store.set('update.json.status', DONE);
      store.set('update.json.success', true);
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
  // set json updating status to complete and update other data
  var end_date = new Date();
  store.delete('update.json.end_date', end_date);
  store.set('update.json.status', DONE);
  store.set('update.json.success', true);
}

if (store.get('update.json.status') == 'in-progress') {
  console.log('The ESPN data is currently being updated.');
}
else if (last_updated_start != undefined && last_updated_start.toLocaleDateString() == date.toLocaleDateString() && last_update_did_succeed) {
  console.log("Your ESPN data should be up to date!");
}
else {
  console.log('starting jsonDB update');
  updateJsonDB(date, finshedJsonDbBUpdate);
}
