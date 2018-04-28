import { NgModule, Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from "@angular/common";
const {ipcRenderer} = require('electron');

import * as globals from './../global.vars';
const noUiSlider = require('nouislider/distribute/nouislider');
import * as jquery from 'jquery';
window['$'] = jquery;
window['jQuery'] = jquery;
import * as select2 from 'select2';

@Component({
  selector: 'main-nav',
  templateUrl: 'templates/nav.main.html'
})

export class MainNavComponent {
  @Output() pageChanged = new EventEmitter<string>();
  @Output() savedFilterChanged = new EventEmitter<string>();
  currentPage = "players";

  showSaveModal(){
    /*
      Show current page's save filter modal
    */
    var modalId = "#" + this.currentPage + "-save-filters-modal";
    $(modalId).modal('toggle');

  }

  ngOnInit(): void {
    select2();
    globals.createSelect2("#saved-filters", 'Select', globals.getSavedFilters);
    $('#saved-filters').on("change", (e) => {

      // if you select the null value, do nothing
      if (e.target.value == -1) return;

      // get the data from the saved filter object
      var filterData = $('#saved-filters').select2('data')[0].data;

      // send the data to the app component
      // to be able to pass it to the correct filter
      this.savedFilterChanged.emit(filterData);

      // change the currently selected to match selected saved filter
      this.currentPage = filterData.page;

    });
    $("#print-tooltip").tooltip();
    $("#saved-filters-wrapper").tooltip();
    $("#save-filter-tooltip").tooltip();

  }

  pageClicked(event){
    if (event.target.id == this.currentPage) return
    this.currentPage = event.target.id;
    this.pageChanged.emit(this.currentPage);
  }

  printMsg(event): void {
    console.log('Cornell Basketball Logo');
  }

  printPage(event) {
    ipcRenderer.send('print-to-pdf');
  }

  ipcRenderer.on('wrote-pdf', (event, path) => {
    const message = `Wrote PDF to: ${path}`;
    document.getElementById('content-teams').innerHTML = message;
  });

}

@NgModule({
   imports: [CommonModule],
   exports: [MainNavComponent],
   declarations: [MainNavComponent]
})

export class MainNavModule {
}
