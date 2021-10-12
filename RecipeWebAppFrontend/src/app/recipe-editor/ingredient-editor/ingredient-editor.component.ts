import { Component, ViewChild , OnInit, Input } from '@angular/core';
import {fromEvent } from 'rxjs';
import { filter, debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { IngredientEditorService } from './ingredient-editor.service';
import { RecipeEditorService } from '../recipe-editor.service';

@Component({
  selector: 'app-ingredient-editor',
  templateUrl: './ingredient-editor.component.html',
  providers: [IngredientEditorService],
  styleUrls: ['./ingredient-editor.component.css']
})
export class IngredientEditorComponent implements OnInit {
  @ViewChild('editor') editor;
  @ViewChild('editorStatus') editorStatus;
  @ViewChild('resultTable') resultTable;
  @ViewChild('searchTable') searchTable;
  @ViewChild('portionen') portionen;
  @Input('recipeLoad') recipeLoad;
 
  recentData = []
  lastIngridientText
  visibleFields = [
    "Energie (Kilokalorien) kcal",
    "Eiweiß (Protein) mg",
    "Fett mg",
    "Kohlenhydrate, resorbierbar mg"
  ]

 

  constructor(private ingredientEditorService: IngredientEditorService, 
              private recipeEditor: RecipeEditorService) {
    
  }

  ngOnInit(): void {}

  
  ngAfterViewInit() {
    var self = this

    this.ingredientEditorService.ingredientLoaded.pipe(
      filter(Boolean),
      debounceTime(100),
      distinctUntilChanged(),
      tap((e) => {
        //Loaded
        self.tableGeneratorSearch();
        self.tableGeneratorResults();
        self.editorStatus.nativeElement.classList.remove("is-loading")
      })
    ).subscribe();
    
    this.recipeEditor.recipeLoaded.subscribe({
      next: x => this.ingredientEditorService.buildDiff(x["body"]["ZUTATEN"]),
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification'),
    })
    
    
    // server-side search
    fromEvent(this.editor.nativeElement,'keyup')
        .pipe(
            filter(Boolean),
            debounceTime(250),
            distinctUntilChanged(),
            tap((e) => {
              this.editorStatus.nativeElement.classList.add("is-loading")
              //Process input
              var ele = <Event>e
              var target = <HTMLInputElement>ele.target
              //var text = target.innerText
              var text = target.value
              this.ingredientEditorService.buildDiff(text) 
            })
            
        ).subscribe();
        
    fromEvent(this.portionen.nativeElement,'change')
        .pipe(
            filter(Boolean),
            debounceTime(100),
            distinctUntilChanged(),
            tap((e) => {
              this.updatePerProtion()
            })
            
        )
        .subscribe();
  }

  getColorForPercentage(pct) {
    var percentColors = [
      { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
      { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
      { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } } ];
  
    
      for (var i = 1; i < percentColors.length - 1; i++) {
          if (pct < percentColors[i].pct) {
              break;
          }
      }
      var lower = percentColors[i - 1];
      var upper = percentColors[i];
      var range = upper.pct - lower.pct;
      var rangePct = (pct - lower.pct) / range;
      var pctLower = 1 - rangePct;
      var pctUpper = rangePct;
      var color = {
          r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
          g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
          b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
      };
      return 'rgb(' + [color.r, color.g, color.b].join(',') + ')';
      // or output as hex if preferred
  };

  
  tableGeneratorSearch() {
    var self = this;
    var searchTable = <HTMLTableElement>this.searchTable.nativeElement;

    //Cleanup Table
    while (searchTable.rows.length > 0) {
      searchTable.deleteRow(0);
    }

    var lines = this.editor.nativeElement.value.split('\n');

    //Create header:
    var tr = searchTable.insertRow();
    ["value", "unit", "valueD", "unitD", "ingredient", "original"].forEach(function(entry) {
      var td = tr.insertCell();
      td.appendChild(document.createTextNode(entry));
    });

    //Create Body
    self.ingredientEditorService.ingredientArray.forEach(function(line) {
      var entry = self.ingredientEditorService.ingredientsCached[line]
      
      if(entry && 0 in entry["data"]) {
        var tr = searchTable.insertRow();
        ["value", "unit", "valueD", "unitD", "ingredient", "original"].forEach(function(field) {
          var td = tr.insertCell();
          var text = entry["data"][0][field]
          if(entry["data"][0][field] == null) {
            text = "";
          };
          td.appendChild(document.createTextNode(text));
          td.style.border = '1px solid black';
          td.style.backgroundColor = self.getColorForPercentage(entry["data"][0]["confidence"]);
        });	
      }
    });
  }

  getSumDict() {
    var self = this;
    var data = []
    self.ingredientEditorService.ingredientArray.forEach(line => {
      if(line in self.ingredientEditorService.ingredientsCached) {
        data.push(self.ingredientEditorService.ingredientsCached[line]["data"][0])
      }
    })

    var sum_dict = new Object();
    data.forEach(function(entry) {
      var dict = new Object();
      if(entry && entry["data"] && 0 in entry["data"]) {
        for (const [key, value] of Object.entries(entry["data"])) {
          dict[key] = 0;
          if(value > 0) {
            dict[key] = Number(value)/100 * entry["value"];
          }
          if(sum_dict[key]) {
            sum_dict[key] += dict[key];
          } else {
            sum_dict[key] = dict[key];
          }
        };
        entry["calculated"] = dict;
      }
    });
    return sum_dict
  }

  tableGeneratorResults() {
    var resultTable = <HTMLTableElement>this.resultTable.nativeElement;

    //For each we calculated the correct value
    var sum_dict = this.getSumDict()
    //Cleanup Table
    while ( resultTable.rows.length > 0 ) {
      resultTable.deleteRow(0);
    }

    //Create header:
    var tr = resultTable.insertRow();
    var td = tr.insertCell();
    td.appendChild(document.createTextNode(""));
    for(const [key, value] of Object.entries(this.visibleFields)) {
      var td = tr.insertCell();
      td.appendChild(document.createTextNode(String(value).replace('/100g', '')));
    }
    
    //Row 1
    var tr = resultTable.insertRow();
    var td = tr.insertCell();
    td.appendChild(document.createTextNode("Summe"));
    for (const [key, value] of Object.entries(this.visibleFields)) {
      var td = tr.insertCell();
      td.appendChild(document.createTextNode((Math.round((sum_dict[key] + Number.EPSILON) * 100) / 100).toString()));
      td.style.border = '1px solid black';
    }

    this.updatePerProtion()
  }

  updatePerProtion() {
    var portion = this.portionen.nativeElement.value;
    var resultTable = <HTMLTableElement>this.resultTable.nativeElement;

    var sum_dict = this.getSumDict()
    while ( resultTable.rows.length > 2 ) {
      var rowCount = resultTable.rows.length;
      resultTable.deleteRow(rowCount-1);
    }
    //Row 2
    var tr = resultTable.insertRow();
    var td = tr.insertCell();
    td.appendChild(document.createTextNode("Pro Portion"));
    for (const [key, value] of Object.entries(this.visibleFields)) { //data["column_map"]
      var td = tr.insertCell();
      td.appendChild(document.createTextNode((Math.round((sum_dict[key]/portion + Number.EPSILON) * 100) / 100).toString()));
      td.style.border = '1px solid black';
    }
  }


  genIngredient() {
    var promise = this.recipeEditor.generateSuggestion(this.editor.nativeElement.value)

        promise.then(
          (val) => this.genIngredientSelect(val),
          (err) => this.recipeEditor.alertService.error('Error: '+err.status+' '+err.statusText)
        )
  }

  genIngredientSelect(iglist) {
    var newitem = iglist[Math.floor(Math.random() * iglist.length)]
    console.log(newitem)
    this.editor.nativeElement.value += "\n"+newitem
  }

}
