import { LoggedUser } from './../classes/logged-user';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { BackendApiService } from 'src/app/backend-api/backend-api.service';
import { Order } from './../classes/order';
import { OrderService } from './../services/order.service';
import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-new-order',
  templateUrl: './new-order.component.html',
  styleUrls: ['./new-order.component.css']
})
export class NewOrderComponent implements OnInit {

  currentOrder: Order;
  currentUser: LoggedUser;
  teas = [];
  orderDetailsFormGroup: FormGroup

  constructor(private orderService: OrderService,
    private backendApiService: BackendApiService,
    private router: Router,
    private userService: UserService,
    private formBuilder: FormBuilder) { }

  ngOnInit(): void {
    this.orderDetailsFormGroup = this.formBuilder.group({
      street: ['', [Validators.required]],
      city: ['', [Validators.required]],
      number: ['', [Validators.required]],
      postal_code: ['', [Validators.required]],
      details: ['', [Validators.required]],
    });
    this.orderService.currentOrder.subscribe(value => {
      this.currentOrder = value;
      this.currentOrder.teas.forEach(teaId => this.backendApiService.getTea(teaId).subscribe(res => this.teas.push(res)));
    });
    this.userService.currentUser.subscribe(value => this.currentUser = value);
  }

  orderPrice() {
    let sum = 0;
    this.teas.forEach(tea => sum += tea.price);
    return sum;
  }

  makeOrder() {
    this.currentOrder.address = {
      street: this.orderDetailsFormGroup.get('street').value,
      country: 'Polska',
      city: this.orderDetailsFormGroup.get('city').value,
      number: this.orderDetailsFormGroup.get('number').value,
      postal_code: this.orderDetailsFormGroup.get('postal_code').value
    };
    this.currentOrder.details = this.orderDetailsFormGroup.get('details').value;
    console.log(this.currentOrder);
    this.backendApiService.postOrder(this.currentOrder, this.currentUser).subscribe(res => {
      this.orderService.setOrder(new Order());
      this.backendApiService.getUser(this.currentUser.id).subscribe(value => this.currentUser.orders = value.orders);
      this.router.navigate(['/orders-list']);
    });
  }
}
