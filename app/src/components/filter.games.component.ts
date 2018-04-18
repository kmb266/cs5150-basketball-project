import { NgModule, Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from "@angular/common";
import * as globals from './../global.vars';

const ionRangeSlider = require('ion-rangeslider/js/ion.rangeSlider');
import * as jquery from 'jquery';
window['$'] = jquery;
window['jQuery'] = jquery;
import * as select2 from 'select2';

@Component({
  selector: 'filter-games',
  templateUrl: 'templates/filter.games.html'
})
export class GamesFilterComponent implements OnInit {
  // use this to pass data to app.component in applyFilters
  @Output() dataEvent = new EventEmitter<string>();

  currentPageName = "games";

  // Object to save time from sliders
  gametime = {
    ggtSlider:{
      start:{clock: "20:00", sec:-2400},
      end:{clock: "00:00", sec:0}
    },
    ggtSliderExtra:{
      start:{clock: "20:00", sec:-2400},
      end:{clock: "00:00", sec:0}
    }
  };
  // Tells if the time referenced in the sliders in the first or second half
  startTime2ndHalf = {
    ggtSlider:false,
    ggtSliderExtra: false,
  }
  endTime2ndHalf = {
    ggtSlider:true,
    ggtSliderExtra: true,
  }


  // 2 way bound filters -- simple checkbox and number inputs
  homeGames:boolean = false;
  awayGames:boolean = false;
  neutralGames:boolean = false;
  wins:boolean = false;
  losses:boolean = false;
  lastNGames:string;
  upOrDown:string;

  oldFilters = [];

  // Tells if the extra slider shown to show two time frames
  hidePgtExtra = true;

  invalidInput(el) {
    //show a red box around the input box
    console.log("invalid input");
  }

  getAllFilters() {
    /*
      Get the filters entered by the user
      Returns: Filter object
      {
        "page": string,
        "team": [],
        "opponent": [],
        "conference": [],
        "upOrDown": [],
        "season": [],
        "gametime": {
          "slider": {
            "start": {
              "clock": "20:00",
              "sec": -2400
            },
            "end": {
              "clock": "00:00",
              "sec": 0
            }
          },
          "sliderExtra": {
            "start": {
              "clock": "20:00",
              "sec": -2400
            },
            "end": {
              "clock": "00:00",
              "sec": 0
            }
          },
          "multipleTimeFrames": boolean
        },
        "location": {
          "home": boolean,
          "away": boolean,
          "neutral": boolean
        },
        "outcome": {
          "wins": boolean,
          "losses": boolean
        }
      }
    */
    // Initialize filters object to return
    var filters = {};

    // set which page we are requesting the filters from
    filters['page'] = this.currentPageName;

    // Gather dropdown data from .page-select2 class
    $('.games-select2').each(function() {
      // Normalize filter names to send to middle stack by removing page name
      var id = this.id.split('-')[1];
      // add filters to filters object
      filters[id] = $(this).val();
    });

    // Gather game time data from sliders
    filters.gametime = {};
    // Normalize gametime object names for simplicity on backend
    filters.gametime.slider = this.gametime.ggtSlider;
    filters.gametime.sliderExtra = this.gametime.ggtSliderExtra;
    // Include if extra time should even be looked at for backend
    filters.gametime.multipleTimeFrames = !this.hidePgtExtra;

    // Gather game score and recent game filters
    filters.upOrDown = [filters.upOrDown, this.upOrDown];
    filters.recentGames = this.lastNGames;

    // Gather game location filters; default is to include all games (all true)
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
    // Gather game outcome filters; default is both wins and losses = true
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
    /*
      Save filters to file in order to be able to use
      back and forward button
      Input:
        filters: object containing all of the filters input by the user
    */
    this.oldFilters.push(filters);
  }
  clearAllFilters() {
    /*
      Clears filters by setting checkboxes to false,
      removing all input from dropdowns, set number inputs to null
    */
    var filters = this.getAllFilters();
    this.saveFilters(filters);
    // clear dropdown inputs
    $('.games-select2').val(null).trigger('change');
    $('#games-select-season').val('season17').trigger('change');

    // clear checkboxes and number inputs
    this.homeGames = false;
    this.awayGames = false;
    this.neutralGames = false;
    this.wins = false;
    this.losses = false;
    $(lastNGames).val(null);
    $(upOrDown).val(null);
    console.log("cleared all filters");
  }


  // Gametime Slider methods -- for specifications look at globals functions
  updateSliderStart(clock, inputId) {
    globals.updateSliderStart(this, clock, inputId);
  }
  updateSliderEnd(clock, inputId) {
    globals.updateSliderEnd(this, clock, inputId);
  }
  changedStartHalf(inputId) {
    globals.changedStartHalf(this, inputId);
  }
  changedEndHalf(inputId) {
    globals.changedEndHalf(this, inputId);
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
    /*
      Get all of the filters as an object
      Save them to be able to enable back and forward buttons
      and send them to the backend
    */
    var filters = this.getAllFilters();
    // this.saveFilters(filters);
    globals.applyFilters(this.currentPageName, filters, this.dataEvent);
  }

  ngOnInit(): void {

    // Setup gametime slider as range slider
    $("#ggtSlider").ionRangeSlider({
      type: "double",
      hide_min_max: true,
      hide_from_to: true,
      min: -20*2*60,
      max: 0,
      from: -20*2*60,
      to: 0,
      onChange: (data) => {
        this.gametime.ggtSlider.start.sec = data.from;
        this.gametime.ggtSlider.end.sec = data.to;

        this.gametime.ggtSlider.start.clock = globals.secondsToGametime(data.from);
        this.gametime.ggtSlider.end.clock = globals.secondsToGametime(data.to);

        if (data.from >= -1200) this.startTime2ndHalf.ggtSlider = true;
        else this.startTime2ndHalf.ggtSlider = false;
        if (data.to >= -1200) this.endTime2ndHalf.ggtSlider = true;
        else this.endTime2ndHalf.ggtSlider = false;
      }
    });
    $("#ggtSliderExtra").ionRangeSlider({
      type: "double",
      hide_min_max: true,
      hide_from_to: true,
      min: -20*2*60,
      max: 0,
      from: -20*2*60,
      to: 0,
      onChange: (data) => {
        this.gametime.ggtSliderExtra.start.sec = data.from;
        this.gametime.ggtSliderExtra.end.sec = data.to;

        this.gametime.ggtSliderExtra.start.clock = globals.secondsToGametime(data.from);
        this.gametime.ggtSliderExtra.end.clock = globals.secondsToGametime(data.to);

        if (data.from >= -1200) this.startTime2ndHalf.ggtSliderExtra = true;
        else this.startTime2ndHalf.ggtSliderExtra = false;
        if (data.to >= -1200) this.endTime2ndHalf.ggtSliderExtra = true;
        else this.endTime2ndHalf.ggtSliderExtra = false;
      }
    });

    // set up the multiple select dropdowns
    // id of dropdowns pattern is #currentPageName-category eg. #games-opponent
    select2();
    globals.createSelect2("#games-team", 'Select Team(s)', this.getTeams);
    globals.createSelect2("#games-opponent", 'Select Team(s)', this.getOpponents);
    globals.createSelect2("#games-conference", 'Select Conf(s)', this.getConferences);
    globals.createSelect2("#games-upOrDown", 'Select', globals.getUpOrDown);
    globals.createSelect2("#games_select-season", 'Ex. 17-18', this.getAvailableSeasons);

    // styling on select2s done here after initialization
    $(".select2-selection__rendered").css("overflow-x","scroll");
    $(".select2-selection.select2-selection--multiple").css("line-height","1em");
    $(".select2-selection.select2-selection--multiple").css("min-height","26px");

  }

}
