import { NgModule, Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'stats-table',
  templateUrl: 'templates/table.players.html'
})

export class StatsTableComponent {
  public readonly header = 'h1';
  public readonly headers = ["Player","MIN","FG","3PT","FT","OREB","DREB","REB","AST","STL","BLK","TO","PF","PTS"];

}

@NgModule({
   imports: [CommonModule],
   exports: [StatsTableComponent],
   declarations: [StatsTableComponent],
   providers: [],
})

export class StatsTableModule {
}
