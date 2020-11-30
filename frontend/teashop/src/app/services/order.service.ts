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

  setOrder(order: Order){
    this.orderSource.next(order);
  }
}
