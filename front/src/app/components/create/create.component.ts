import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CorsMainService } from '../cors/cors-main.service';

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

  constructor(private cors: CorsMainService) { }

  ngOnInit(): void {

  }

  errors: any;
  err_modal = false
  create_func(title: string, priority: string, type: string, address: string, director: string, email: string, phone: string, inn: string, kpp: string, logo: string) {
    if (!title || !priority ||
      !type ||
      !address || 
      !director ||
      !email ||
      !phone ||
      !inn ||
      !kpp ||
      !logo) {
        alert("ПОЖАЛУЙСТА ВВЕДИ ВСЁ РАДИ БОЖЕ");
        return;
      }
    this.cors.postCreate(title,
      priority, 
      type,
      address, 
      director, 
      email, 
      phone, 
      inn, 
      kpp, 
      logo).subscribe(() => 
      {return 1},
       (err) => {
         this.errors = err.error.detail;
         this.err_modal = true; 
        }
      )
    // this.cors.postCreate('title', '333', 'ООО', 'address', 'director', 'email', '11123456789', '1123456789', '123456789', '\agents\no_image.png').subscribe((b) => {return 1});
  }
}
