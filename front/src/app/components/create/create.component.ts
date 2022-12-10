import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.scss']
})
export class CreateComponent implements OnInit {

  @Output() close = new EventEmitter()

  constructor() { }

  ngOnInit(): void {
  }

}
