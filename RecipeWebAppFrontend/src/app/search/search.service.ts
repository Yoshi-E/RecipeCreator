import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(private http: HttpClient) { }

  configUrl = 'api/editor/searchIngredient/';

  searchIngredient(word) {
    let promise = new Promise((resolve, reject) => {
      this.http.get(this.configUrl+word)
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
