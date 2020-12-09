import { OrderService } from './../services/order.service';
import { LoggedUser } from './../classes/logged-user';
import { UserService } from './../services/user.service';
import { BackendApiService } from './../backend-api/backend-api.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { Order } from '../classes/order';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  currentUser: any;
  currentOrder: Order;

  constructor(private backendApiService: BackendApiService,
    private userService: UserService,
    private router: Router,
    private infoSnackBar: MatSnackBar,
    private dialog: MatDialog,
    private orderService: OrderService) { }

  ngOnInit(): void {
    this.userService.currentUser.subscribe(value => this.currentUser = value);
    this.orderService.currentOrder.subscribe(value => this.currentOrder = value);
  }

  loggedUserTagClicked() {
    if (this.currentUser.id) {
      if (this.currentUser.user_type === 1) {
        this.router.navigate(['/admin-panel']);
      } else {
        this.router.navigate(['/orders-list']);
      }
    } else {
      this.router.navigate(['/login']);
    }
  }

  logout() {
    this.backendApiService.key = undefined;
    this.userService.setUser(new LoggedUser());
    this.infoSnackBar.open('Wylogowano pomyslnie', '', {
      duration: 5000,
    });
    this.router.navigate(['/login']);
  }
}
