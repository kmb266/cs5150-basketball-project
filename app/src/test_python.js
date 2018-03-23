const path = require('path');
const pathToPythonScript = path.join(__dirname, 'read_in_json.py');

var spawn = require('child_process').spawn,
    py    = spawn('python', [pathToPythonScript]),
    data = [1,2,3,4,5,6,7,8,9],
    dataString = '';

py.stdout.on('data', function(data){
  dataString += data.toString();
});
py.stdout.on('end', function(){
  console.log(dataString);
  // $('#blue-number').append(dataString)
});
py.stdin.write(JSON.stringify(data));
py.stdin.end();
