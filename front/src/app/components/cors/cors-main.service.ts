import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { observable, Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CorsMainService {
  constructor(private http: HttpClient) { }
  url: string = "http://26.246.185.101:8000/";
  // url: string = "http://127.0.0.1:8000/";
  getAgent(page: string, 
    type?: string, 
    search?: string, 
    order_by?: number, 
    order?: boolean) 
    {
      const palk = "/"
      const vopr = "?" 

      let tmpType = 'type_='+type;
      let tmpSearch = "&search="+search;
      let tmpOrder_by = "&order_by=" + String(order_by);
      let tmpOrder = "&order=" + String(order);
      if (!type)
        tmpType = ""
      if (!search)
        tmpSearch = ""
      if (!order_by)
        tmpOrder_by = ""
      if (order == undefined)
        tmpOrder = ""
      let tmpUrl = this.url + "agent/"+page+palk+vopr+tmpType+tmpSearch+tmpOrder_by+tmpOrder;
      if (tmpType == "" && tmpSearch == "" && tmpOrder_by == "" && tmpOrder == "") {
        tmpUrl = this.url + "agent/"+page+palk;
      }
      tmpUrl = tmpUrl.replace("?&","?");
      console.log(tmpUrl)
      return this.http.get(tmpUrl);
  }
  getTypes() {
    return this.http.get(this.url + "agent/types/");
  }
  getMaxPage(type?: string, search?: string) {
    let tmpType = 'type_='+type;
    let tmpSearch = "&search="+search;
    if (!type)
      tmpType = ""
    if (!search)
      tmpSearch = ""
    if (tmpSearch == "" && tmpType == "")
      return this.http.get(this.url + "agent/pages/");
    else {
      let tmpUrl = this.url + "agent/pages/?"+tmpType+tmpSearch;
      tmpUrl = tmpUrl.replace("?&","?");
      return this.http.get(tmpUrl);
    }
  }
}
// export interface Agent {
  
// }