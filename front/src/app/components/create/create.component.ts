import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.scss']
})
export class CreateComponent implements OnInit {

  @Output() close = new EventEmitter()
  ag_title: string | undefined;
  ag_priority: string | undefined;
  ag_type: string | undefined;
  ag_address: string | undefined;
  ag_director: string | undefined;
  ag_email: string | undefined;
  ag_phone: string | undefined;
  ag_inn: string | undefined;
  ag_kpp: string | undefined;
  ag_logo_path: string | undefined;

  constructor() { }

  ngOnInit(): void {

  }

  create_func(title: string, priority: string, type: string, address: string, director: string, email: string, phone: string, inn: string, kpp: string, logo: string) {
    
  }
}
