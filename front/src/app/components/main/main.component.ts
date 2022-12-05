import { Component, OnInit } from '@angular/core';
import { Agent, CorsMainService } from '../cors/cors-main.service';


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  constructor(private CorsMainService: CorsMainService) { }

  //ВЫВОД ДАННЫХ
  MainData: any;
  Types: any;
  selected_sort: string = "-";
  //ВЫВОД ДАННЫХ

  // КОРС ПЕРЕМЕННЫЕ
  page: string = "1"
  search: string | undefined;
  type: string | undefined;
  order_by: number | undefined;
  order: boolean | undefined;
  // КОРС ПЕРЕМЕННЫЕ

  ngOnInit(): void {
    this.getAgents();
    this.getTypes();
  }
  getTypes() {
    this.CorsMainService.getTypes().subscribe((data: Agent)=>{
      this.Types = data;
    });
  }
  
  getAgents() {
    this.CorsMainService.getAgent(this.page, this.type, this.search, this.order_by, this.order).subscribe((data: Agent)=>{
      this.MainData = data;
      // console.log(this.MainData)
    });
  }
  getSearch() {
    //@ts-ignore
    let string: string | undefined = document.getElementById("search").value
    this.search = string;
    if (string == "") {
      this.search = undefined;
    }
    this.getAgents();
  }
  getOrder_by(string: number) {
    this.order_by = string;
    this.getAgents();
  }
  getSort(string: string) {
    this.selected_sort = string;
    this.type = string
    if (string == "-")
    this.type = undefined
    this.getAgents();
  }
  
}
