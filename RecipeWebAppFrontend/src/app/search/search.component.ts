import { Component, OnInit, ViewChild } from '@angular/core';
import { SearchService } from './search.service';
import {fromEvent } from 'rxjs';
import { filter, debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  providers: [ SearchService ],
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  @ViewChild('search') search;
  @ViewChild('searchTable') searchTable;

  constructor(private searchService: SearchService) { }

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
              var promise = this.searchService.searchIngredient(this.search.nativeElement.value)
              
              promise.then(
                (val) => this.showSearchResults(val),
                (err) => console.error(err)
              )
              /*.subscribe(
                data => this.showSearchResults(data)
              );*/
            })
        )
        .subscribe();
  }

  showSearchResults(data) {
    console.log(data);
    const tbl = this.searchTable.nativeElement
    while ( tbl.rows.length > 0 ) {
      tbl.deleteRow(0);
    }

    if (data["response"] !== null) {
      var tr = tbl.insertRow();
      data["fields"].forEach(function(entry) {
        var td = tr.insertCell();
        td.appendChild(document.createTextNode(data["column_map"][entry]));
      });
  
      data["data"].forEach(function(entry) {
        var tr = tbl.insertRow();
        data["fields"].forEach(function(field) {
          var td = tr.insertCell();
          td.appendChild(document.createTextNode(entry[field]));
          td.style.border = '1px solid black';
        });	
      });
    }
  }

}
