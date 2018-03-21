import { NgModule, Component, Input } from '@angular/core';
import { CommonModule } from "@angular/common";

@Component({
  selector: 'filter-players',
  templateUrl: 'templates/filter.players.html'
})
export class PlayersFilterComponent implements AfterViewInit {
  filters = {};
}
