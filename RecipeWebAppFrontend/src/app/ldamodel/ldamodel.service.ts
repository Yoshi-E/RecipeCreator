import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LDAModelService {

  constructor(private http: HttpClient) { }


  getLDAModels() {
    let promise = new Promise((resolve, reject) => {
      //let params = new HttpParams().set("id",id)
      this.http.get("/api/lda/models") //, {params: params})
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
