import { Component, OnInit } from '@angular/core';
// Agent,
import { CorsMainService } from '../cors/cors-main.service';


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  constructor(private CorsMainService: CorsMainService) { }
  // Модальные окна
  modal_create = false;
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
    });
    this.CorsMainService.getMaxPage(this.type, this.search).subscribe((data) => {
      this.max_page = Number(data);
    })
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
    this.CorsMainService.deleteAg(id).subscribe(() => {});
    this.getAgents();
  }
}
