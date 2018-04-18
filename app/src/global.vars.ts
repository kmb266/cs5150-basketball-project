'use strict';
export const navHeight: number = 50;
export const pages: Array<string> = ["players", "teams","games"];
export const numPages: number = pages.length;
export const secondsToGametime = (totalSeconds) => {
  if (Math.abs(totalSeconds) > 1200) {
    var s = Math.abs(totalSeconds) - 20*60;
    var minutes = Math.floor(s / 60);
    var seconds = s % 60;
    if (minutes < 10) {minutes = '0'+ minutes;}
    if (seconds < 10) {seconds = '0'+ seconds;}
    return minutes+':'+seconds
  }
  var s = Math.abs(totalSeconds);
  var minutes = Math.floor(s / 60);
  var seconds = s % 60;
  if (minutes < 10) {minutes = '0'+ minutes;}
  if (seconds < 10) {seconds = '0'+ seconds;}
  return minutes+':'+seconds;
}
export const gametimeToSeconds = (gametime, isSecondHalf) => {
  var minSec = gametime.split(":");
  if (isSecondHalf) return parseInt(minSec[0])*60 + parseInt(minSec[1]);
  return parseInt(minSec[0])*60 + parseInt(minSec[1]) + 1200;
}

export const createSelect2 = (id, placeholder, getData) => {
  $(id).select2({
    // dropdownCssClass : 'small-dropdown'
    placeholder: placeholder,
    dropdownAutoWidth : true,
    width: 'element',
    data: getData()
  });
}

export const updateSliderStart = (that, clock, inputId) => {
  /*
    Changes the start time of range slider with id:inputId to
    the input clock time

    Inputs:
      clock: string = game time string in format 'MM:SS'
      inputId: string = id of the range slider that corresponds to input
        being changed
  */
  var seconds = - globals.gametimeToSeconds(clock, that.startTime2ndHalf[inputId]);
  if (seconds >= that.gametime[inputId].end.sec) {
    that.invalidInput(event);
    return;
  }

  that.gametime[inputId].start.clock = clock;
  that.gametime[inputId].start.sec = seconds;
  var slider = $("#"+inputId).data("ionRangeSlider");
  slider.update({from: seconds});
}
export const updateSliderEnd = (that, clock, inputId) => {
  /*
    Changes the end time of range slider with id:inputId to
    the input clock time

    Inputs:
      clock: string = game time string in format 'MM:SS'
      inputId: string = id of the range slider to be changed
  */
  var seconds = - globals.gametimeToSeconds(clock, that.endTime2ndHalf[inputId]);
  if (seconds <= that.gametime[inputId].start.sec) {
    that.invalidInput(event);
    return;
  }
  that.gametime[inputId].end.clock = clock;
  that.gametime[inputId].end.sec = seconds;
  var slider = $("#"+inputId).data("ionRangeSlider");
  slider.update({to: seconds});
}
export const changedStartHalf( = that, inputId) => {
  /*
    Changes the slider with id inputId start time to the opposite half of what it
    currently is.
    If the box is currelty not checked, the time is in the first half.
    If you check the box, the time displayed in the text input that corresponds
    to the slider with id:inputId is now in the second half and vice versa.

    Inputs:
      inputId: string = id of range slider to be changed
  */
  var slider = $("#"+inputId).data("ionRangeSlider");
  if (that.startTime2ndHalf[inputId]) {
    that.gametime[inputId].start.sec += 1200;
    slider.update({from: that.gametime[inputId].start.sec});
  }
  else {
    that.gametime[inputId].start.sec -= 1200;
    slider.update({from: that.gametime[inputId].start.sec});
  }

  console.log(that.gametime[inputId].start.sec);
}
export const changedEndHalf = (that, inputId) => {
  /*
    Changes the slider with id inputId end time to the opposite half of what it
    currently is.
    If the box is currelty not checked, the time is in the first half.
    If you check the box, the time displayed in the text input that corresponds
    to the slider with id:inputId is now in the second half and vice versa.

    Inputs:
      inputId: string = id of range slider to be changed
  */
  var slider = $("#"+inputId).data("ionRangeSlider");
  if (that.endTime2ndHalf[inputId]) {
    that.gametime[inputId].end.sec += 1200;
    slider.update({to: that.gametime[inputId].end.sec});
  }
  else {
    that.gametime[inputId].end.sec -= 1200;
    slider.update({to: that.gametime[inputId].end.sec});
  }

  console.log(that.gametime[inputId].end.sec);
}

export const getUpOrDown = () => {
  var data = [
    {
      id: 'up',
      text: 'up by'
    },
    {
      id: 'down',
      text: 'down'
    },
    {
      id: 'withIn',
      text: 'within',
      selected: true
    },
  ];
  return data;
}

export const applyFilters = (page, filters_data, emitter) => {
  // initial a child process

  // When packaging the app, use pyinstaller to package all of the python files
  // and then put the dist directory in the python folder and the files will run
  // uncomment the next 3 lines to replace spawn and py vars below
  // got ideas from https://github.com/fyears/electron-python-example
  // var path = require('path'),
  //     path_to_exe = path.join(__dirname, 'python', 'dist', 'data_manager','data_manager'),
  //     py = require('child_process').execFile(path_to_exe),

  var spawn = require('child_process').spawn,
      py = spawn('python', ['./data_manager.py']),
      data = [99,2,3,4,5,6,7,8,9],
      dataString = '';

  // retrieve the data from the data_manager.py
  py.stdout.on('data', function(data){
    dataString += data.toString();
  });

  // print the data when the child process ends
  py.stdout.on('end', function(){
    emitter.emit(dataString);
  });

  // if there is an error, print it out
  py.on('error', function(err) {
    console.log("Failed to start child. " + err);
  });

  py.stdin.write(JSON.stringify(data));
  py.stdin.end();

  /*
  const {exec} = require('child_process');
  exec('python ./data_manager.py', (error, stdout, stderr) => {
    if (error) {
      console.log(error);
    } else {
      //console.log(stderr);
      console.log(stdout);
    }
  });
  */
}
