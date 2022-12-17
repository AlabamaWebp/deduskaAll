import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { CorsMainService } from '../cors/cors-main.service';

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.scss']
})
export class EditComponent implements OnInit {

  constructor(private cors: CorsMainService) { }
  @Output() close = new EventEmitter()
  @Output() reload = new EventEmitter()
  @Input() ag_id: string | undefined;
  @Input() ag_title: string | undefined;
  @Input() ag_priority: string | undefined;
  @Input() ag_type: string | undefined;
  @Input() ag_address: string | undefined;
  @Input() ag_director: string | undefined;
  @Input() ag_email: string | undefined;
  @Input() ag_phone: string | undefined;
  @Input() ag_inn: string | undefined;
  @Input() ag_kpp: string | undefined;
  @Input() ag_logo: string | undefined;

  ngOnInit(): void {
  }
  errors: any;
  err_modal = false
  edit_func(title: string, priority: string, type: string, address: string, director: string, email: string, phone: string, inn: string, kpp: string, logo: string) {
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
    this.cors.putEdit(
      Number(this.ag_id),
      title,
      Number(priority),
      type,
      address,
      director,
      email,
      Number(phone),
      Number(inn),
      Number(kpp),
      logo).subscribe(() => {
        this.reload.emit();
        document.getElementsByClassName("uspeh")[0].classList.add("anUs");
        setTimeout(() => {
          document.getElementsByClassName("uspeh")[0].classList.remove("anUs");
        }, 500);
        return;
      },
        (err) => {
          this.errors = err.error.detail;
          this.err_modal = true;
        }
      )
  }
}
