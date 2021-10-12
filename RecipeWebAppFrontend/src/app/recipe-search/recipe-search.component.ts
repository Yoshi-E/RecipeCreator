import { Component, OnInit, ViewChild } from '@angular/core';
import { RecipeSearchService } from './recipe-search.service';
import {fromEvent } from 'rxjs';
import { filter, debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';

@Component({
  selector: 'app-recipe-search',
  templateUrl: './recipe-search.component.html',
  styleUrls: ['./recipe-search.component.css']
})
export class RecipeSearchComponent implements OnInit {

  @ViewChild('search') search;
  @ViewChild('searchTable') searchTable;

  searchResults = [ ]
  constructor(private searchService: RecipeSearchService) { }

  ngOnInit(): void {

  }

  ngAfterViewInit() { 
    // server-side search
    fromEvent(this.search.nativeElement,'keyup')
        .pipe(
            filter(Boolean),
            debounceTime(500),
            distinctUntilChanged(),
            tap((text) => {
              //Process input
              var promise = this.searchService.searchRecipe(this.search.nativeElement.value)
              
              promise.then(
                (val) => this.showSearchResults(val),
                (err) => console.error(err)
              )
            })
        )
        .subscribe();
  }

  showSearchResults(data) {
    this.searchResults = data
  }

}