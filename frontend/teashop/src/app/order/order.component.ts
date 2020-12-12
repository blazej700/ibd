import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { BackendApiService } from '../backend-api/backend-api.service';

@Component({
  selector: 'app-order',
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.css']
})
export class OrderComponent implements OnInit {

  order: any;
  teas = [];
  constructor(@Inject(MAT_DIALOG_DATA) public data,
    private backendApiService: BackendApiService) {
    this.order = data;
  }

  ngOnInit(): void {
    this.order.teas.forEach(tea => {
      this.backendApiService.getTea(tea.teaId)
      .subscribe(res => this.teas.push(res));
    });
  }

  orderPrice() {
    let sum = 0;
    this.teas.forEach(tea => sum += tea.price);
    return sum;
  }

}
