import { NgModule, Component, Input } from '@angular/core';
import { CommonModule } from "@angular/common";

@Component({
  selector: 'filter-teams',
  templateUrl: 'templates/filter.teams.html'
})
export class TeamsFilterComponent implements AfterViewInit {
  filters = {};
}
