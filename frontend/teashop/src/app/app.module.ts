import { MatIconModule } from '@angular/material/icon';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RegisterComponent } from './register/register.component';
import { OrderComponent } from './order/order.component';
import { HomeComponent } from './home/home.component';
import { SideBarComponent } from './home/side-bar/side-bar.component';
import { ProductComponent } from './home/product/product.component';
import { ProductDetailsComponent } from './product-details/product-details.component';
import { LoginComponent } from './login/login.component';
import { OrdersListComponent } from './orders-list/orders-list.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    RegisterComponent,
    OrderComponent,
    HomeComponent,
    SideBarComponent,
    ProductComponent,
    ProductDetailsComponent,
    LoginComponent,
    OrdersListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatIconModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
