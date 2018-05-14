import { NgModule, Component, Input, OnInit, OnChanges, SimpleChanges, SimpleChange} from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'stats-table',
  templateUrl: 'templates/stats.table.html'
})

export class StatsTableComponent {
  public readonly header = 'h1';
  public readonly headers = ["Player", "FGM", "FGA", "3FGM", "3FGA", "FTM", "FTA", "OREB","DREB","TREB","FOUL", "AST", "TO","BLK","STL", "MIN","PTS", "FG%","3PT%","FT%"];

  //list of headers/columns to display in tables *** CHANGE DO GET LIST PASSED IN FROM DB ***
  keyHeaders = ["name","FG","FGA", "3PT", "FGA3", "FT", "FTA", "OREB","DREB","REB", "PF", "AST","TO","BLK","STL", "MIN", "PTS", "FGPerc", "FG3Perc", "FTPerc"];
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
