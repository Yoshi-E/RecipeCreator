import { Injectable, Output, EventEmitter } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { AlertService } from '../_alert';
import { Title } from '@angular/platform-browser';

@Injectable({
  providedIn: 'root'
})
export class RecipeEditorService {
  @Output() recipeLoaded = new EventEmitter();

  apiUrl = '/api/editor/';
  recipeLoadRaw
  recipeLoad = {ingredients: "",
                title: "",
                description: "",
                meta: "<current user>"
  }
  options = {
    autoClose: true,
    keepAfterRouteChange: false
  }
  alertService: AlertService

  constructor(private http: HttpClient, 
              alertService: AlertService,
              private titleService: Title) {
    this.alertService = alertService
    this.titleService.setTitle("");
   }
  
  getRecipeFromID(id) {
    let promise = new Promise((resolve, reject) => {
      let params = new HttpParams().set("id",id)
      this.http.get(this.apiUrl+"recipe", {params: params})
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

  getRecipeImagesFromID(id) {
    let promise = new Promise((resolve, reject) => {
      let params = new HttpParams().set("id",id)
      this.http.get(this.apiUrl+"recipeImage", {params: params})
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

  loadRecipe(data) {
    
    this.recipeLoadRaw = data

    this.recipeLoad["ingredients"] = data["body"]["ZUTATEN"]
    this.recipeLoad["title"] = data["body"]["TITEL"]
    this.recipeLoad["description"] = data["body"]["ZUBEREITUNG"]
    this.recipeLoad["meta"] = "Foodstylist: "+data["head"]["FOODSTYLIST"]
    this.recipeLoad["dcid"] = data["head"]["DCID"]
    //Loaded event
    this.recipeLoaded.emit(data);
    this.titleService.setTitle(this.recipeLoad["title"]);
  }


  generateSuggestion(text) {
    var api = "/api/editor/prediction"

    let promise = new Promise((resolve, reject) => {
      let params = new HttpParams().set("text",text)
      this.http.get(api, {params: params})
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
}
