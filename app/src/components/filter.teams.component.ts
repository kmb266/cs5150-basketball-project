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

  // Receive the saved filter from the app component
  @Input()
  set savedFilter(savedFilterObj: object) {

    // NOTE: If we want to run a default filter object on opening the file,
    // do it here, remove the if statement and change the blank.data to a filter

    // if a real option has been selected that is not the null value
    if ($('#saved-filters').val() != -1 ) {

      // apply the saved filters and send to middle stack
      globals.applyFilters(this.currentPageName, savedFilterObj, this.dataEvent);

      this.updateFilters(savedFilterObj);

    }

  }

  currentPageName = "teams";
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
    filters.gametime.slider = this.gametime.tgtSlider;
    filters.gametime.sliderExtra = this.gametime.tgtSliderExtra;
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
    $('.teams-select2').val(null).trigger('change');
    $('#teams-select-season').val('season17').trigger('change');

    this.homeGames = false;
    this.awayGames = false;
    this.neutralGames = false;
    this.wins = false;
    this.losses = false;
    $(lastNGames).val(null);
    $(upOrDown).val(null);

    globals.clearSliders(this, "tgtSlider");

    console.log("cleared all filters");
  }

  updateFilters(filters) {
    /*
      Changes the filters in the side bar to match the chose saved filter
      Inputs:
        filters: Object that contains all of the filter data
    */

    // clear all filters just to be safe
    this.clearAllFilters();

    // set all of the filters with the saved filters
    globals.updateAllSlidersFromSavedFilter(this, 'tgtSlider', filters);
    globals.updateSelect2sFromSavedFilter(this.currentPageName, filters);
    this.updateSimpleInputsFromSavedFilter(filters);

  }

  updateSimpleInputsFromSavedFilter(filters) {
    /*
      Changes the checkboxes in the filter to match the filters data
      Sets the non dropdown input values to match the filters data
      Inputs:
        filters: Object that contains all of the filter data

      // NOTE:  this needs to be component specific because each component has
                a different set of filters
    */

    // set score input
    this.upOrDown = filters.upOrDown[1];

    // set recent games input
    this.lastNGames = filters.recentGames;

    // set location checkboxes
    this.homeGames = filters.location.home;
    this.awayGames = filters.location.away;
    this.neutralGames = filters.location.neutral;
    if globals.allTrue(filters.location) {
      this.homeGames = false;
      this.awayGames = false;
      this.neutralGames = false;
    }

    // set outcome checkboxes
    this.wins = filters.outcome.wins;
    this.losses = filters.outcome.losses;
    if globals.allTrue(filters.outcome) {
      this.wins = false;
      this.losses = false;
    }

    // TODO: Overtime for games tab
    // // set overtime checkboxes
    // var otList = ['ot1','ot2','ot3','ot4','ot5','ot6'];
    // var anyTrue = [];
    // otList.forEach( (ot) => {
    //   this[ot] = filters.overtime[ot];
    //   anyTrue.push(filters.overtime[ot]);
    // });
    // this.otAll = false;
    // if (anyTrue.every(function(tf){return tf == true;})) this.otAll = true;
    //
    // this.otNone = false;
    // if (anyTrue.every(function(tf){return tf == false;})) this.otNone = true;
    //
    // this.onlyOT = filters.overtime.onlyQueryOT;

  }

  // For specifications see global.vars
  saveCurrentFilter(inputId, filterName, modalId) {
    // Get all currently set filters
    var filters = this.getAllFilters();
    globals.saveCurrentFilter(modalId, inputId, filterName, filters);
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
    globals.createSelect2("#teams-upOrDown", "Select", globals.getUpOrDown);
    globals.createSelect2("#teams_select-season", 'Ex. 17-18', this.getAvailableSeasons);

    // styling on select2s done here after initialization
    $(".select2-selection__rendered").css("overflow-x","scroll");
    $(".select2-selection.select2-selection--multiple").css("line-height","1em");
    $(".select2-selection.select2-selection--multiple").css("min-height","26px");

  }

}
