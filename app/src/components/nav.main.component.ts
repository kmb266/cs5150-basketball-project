import { NgModule, Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from "@angular/common";
const {ipcRenderer} = require('electron');
const noUiSlider = require('nouislider/distribute/nouislider');

@Component({
  selector: 'main-nav',
  templateUrl: 'templates/nav.main.html'
})

export class MainNavComponent {
  @Output() pageChanged = new EventEmitter<string>();
  currentPage = "players";

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
  })

  // var slider = document.getElementById('slider');
  // console.log(slider);
  // noUiSlider.create(slider, {
  // 	start: [20, 80],
  // 	connect: true,
  // 	range: {
  // 		'min': 0,
  // 		'max': 100
  // 	}
  // });
}

@NgModule({
   imports: [CommonModule],
   exports: [MainNavComponent],
   declarations: [MainNavComponent]
})

export class MainNavModule {
}
