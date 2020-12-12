import { OrderService } from './../services/order.service';
import { UserService } from './../services/user.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { BackendApiService } from '../backend-api/backend-api.service';
import { LoggedUser } from '../classes/logged-user';
import { Order } from '../classes/order';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginFormGroup: FormGroup;

  constructor(private formBuilder: FormBuilder,
    private backendApiService: BackendApiService,
    private router: Router,
    private infoSnackBar: MatSnackBar,
    private userService: UserService,
    private orderService: OrderService) { }

  ngOnInit(): void {
    this.loginFormGroup = this.formBuilder.group({
      login: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  get login() {
    return this.loginFormGroup.get('login');
  }

  get password() {
    return this.loginFormGroup.get('password');
  }

  submitLogin(): void {
    this.backendApiService.postLogin(this.login.value, this.password.value).subscribe(res => {
      this.backendApiService.key = res.key;
      localStorage.setItem('key', JSON.stringify(res.key));
      this.backendApiService.getUser(res.userId).subscribe(r => {
        const newUser = new LoggedUser();
        newUser.id = r.id,
          newUser.default_address = r.default_address,
          newUser.user_type = r.user_type,
          newUser.password = r.password,
          newUser.email = r.email,
          newUser.login = r.login;
        newUser.orders = r.orders;
        this.userService.setUser(newUser);
        this.orderService.setOrder(new Order());
        this.infoSnackBar.open('Zalogowoano ' + newUser.login, '', {
          duration: 5000,
        });
        this.router.navigate(['']);
      });
    }, error => {
      console.error(error);
      this.infoSnackBar.open('Błąd logowania', '', {
        duration: 5000,
      });
    });
  }
}