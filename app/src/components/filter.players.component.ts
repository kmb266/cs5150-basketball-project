import { NgModule, Component, Input, OnInit } from '@angular/core';
import { CommonModule } from "@angular/common";
import * as globals from './../global.vars';

const ionRangeSlider = require('ion-rangeslider/js/ion.rangeSlider');
import * as jquery from 'jquery';
window['$'] = jquery;

@Component({
  selector: 'filter-players',
  templateUrl: 'templates/filter.players.html'
})
export class PlayersFilterComponent implements OnInit {
  filters = {};
  gametime = {
    start:{clock: "20:00", sec:-2400},
    end:{clock: "00:00", sec:0}
  };
  startTime2ndHalf:boolean = false;
  endTime2ndHalf:boolean = true;

  runPython() {
    require('../test_python');
  }

  invalidInput(el) {
    //show a red box around the input box
    console.log("invalid input");
  }
  updateSliderStart(clock) {
    var seconds = - globals.gametimeToSeconds(clock, this.startTime2ndHalf);
    if (seconds >= this.gametime.end.sec) {
      this.invalidInput(event);
      return;
    }

    this.gametime.start.clock = clock;
    this.gametime.start.sec = seconds;
    var slider = $("#player-game-time-slider").data("ionRangeSlider");
    slider.update({from: seconds});
  }
  updateSliderEnd(clock) {
    var seconds = - globals.gametimeToSeconds(clock, this.endTime2ndHalf);
    if (seconds <= this.gametime.start.sec) {
      this.invalidInput(event);
      return;
    }
    this.gametime.end.clock = clock;
    this.gametime.end.sec = seconds;
    var slider = $("#player-game-time-slider").data("ionRangeSlider");
    slider.update({to: seconds});
  }


  changedStartHalf() {
    var slider = $("#player-game-time-slider").data("ionRangeSlider");
    if (this.startTime2ndHalf) {
      this.gametime.start.sec += 1200;
      slider.update({from: this.gametime.start.sec});
    }
    else {
      this.gametime.start.sec -= 1200;
      slider.update({from: this.gametime.start.sec});
    }

    console.log(this.gametime.start.sec);
  }
  changedEndHalf() {
    var slider = $("#player-game-time-slider").data("ionRangeSlider");
    if (this.endTime2ndHalf) {
      this.gametime.end.sec += 1200;
      slider.update({to: this.gametime.end.sec});
    }
    else {
      this.gametime.end.sec -= 1200;
      slider.update({to: this.gametime.end.sec});
    }

    console.log(this.gametime.end.sec);
  }


  ngOnInit(): void {

    $("#player-game-time-slider").ionRangeSlider({
      type: "double",
      hide_min_max: true,
      hide_from_to: true,
      min: -20*2*60,
      max: 0,
      from: -20*2*60,
      to: 0,
      onChange: (data) => {
        this.gametime.start.sec = data.from;
        this.gametime.end.sec = data.to;

        this.gametime.start.clock = globals.secondsToGametime(data.from);
        this.gametime.end.clock = globals.secondsToGametime(data.to);

        if (data.from >= -1200) this.startTime2ndHalf = true;
        else this.startTime2ndHalf = false;
        if (data.to >= -1200) this.endTime2ndHalf = true;
        else this.endTime2ndHalf = false;
      }
    });

  }

}
