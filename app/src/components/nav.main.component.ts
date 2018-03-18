import { NgModule, Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from "@angular/common";

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
}

@NgModule({
   imports: [CommonModule],
   exports: [MainNavComponent],
   declarations: [MainNavComponent]
})

export class MainNavModule {
}
