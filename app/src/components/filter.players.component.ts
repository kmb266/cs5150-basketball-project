import { NgModule, Component, Input, OnInit } from '@angular/core';
import { CommonModule } from "@angular/common";
import * as globals from './../global.vars';

const ionRangeSlider = require('ion-rangeslider/js/ion.rangeSlider');
import * as jquery from 'jquery';
window['$'] = jquery;
window['jQuery'] = jquery;
import * as select2 from 'select2';

@Component({
  selector: 'filter-players',
  templateUrl: 'templates/filter.players.html'
})
export class PlayersFilterComponent implements OnInit {
  filters = {};
  gametime = {
    pgtSlider:{
      start:{clock: "20:00", sec:-2400},
      end:{clock: "00:00", sec:0}
    },
    pgtSliderExtra:{
      start:{clock: "20:00", sec:-2400},
      end:{clock: "00:00", sec:0}
    }
  };
  startTime2ndHalf = {
    pgtSlider:false,
    pgtSliderExtra: false,
  }
  endTime2ndHalf = {
    pgtSlider:true,
    pgtSliderExtra: true,
  }

  oldFilters = [];

  hidePgtExtra = true;
  togglePgtExtra() {
    this.hidePgtExtra= !this.hidePgtExtra;
  }

  invalidInput(el) {
    //show a red box around the input box
    console.log("invalid input");
  }

  getAllFilters() {
    var filters = {};
    // TODO: Add all filters here, probably can get with jquery, maybe with angular ---
    return filters;
  }
  saveFilters() {
    var filters = this.getAllFilters();
    this.oldFilters.push(filters);
  }
  clearAllFilters() {
    this.saveFilters()
    console.log("cleared all filters")
    // clear dropdown inputs
    $('.player-select2').val(null).trigger('change');
    $('#select-season').val('season17').trigger('change');
    $('#select-season').val('season17').trigger('change');
    // TODO: clear game-filters here

  }

  // Gametime Slider methods
  updateSliderStart(clock, inputId) {
    var seconds = - globals.gametimeToSeconds(clock, this.startTime2ndHalf[inputId]);
    if (seconds >= this.gametime[inputId].end.sec) {
      this.invalidInput(event);
      return;
    }

    this.gametime[inputId].start.clock = clock;
    this.gametime[inputId].start.sec = seconds;
    var slider = $("#"+inputId).data("ionRangeSlider");
    slider.update({from: seconds});
  }
  updateSliderEnd(clock, inputId) {
    var seconds = - globals.gametimeToSeconds(clock, this.endTime2ndHalf[inputId]);
    if (seconds <= this.gametime[inputId].start.sec) {
      this.invalidInput(event);
      return;
    }
    this.gametime[inputId].end.clock = clock;
    this.gametime[inputId].end.sec = seconds;
    var slider = $("#"+inputId).data("ionRangeSlider");
    slider.update({to: seconds});
  }
  changedStartHalf(inputId) {
    var slider = $("#"+inputId).data("ionRangeSlider");
    if (this.startTime2ndHalf[inputId]) {
      this.gametime[inputId].start.sec += 1200;
      slider.update({from: this.gametime[inputId].start.sec});
    }
    else {
      this.gametime[inputId].start.sec -= 1200;
      slider.update({from: this.gametime[inputId].start.sec});
    }

    console.log(this.gametime[inputId].start.sec);
  }
  changedEndHalf(inputId) {
    var slider = $("#"+inputId).data("ionRangeSlider");
    if (this.endTime2ndHalf[inputId]) {
      this.gametime[inputId].end.sec += 1200;
      slider.update({to: this.gametime[inputId].end.sec});
    }
    else {
      this.gametime[inputId].end.sec -= 1200;
      slider.update({to: this.gametime[inputId].end.sec});
    }

    console.log(this.gametime[inputId].end.sec);
  }

