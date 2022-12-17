import { Component, OnInit, ViewChild } from '@angular/core';
import { max } from 'rxjs';
// Agent,
import { CorsMainService } from '../cors/cors-main.service';
import { EditComponent } from '../edit/edit.component';


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  constructor(private CorsMainService: CorsMainService) { }
  // perem ag
  ag_id: string | undefined;
  ag_title: string | undefined;
  ag_priority: string | undefined;
  ag_type: string | undefined;
  ag_address: string | undefined;
  ag_director: string | undefined;
  ag_email: string | undefined;
  ag_phone: string | undefined;
  ag_inn: string | undefined;
  ag_kpp: string | undefined;
  ag_image: string | undefined;
  // perem ag


  ag_edit(list: any) {
      this.ag_id = list.ag_id,
      this.ag_title = list.ag_title,
      this.ag_priority = list.ag_priority,
      this.ag_type = list.ag_type,
      this.ag_address = list.ag_address,
      this.ag_director = list.ag_director,
      this.ag_email = list.ag_email,
      this.ag_phone = list.ag_phone,
      this.ag_inn = list.ag_inn,
      this.ag_kpp = list.ag_kpp,
      this.ag_image = list.ag_logo_path
      this.modal_edit = true
  }

  // Модальные окна
  modal_create = false;
  modal_edit = false;
  // Модальные окна

  //ВЫВОД ДАННЫХ
  MainData: any;
  Types: any;
  selected_sort: string = "Без фильтра";
  filter_placeholder = "Название";
  strela_sorta = true;
  max_page: number = 2;
  //ВЫВОД ДАННЫХ

  // КОРС ПЕРЕМЕННЫЕ
  page: number = 1;
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
    this.CorsMainService.getTypes().subscribe((data) => {
      this.Types = data;
    });
  }

  getAgents() {
    this.CorsMainService.getAgent(String(this.page), this.type, this.search, this.order_by, this.order).subscribe((data) => {
      this.MainData = data;
      for (let i = 0; i < this.MainData.length; i++) {
        if (this.MainData[i].ag_logo_path == 'none' || this.MainData[i].ag_logo_path == 'отсутствует')
          this.MainData[i].ag_logo_path = "/agents/no_image.png";
      }
    }, (err) => {console.log(err)});
    this.CorsMainService.getMaxPage(this.type, this.search).subscribe((data) => {
      this.max_page = Number(data);
    })
  }
  getSearch() {
    //@ts-ignore
    let string: string | undefined = document.getElementById("search").value
    this.search = string;
    this.page = 1;
    if (string == "") {
      this.search = undefined;
    }
    this.getAgents();
  }
  getOrder_by(string: number) {
    switch (string) {
      case 1: {
        this.filter_placeholder = "Название"; break;
      }
      case 2: {
        this.filter_placeholder = "Приоритет"; break;
      }
      case 3: {
        this.filter_placeholder = "Скидка"; break;
      }
    }
    this.order_by = string;
    this.getAgents();
  }
  getSort(string: string) {
    this.selected_sort = string;
    this.page = 1;
    this.type = string
    if (string == "Без фильтра")
      this.type = undefined
    this.getAgents();
  }
  toggle_strela() {
    this.strela_sorta = !this.strela_sorta;
    this.order = this.strela_sorta;
    this.getAgents();
    document.getElementById('strelochka')?.classList.toggle('rotate');
  }
  paginator(page: number) {
    switch (page) {
      case 1: {
        if (this.page != 1) {
          this.page = 1;
          this.getAgents();
        }
        break;
      }
      case 2: {
        if (this.page > 1) {
          this.page = this.page - 1;
          this.getAgents();
        }
        break;
      }
      case 3: {
        if (this.page < this.max_page) {
          this.page = this.page + 1;
          this.getAgents();
        }
        break;
      }
      case 4: {
        // if (this.page <= this.max_page) {
        this.page = this.max_page;
        this.getAgents();
        // }
        break;
      }
    }
  }
  goto_func(event: any) {
    const value = Number(event.target.value)
    if (this.page > this.max_page) {
      this.page = this.max_page;
    }
    else this.page = value;
    setTimeout(() => {
      event.target.value = this.page;
    }, 1000);
    this.getAgents();
  }
  delete(id: string) {
    //@ts-ignore
    this.CorsMainService.deleteAg(id).subscribe((r) => {if (r.status_code == 202) alert(r.detail)},
     (err) => {alert(err)});
    this.getAgents();
  }
  logoFunc(logo: any) {
    console.log(logo)
  }
}
