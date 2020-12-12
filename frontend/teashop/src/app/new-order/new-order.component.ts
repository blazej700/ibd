import { LoggedUser } from './../classes/logged-user';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { BackendApiService } from 'src/app/backend-api/backend-api.service';
import { Order } from './../classes/order';
import { OrderService } from './../services/order.service';
import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { identifierModuleUrl } from '@angular/compiler';

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
    private formBuilder: FormBuilder,
    private infoSnackBar: MatSnackBar) { }

  ngOnInit(): void {
    this.orderDetailsFormGroup = this.formBuilder.group({
      street: ['', [Validators.required]],
      city: ['', [Validators.required]],
      number: ['', [Validators.required]],
      postal_code: ['', [Validators.required]],
      details: [''],
    });
    this.orderService.getOrder().subscribe(value => {
      this.currentOrder = value;
      this.currentOrder.teas.forEach(tea => this.backendApiService.getTea(tea.teaId).subscribe(res => this.teas.push(res)));
    });
    this.userService.getUser().subscribe(value => this.currentUser = value);
  }

  orderPrice() {
    let sum = 0;
    this.teas.forEach(tea => {
      sum += tea.price * this.currentOrder.teas.find(el => el.id = tea.id).quantity;
    });
    return sum;
  }

  makeOrder() {
    if (!this.orderDetailsFormGroup.valid) {
      this.infoSnackBar.open('Uzupełnij wszystkie wymagane pola', '', {
        duration: 8000,
      });
      
      return;
    }
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

  quantityChanged(index: number, value: number) {
    this.currentOrder.teas[index].quantity = value;
    if (this.currentOrder.teas[index].quantity == 0) {
      this.currentOrder.teas.splice(index, 1);
      this.teas.splice(index, 1);
    }
    localStorage.setItem('currentOrder', JSON.stringify(this.currentOrder));
  }
}