  // TODO: integrate with middle stack team make call to db and get the data for the following
  getPositions() {
    var data = [
      {
          id: 'point-guard',
          text: 'PG'
      },
      {
          id: 'shooting-guard',
          text: 'SG'
      },
      {
          id: 'small-forward',
          text: 'SF'
      },
      {
          id: 'power-forward',
          text: 'PF'
      },
      {
          id: 'center',
          text: 'C'
      }
    ];
    return data;
  }
  getTeams() {
    var data = [
      {
          id: 'team1',
          text: 'Universiy of Alabama'
      },
      {
          id: 'team2',
          text: 'University of Arizona'
      },
      {
          id: 'team25',
          text: 'Cornell',
          selected: true
      },
      {
          id: 'team351',
          text: 'Xavier University'
      }
    ];
    return data;
  }
  getOpponents() {
    var data = [
      {
          id: 'team1',
          text: 'Universiy of Alabama'
      },
      {
          id: 'team2',
          text: 'University of Arizona'
      },
      {
          id: 'team25',
          text: 'Cornell',
      },
      {
          id: 'team351',
          text: 'Harvard',
      }
    ];
    return data;
  }
  getConferences() {
    var data = [
      {
          id: 'conf1',
          text: 'AAC'
      },
      {
          id: 'conf2',
          text: 'ACC'
      },
      {
          id: 'conf3',
          text: 'Ivy League'
      },
      {
          id: 'confX',
          text: 'WAC'
      }
    ];
    return data;
  }
  getCurrentTeamMembers() {
    var data = [
      {
        id: 'cornell-player1',
          text: '1 Kyle Brown'
      },
      {
        id: 'cornell-player10',
          text: '10 Matt Morgan'
      },
      {
          id: 'cornell-player12',
          text: '12 Jordan Abdur Ra\'oof'
      },
      {
        id: 'cornell-player32',
          text: '32 Jack Gordon'
      }
    ];
    return data;
  }
  getAvailableSeasons() {
    var data = [
      {
        id: 'season15',
        text: '2015-16'
      },
      {
        id: 'season16',
        text: '2016-17'
      },
      {
        id: 'season17',
        text: '2017-18',
        selected: true
      },
    ];
    return data;
  }

  createSelect2(id, placeholder, getData) {
    $(id).select2({
      // dropdownCssClass : 'small-dropdown'
      placeholder: placeholder,
      dropdownAutoWidth : true,
      width: 'element',
      data: getData()
    });
  }


  applyPlayerFilters(){
    // initial a child process
    var spawn = require('child_process').spawn,
        py    = spawn('python', ['./data_manager.py']),
        data = [99,2,3,4,5,6,7,8,9],
        dataString = '';

    // retrieve the data from the data_manager.py
    py.stdout.on('data', function(data){
      dataString += data.toString();
    });

    // print the data when the child process ends
    py.stdout.on('end', function(){
      console.log('Result=',dataString);
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

  ngOnInit(): void {

    // Setup gametime slider as range slider
    $("#pgtSlider").ionRangeSlider({
      type: "double",
      hide_min_max: true,
      hide_from_to: true,
      min: -20*2*60,
      max: 0,
      from: -20*2*60,
      to: 0,
      onChange: (data) => {
        this.gametime.pgtSlider.start.sec = data.from;
        this.gametime.pgtSlider.end.sec = data.to;

        this.gametime.pgtSlider.start.clock = globals.secondsToGametime(data.from);
        this.gametime.pgtSlider.end.clock = globals.secondsToGametime(data.to);

        if (data.from >= -1200) this.startTime2ndHalf.pgtSlider = true;
        else this.startTime2ndHalf.pgtSlider = false;
        if (data.to >= -1200) this.endTime2ndHalf.pgtSlider = true;
        else this.endTime2ndHalf.pgtSlider = false;
      }
    });
    $("#pgtSliderExtra").ionRangeSlider({
      type: "double",
      hide_min_max: true,
      hide_from_to: true,
      min: -20*2*60,
      max: 0,
      from: -20*2*60,
      to: 0,
      onChange: (data) => {
        this.gametime.pgtSliderExtra.start.sec = data.from;
        this.gametime.pgtSliderExtra.end.sec = data.to;

        this.gametime.pgtSliderExtra.start.clock = globals.secondsToGametime(data.from);
        this.gametime.pgtSliderExtra.end.clock = globals.secondsToGametime(data.to);

        if (data.from >= -1200) this.startTime2ndHalf.pgtSliderExtra = true;
        else this.startTime2ndHalf.pgtSliderExtra = false;
        if (data.to >= -1200) this.endTime2ndHalf.pgtSliderExtra = true;
        else this.endTime2ndHalf.pgtSliderExtra = false;
      }
    });

    // set up the multiple select dropdowns
    select2();
    this.createSelect2("#player-position", 'Select Position(s)', this.getPositions);
    this.createSelect2("#player-team", 'Select Team(s)', this.getTeams);
    this.createSelect2("#player-opponent", 'Select Team(s)', this.getOpponents);
    this.createSelect2("#player-conference", 'Select Conf(s)', this.getConferences);
    this.createSelect2("#player-in-lineup", 'Select Player(s)', this.getCurrentTeamMembers);
    this.createSelect2("#player-out-lineup", 'Select Player(s)', this.getCurrentTeamMembers);
    this.createSelect2("#select-season", 'Ex. 17-18', this.getAvailableSeasons);

    // styling on select2s done here after initialization
    $(".select2-selection__rendered").css("overflow-x","scroll");
    $(".select2-selection.select2-selection--multiple").css("line-height","1em");
    $(".select2-selection.select2-selection--multiple").css("min-height","26px");

  }


}
