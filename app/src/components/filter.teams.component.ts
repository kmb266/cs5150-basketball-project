import { NgModule, Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from "@angular/common";
import * as globals from './../global.vars';

const ionRangeSlider = require('ion-rangeslider/js/ion.rangeSlider');
import * as jquery from 'jquery';
window['$'] = jquery;
window['jQuery'] = jquery;
import * as select2 from 'select2';

@Component({
  selector: 'filter-teams',
  templateUrl: 'templates/filter.teams.html'
})
export class TeamsFilterComponent implements OnInit {
  @Output() dataEvent = new EventEmitter<string>();

  currentPageName = "games";
  gametime = {
    tgtSlider:{
      start:{clock: "20:00", sec:-2400},
      end:{clock: "00:00", sec:0}
    },
    tgtSliderExtra:{
      start:{clock: "20:00", sec:-2400},
      end:{clock: "00:00", sec:0}
    }
  };
  startTime2ndHalf = {
    tgtSlider:false,
    tgtSliderExtra: false,
  }
  endTime2ndHalf = {
    tgtSlider:true,
    tgtSliderExtra: true,
  }

  // 2 way bound filters -- simple inputs
  homeGames:boolean = false;
  awayGames:boolean = false;
  neutralGames:boolean = false;
  wins:boolean = false;
  losses:boolean = false;
  lastNGames:string;
  upOrDown:string;

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
    var filters = {};
    // set which page we are requesting the filters from
    filters['page'] = this.currentPageName;
    // Gather dropdown data
    $('.teams-select2').each(function() {
      // Normalize filter names to send to middle stack
      var id = this.id.split('-')[1];
      filters[id] = $(this).val();
    });

    // Gather data not in dropdowns
    filters.gametime = {};
    filters.gametime.slider = this.gametime.pgtSlider;
    filters.gametime.sliderExtra = this.gametime.pgtSliderExtra;
    filters.gametime.multipleTimeFrames = !this.hidePgtExtra;

    filters.upOrDown = [filters.upOrDown, this.upOrDown];
    filters.recentGames = this.lastNGames;

    if (!this.homeGames && !this.awayGames && !this.neutralGames) {
      filters.location = {
        home:true,
        away:true,
        neutral:true
      }
    }
    else {
      filters.location = {
        home:this.homeGames,
        away:this.awayGames,
        neutral:this.neutralGames
      }
    }

    if (!this.wins && !this.losses) {
      filters.outcome = {
        wins: true,
        losses: true
      }
    }
    else {
      filters.outcome = {
        wins: this.wins,
        losses: this.losses
      }
    }

    console.log(filters);
    return filters;
  }
  saveFilters(filters) {
    this.oldFilters.push(filters);
  }
  clearAllFilters() {
    var filters = this.getAllFilters();
    this.saveFilters(filters);
    // clear dropdown inputs
    $('.team-select2').val(null).trigger('change');
    $('#team-select-season').val('season17').trigger('change');

    this.homeGames = false;
    this.awayGames = false;
    this.neutralGames = false;
    this.wins = false;
    this.losses = false;
    $(lastNGames).val(null);
    $(upOrDown).val(null);
    console.log("cleared all filters");
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

  applyPlayerFilters(){
    var filters = this.getAllFilters();
    // this.saveFilters(filters);
    globals.applyFilters(this.currentPageName, filters, this.dataEvent);
  }

  ngOnInit(): void {

    // Setup gametime slider as range slider
    $("#tgtSlider").ionRangeSlider({
      type: "double",
      hide_min_max: true,
      hide_from_to: true,
      min: -20*2*60,
      max: 0,
      from: -20*2*60,
      to: 0,
      onChange: (data) => {
        this.gametime.tgtSlider.start.sec = data.from;
        this.gametime.tgtSlider.end.sec = data.to;

        this.gametime.tgtSlider.start.clock = globals.secondsToGametime(data.from);
        this.gametime.tgtSlider.end.clock = globals.secondsToGametime(data.to);

        if (data.from >= -1200) this.startTime2ndHalf.tgtSlider = true;
        else this.startTime2ndHalf.tgtSlider = false;
        if (data.to >= -1200) this.endTime2ndHalf.tgtSlider = true;
        else this.endTime2ndHalf.tgtSlider = false;
      }
    });
    $("#tgtSliderExtra").ionRangeSlider({
      type: "double",
      hide_min_max: true,
      hide_from_to: true,
      min: -20*2*60,
      max: 0,
      from: -20*2*60,
      to: 0,
      onChange: (data) => {
        this.gametime.tgtSliderExtra.start.sec = data.from;
        this.gametime.tgtSliderExtra.end.sec = data.to;

        this.gametime.tgtSliderExtra.start.clock = globals.secondsToGametime(data.from);
        this.gametime.tgtSliderExtra.end.clock = globals.secondsToGametime(data.to);

        if (data.from >= -1200) this.startTime2ndHalf.tgtSliderExtra = true;
        else this.startTime2ndHalf.tgtSliderExtra = false;
        if (data.to >= -1200) this.endTime2ndHalf.tgtSliderExtra = true;
        else this.endTime2ndHalf.tgtSliderExtra = false;
      }
    });

    // set up the multiple select dropdowns
    select2();
    globals.createSelect2("#teams-team", 'Select Team(s)', this.getTeams);
    globals.createSelect2("#teams-opponent", 'Select Team(s)', this.getOpponents);
    globals.createSelect2("#teams-conference", 'Select Conf(s)', this.getConferences);
    globals.createSelect2("#teams-upOrDown", "Select", globals.getUpOrDown);
    globals.createSelect2("#teams_select-season", 'Ex. 17-18', this.getAvailableSeasons);

    // styling on select2s done here after initialization
    $(".select2-selection__rendered").css("overflow-x","scroll");
    $(".select2-selection.select2-selection--multiple").css("line-height","1em");
    $(".select2-selection.select2-selection--multiple").css("min-height","26px");

  }

}
