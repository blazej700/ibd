import { LoggedUser } from './../classes/logged-user';
import { UserService } from './../services/user.service';
import { Component, OnInit } from '@angular/core';
import { BackendApiService } from '../backend-api/backend-api.service';

@Component({
  selector: 'app-orders-list',
  templateUrl: './orders-list.component.html',
  styleUrls: ['./orders-list.component.css']
})
export class OrdersListComponent implements OnInit {

  currentUser: LoggedUser;
  orders = [];
  constructor(private backendApiService: BackendApiService,
    private userService: UserService,) { }

  ngOnInit(): void {
    this.userService.currentUser.subscribe(value => this.currentUser = value);
    this.currentUser.orders.forEach(orderId => {
      this.backendApiService.getOrder(orderId).subscribe(res => this.orders.push(res));
    });
  }

  test() {
    console.log(this.orders);
  }

  getOrderCost(order) {
    let sum = 0;
    order.teas.forEach(element => {
      sum += element.price;
    });
    return sum;
  }
}
