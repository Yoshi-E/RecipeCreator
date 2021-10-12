import { Injectable, Output, EventEmitter } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { RecipeEditorService } from '../recipe-editor.service';
import * as Diff from 'diff'

@Injectable({
  providedIn: 'root'
})
export class IngredientEditorService {
  @Output() ingredientLoaded = new EventEmitter();

  ingredientsCached = {} //TODO: Warning: Memory leak; Not cleared on update
  ingredientArray = []

  constructor(private http: HttpClient, 
              private recipeEditor: RecipeEditorService) { }

  getProcessedInput(text) {
    let promise = new Promise((resolve, reject) => {
      let params = new HttpParams().set("recipe_text",text)
      
      this.http.get(this.recipeEditor.apiUrl+"processIngredientInput", {params: params})
        .toPromise()
        .then(
          res => { // Success
            resolve(res) 
          },
          msg => { // Error
            reject(msg);
          }
        );
    });
    return promise;
  } 

  getLines(text) {
    var lines = text.split('\n');
    var linesArray = []
    lines.forEach(element => {
      linesArray.push(element.trim())
    })
    return linesArray
  }

  buildDiff(text: string) { //obj, funct, newS
    var self = this
    //this.ingredientArray = []
    var newSArray = this.getLines(text) //

    try {
      var diffObj = Diff.diffArrays(this.ingredientArray, newSArray)
    } catch (error) {
      console.error(error);
    }

    diffObj.forEach(diff => {
      if(diff["added"]) {
        diff["value"].forEach(line => {
          //New "line"
          if(!(line in this.ingredientsCached)) {
            this.processLine(line)
          }
        })
      }
    });
    this.ingredientArray = newSArray
    this.ingredientLoaded.emit("UPDATED")
  }

  processLine(line) {
    var promise = this.getProcessedInput(line) //lines[i]
    promise.then(
      (val) => this.updateIngredient(line, val), //
      (err) => this.recipeEditor.alertService.error('Error: '+err.status+' '+err.statusText)
    )
  }
  
  updateIngredient(line, data) {
    this.ingredientsCached[line] = data
    this.ingredientLoaded.emit(line);
  }
}
