import { NgModule, Component, Input, OnInit, OnChanges, SimpleChanges, SimpleChange} from '@angular/core';
import { CommonModule } from '@angular/common';
import * as globals from './../global.vars';

import * as jquery from 'jquery';
window['$'] = jquery;
window['jQuery'] = jquery;

@Component({
  selector: 'stats-table',
  templateUrl: 'templates/stats.table.html'
})

export class StatsTableComponent {
  public readonly headers = ["Player", "MIN", "GP", "FGM", "FGA", "FG%", "3FGM", "3FGA","3PT%", "FTM", "FTA","FT%", "OREB","DREB","TREB","FOUL", "AST", "TO","BLK","STL", "PTS"];
  public readonly headers_adv = ["Player", "MIN", "GP", "FGM", "FGA", "FG%", "3FGM", "3FGA","3PT%", "FTM", "FTA","FT%", "OREB","DREB","TREB","FOUL", "AST", "TO","BLK","STL", "PTS"];

  //list of headers/columns to display in tables *** CHANGE DO GET LIST PASSED IN FROM DB ***
  keyHeaders = ["name","MIN","GAMES", "FG","FGA","FGPerc", "3PT", "FGA3", "FG3Perc", "FT", "FTA", "FTPerc", "OREB", "DREB", "REB", "PF", "AST","TO","BLK","STL", "PTS"];
  keyHeaders_adv = ["name","MIN","GAMES", "FG","FGA","FGPerc", "3PT", "FGA3", "FG3Perc", "FT", "FTA", "FTPerc", "OREB", "DREB", "REB", "PF", "AST","TO","BLK","STL", "PTS"];
  public init_data = [{'FT': 0, 'STL': 0, '3PT': 0, 'BLK': 0, 'FG': 0, 'REB': 0, 'DREB': 0, 'name': 'Player Name', 'AST': 0, 'OREB': 0, 'TO': 0, 'PF': 0, 'PTS': 0, 'jersey': '-'}];

  @Input() pageName:string;

  // Lists of players and columns/headers to be displayed
  public passed_in_headers = [];
  public passed_in_headers_adv = [];
  public playerList = [];
  public playerList_adv = globals.adv_data[this.pageName];

  @Input()
  set data(dataObj){
    this.passed_in_headers = this.keyHeaders;
    if (typeof(dataObj) === 'string') {
      var fixed_data = dataObj.replace(/'/g, '"');
      this.generatePlayerList(JSON.parse(fixed_data).data)
    }
  };

  public generatePlayerList(new_data) {
    /*
      Creates a list of teams/players to display
    */
    if (this.pageName == 'players') {
      var team_end = 'zzzz';

      // sort the data by player Name
      if (new_data != undefined) {
        var is_json = false;
        // see if the data includes json data
        for (let i in new_data){
          var player = new_data[i];
          if (player.name == player.team_id) continue;
          if (player.name.indexOf(',') == -1) is_json = true;
        }
        if (is_json) {
          for (let i in new_data){
            // put last name first and add a comma
            var player = new_data[i];
            if (player.name != player.team_id) {
              player.name = player.name.split(' ')[1] + ', ' + player.name.split(' ')[0];
            }
            // small hack to make the players still separated into teams
            if (player.name == player.team_id || player.name == player.team) {
              player.name = player.name + team_end;
            }
            else player.name = player.team + player.name;
          }
        }
        else {
          for (let i in new_data){
            var player = new_data[i]
            // small hack to make the players still separated into teams
            if (player.name == player.team_id || player.name == player.team) {
              player.name = player.name + team_end;
            }
            else player.name = player.team + player.name;
          }
        }
        // sort the data based on the players last name
        new_data = new_data.sort(function(a, b){
          var nameA=a.name.toLowerCase(), nameB=b.name.toLowerCase()
          if (nameA < nameB) //sort string ascending
              return -1
          if (nameA > nameB)
              return 1
          return 0 //default return value (no sorting)
        });

        for (let i in new_data){
          var player = new_data[i];
          if (player.team != undefined) player.name = player.name.slice(player.team.length);
          else player.name = player.name.slice(0,player.team_id.length);
        }
      }
    }
    this.playerList = new_data;
  }

  ngOnInit() {
    // remvoe the games played from the displayed data as it does not make sense in the teams tab
    if (this.pageName != 'players') {
      this.keyHeaders.splice(2,1);
      this.headers.splice(2,1);

      this.headers[0] = "Team";
    }
    this.generatePlayerList();
    $('.content-wrapper').scroll(function(){
      $('.col-0').css({ 'left': $(this).scrollLeft() });
    });
    // help with styling -- doesnt work yet
    // var maxNameWidth = Math.max.apply(Math, $('.col-0').map(function(){ return $(this).width(); }).get());
    // $('.col-1').css({ 'padding-left': maxNameWidth + 4 + 'px' });
    // $('.col-0').width(maxNameWidth);
  }
}



@NgModule({
   imports: [CommonModule],
   exports: [StatsTableComponent],
   declarations: [StatsTableComponent],
   providers: [],
})

export class StatsTableModule {
}
