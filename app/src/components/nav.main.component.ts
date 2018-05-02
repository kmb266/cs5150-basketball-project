import { NgModule, Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from "@angular/common";
const {ipcRenderer} = require('electron');
const fs = require('fs');

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
  savedFiltersFromFile = this.getSavedFilters();

  getSavedFilters() {
    /*
      return the saved filters from the file
      minus the default filters
    */
    var filtersFromFile = globals.getSavedFilters();
    return filtersFromFile.slice(1);
  }

  showSaveModal(){
    /*
      Show current page's save filter modal
    */
    var modalId = "#" + this.currentPage + "-save-filters-modal";
    $(modalId).modal('toggle');

  }

  showEditSavedFiltersModal(modal) {
    /*
      Shows the edit filters modal
    */
    $(modal).modal('toggle');
    this.savedFiltersFromFile = this.getSavedFilters();

  }
  jsonStringify(data) {
    /*
      Returns stringified data
      Inputs:
        data: obj = filter object data
    */
    return JSON.stringify(data);
  }
  saveFilterChanges(modal) {
    /*
      Saves the changed filters in edit saved filter modal
    */
    var new_filters = "";
    $('.input-filter-names').each(function(){
      if ($(this).data('include')) {
        new_filters += JSON.stringify($(this).data('filter')) + '\n';
      }
    });
    console.log(new_filters);
    // not checking for duplicates, if they want to make a filter the same name
    // we are going to let them do it here..
    fs.writeFile(globals.saved_filters_file, new_filters, function (err) {
      if (err) throw err;
      $(modal).modal('toggle');

      // refresh the saved filters dropdown
      $('#saved-filters').empty();
      globals.createSelect2("#saved-filters", 'Select Saved Filter', globals.getSavedFilters);

      console.log('Saved!');

    });

  }

  deleteFilter(event, index) {
    /*
      delete selected filter
    */
    var isDisabled = $('#filter-names-'+index).prop('disabled');
    $('#filter-names-'+index).prop('disabled', !isDisabled);
    $('#filter-names-'+index).attr('data-include', isDisabled);
    $('#btn-filter-'+index).toggle();
    $('#btn-filter-undo-'+index).toggle();

  }


  ngOnInit(): void {

    // get filter names and data and add them to savedFiltersFromFile

    select2();
    globals.createSelect2("#saved-filters", 'Select Saved Filter', globals.getSavedFilters);
    $('#saved-filters').on("change", (e) => {
      console.log(e.target.value);
      // if you select the null value, do nothing
      if (e.target.value == -1 || e.target.value == '') return;

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
    $(".nav-tooltip").tooltip();

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
