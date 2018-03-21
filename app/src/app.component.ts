import { NgModule, Component, OnInit } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FiltersModule } from './components/filters.module';
import { StatsTableModule } from './components/stats.table.component';
import { MainNavModule } from './components/nav.main.component';
import * as globals from './global.vars';

@Component({
  selector: 'App',
  templateUrl:'templates/app.html',
  host: {
    '(window:resize)': 'onResize($event)'
  }
})
export class AppComponent implements OnInit {
  public readonly title = 'Cornell Basketball Stats';

  currentPage = "players";
  contentHeight = window.innerHeight - globals.navHeight;
  ngOnInit(): void {
    console.log('component initialized');
  }

  onResize(event) {
    this.contentHeight = window.innerHeight - globals.navHeight;
  }

  pageChanged(event) {
    this.currentPage = event;
    console.log(event);
  }

}

@NgModule({
  imports: [BrowserModule, StatsTableModule, FiltersModule, MainNavModule],
  declarations: [AppComponent],
  bootstrap: [AppComponent]
})
export class AppModule {}
