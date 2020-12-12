import { OrderComponent } from './../order/order.component';
import { MatDialog } from '@angular/material/dialog';
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
  teas = [];

  constructor(private backendApiService: BackendApiService,
    private matDialog: MatDialog,
    private userService: UserService,) { }

  ngOnInit(): void {
    this.backendApiService.getTeas(0,100).subscribe(res => this.teas = res.items);
    this.userService.getUser().subscribe(value => {
      this.currentUser = value;
      this.backendApiService.getOrders( 0, 5, this.currentUser.id).subscribe(res => {
        console.log(res);
        this.orders = res.items;
      });
    });
  }

  test() {
  }

  getOrderCost(order) {
    let sum = 0;
    console.log(order);
    order.ordered_teas.forEach(element => {
      sum += this.teas.find(tea => tea.id = element.id).price * element.quantity;
    });
    return sum;
  }

  openDetails(order) {
    this.matDialog.open(OrderComponent, {
      data: order,
      width: '80%',
      height: '80%',
    });
  }
}
