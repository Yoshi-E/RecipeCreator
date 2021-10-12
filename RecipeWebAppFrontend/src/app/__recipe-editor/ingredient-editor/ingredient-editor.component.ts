import { Component, ElementRef, AfterViewInit, ViewChild , OnInit } from '@angular/core';
import {fromEvent } from 'rxjs';
import { filter, debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
declare const myTest: any;

@Component({
  selector: 'app-ingredient-editor',
  templateUrl: './ingredient-editor.component.html',
  styleUrls: ['./ingredient-editor.component.css']
})
export class IngredientEditorComponent implements OnInit {
  @ViewChild('editor') editor;

  constructor() { }

  ngOnInit(): void {
  }

  ngAfterViewInit() {
    // server-side search
    fromEvent(this.editor.nativeElement,'keyup')
        .pipe(
            filter(Boolean),
            debounceTime(550),
            distinctUntilChanged(),
            tap((text) => {
              //Process input
              console.log(this.editor.nativeElement.innerHTML)
            })
        )
        .subscribe();
  }

  editor_onInput(e) {
    console.log(e);
    //TODO: Handel input
  }

}
