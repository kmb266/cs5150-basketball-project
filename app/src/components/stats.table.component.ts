import { NgModule, Component, Input, OnInit, OnChanges, SimpleChanges, SimpleChange} from '@angular/core';
import { CommonModule } from '@angular/common';

import * as jquery from 'jquery';
window['$'] = jquery;
window['jQuery'] = jquery;

@Component({
  selector: 'stats-table',
  templateUrl: 'templates/stats.table.html'
})

export class StatsTableComponent {
  public readonly header = 'h1';
  public readonly headers = ["Player", "MIN", "FGM", "FGA", "FG%", "3FGM", "3FGA","3PT%", "FTM", "FTA","FT%", "OREB","DREB","TREB","FOUL", "AST", "TO","BLK","STL", "PTS"];

  //list of headers/columns to display in tables *** CHANGE DO GET LIST PASSED IN FROM DB ***
  keyHeaders = ["name","MIN","FG","FGA","FGPerc", "3PT", "FGA3", "FG3Perc", "FT", "FTA", "FTPerc", "OREB", "DREB", "REB", "PF", "AST","TO","BLK","STL", "PTS"];
  public init_data = [{'FT': 0, 'STL': 0, '3PT': 0, 'BLK': 0, 'FG': 0, 'REB': 0, 'DREB': 0, 'name': 'Player Name', 'AST': 0, 'OREB': 0, 'TO': 0, 'PF': 0, 'PTS': 0, 'jersey': '-'}];

  @Input() pageName:string;

  // Lists of players and columns/headers to be displayed
  public passed_in_headers = [];
  public playerList = [];

  @Input()
  set data(dataObj){
    this.passed_in_headers = this.keyHeaders;
    if (typeof(dataObj) === 'string') {
      var fixed_data = dataObj.replace(/'/g, '"');
      this.generatePlayerList(JSON.parse(fixed_data).data)
    }
  };

  // Creates the list of players/teams to display
  public generatePlayerList(new_data) {
    this.playerList = new_data;
  }

  ngOnInit() {
    this.generatePlayerList();
    $('.content-wrapper').scroll(function(){
      $('.col-0').css({ 'left': $(this).scrollLeft() });
    });
    // help with styling
    var maxNameWidth = Math.max.apply(Math, $('.col-0').map(function(){ return $(this).width(); }).get());
    $('.col-0').change(function() {
      console.log('changing')
    })
    $('.col-1').css({ 'padding-left': maxNameWidth + 4 + 'px' });
    $('.col-0').width(maxNameWidth);
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
