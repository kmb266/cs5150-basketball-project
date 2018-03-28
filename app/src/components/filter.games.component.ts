import { NgModule, Component, Input } from '@angular/core';
import { CommonModule } from "@angular/common";

@Component({
  selector: 'filter-games',
  templateUrl: 'templates/filter.games.html'
})
export class GamesFilterComponent implements AfterViewInit {
  filters = {};
}
