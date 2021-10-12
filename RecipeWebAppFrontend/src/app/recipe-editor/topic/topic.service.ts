import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TopicService {
  apiUrl = '/api/editor/';

  constructor(private http: HttpClient) { }


  getRecipeTopicFromID(id) {
    let promise = new Promise((resolve, reject) => {
      let params = new HttpParams().set("id",id)
      this.http.get(this.apiUrl+"topicRaw", {params: params})
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
  
  getRecipeTopicFromText(text) {
    let promise = new Promise((resolve, reject) => {
      let params = new HttpParams().set("text",text)
      this.http.get(this.apiUrl+"topicRaw", {params: params})
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

  getRecipesFromTopic(id) {
    let promise = new Promise((resolve, reject) => {
      let params = new HttpParams().set("id",id)
      this.http.get(this.apiUrl+"topicRecipes", {params: params})
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
