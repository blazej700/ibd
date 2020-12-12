import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Order } from '../classes/order';

@Injectable({
  providedIn: 'root'
})
export class OrderService {

  private orderSource = new BehaviorSubject<Order>(new Order());
  public currentOrder = this.orderSource.asObservable();

  constructor() { }

  setOrder(order: Order) {
    localStorage.setItem('currentOrder', JSON.stringify(order));
    this.orderSource.next(order);
  }

  getOrder() {
    if (this.orderSource.getValue().teas.length === 0) {
      const order: Order = JSON.parse(localStorage.getItem('currentOrder'));
      if (order) {
        this.orderSource.next(order);
      } else {
        this.orderSource.next(new Order());
      }
    }
    return this.currentOrder;
  }
}
