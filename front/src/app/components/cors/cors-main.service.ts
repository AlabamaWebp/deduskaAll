import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { observable, Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CorsMainService {
  constructor(private http: HttpClient) { }
  getAgent(page: string, 
    type?: string, 
    search?: string, 
    order_by?: number, 
    order?: boolean) 
    {
      const palk = "/"
      const vopr = "?" /// !!!!!!!!!!!!!! вставь его в код!!!!!!!!

      let tmpType = 'type='+type;
      let tmpSearch = "&search="+search;
      let tmpOrder_by = "&order_by=" + String(order_by);
      let tmpOrder = "&order=" + String(order);
      if (!type)
        tmpType = ""
      if (!search)
        tmpSearch = ""
      if (!order_by)
        tmpOrder_by = ""
      if (!order)
        tmpOrder = ""
      let tmpUrl = "http://26.246.185.101:8000/agents/"+page+palk+vopr+tmpType+tmpSearch+tmpOrder_by+tmpOrder;
      if (tmpType == "" && tmpSearch == "" && tmpOrder_by == "" && tmpOrder == "") {
        tmpUrl = "http://26.246.185.101:8000/agents/"+page+palk;
      }
      // while(tmpUrl.includes("//")) {
      tmpUrl = tmpUrl.replace("?&","?");
      // tmpUrl = tmpUrl.replace("//","/");
      console.log(tmpUrl)
      // }
      return this.http.get(tmpUrl);
  }
  getTypes() {
    return this.http.get("http://26.246.185.101:8000/agents/types/");
  }
}
export interface Agent {
  
}