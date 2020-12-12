import { EditProductComponent } from './edit-product/edit-product.component';
import { MatDialog } from '@angular/material/dialog';
import { BackendApiService } from 'src/app/backend-api/backend-api.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.css']
})
export class AdminPanelComponent implements OnInit {

  products = [];
  orders = [];
  productsResp = {
    perPage: 10,
    page: 1,
    pages: 1,
  }
  ordersResp = {
    perPage: 10,
    page: 1,
    pages: 1,
  }

  constructor(private backendApiService: BackendApiService,
    private matDialog: MatDialog) { }

  ngOnInit(): void {
    this.getProducts();
    this.getOrders();
  }

  getProducts() {
    this.backendApiService.getTeas(this.productsResp.page, this.productsResp.perPage).subscribe(value => {
      this.products = value.items;
      this.productsResp = value;
    });
  }

  getOrders(){
    this.backendApiService.getOrders(this.ordersResp.page, this.ordersResp.perPage).subscribe(value => {
      this.orders = value.items;
      this.ordersResp = value;
      console.log(value);
    });

  }

  editProduct(product) {
    this.matDialog.open(EditProductComponent, {
      data: product,
      width: '42%',
      height: '50%'
    }).afterClosed().subscribe(() => {
      this.getProducts();
    });;
  }

  addProduct() {
    this.matDialog.open(EditProductComponent, {
      data: undefined,
      width: '42%',
      height: '50%'
    }).afterClosed().subscribe(() => {
      this.getProducts();
    });
  }

  deleteProduct(product) {
    this.backendApiService.deleteTea(product.id).subscribe(() => {
      this.getProducts();
    })
  }

  changeStatus(order) {
    let input = <HTMLInputElement>document.getElementById('status');
    if (input.value != '0') {
      order.status = input.value;
      this.backendApiService.putOrder(order).subscribe(res => {
        this.getOrders();
      });
    }
    // order = {
    //   address: {
    //     city: "a",
    //     country: "Polska",
    //     id: 8,
    //     number: "a",
    //     postal_code: "a",
    //     street: "a",
    //   },
    //   details: "",
    //   id: 1,
    //   orderedBy: 5,
    //   ordered_teas: [{ id: 17, quantity: 1, teaId: 1 }, { id: 18, quantity: 1, teaId: 5 }],
    //   status: 1,
    // }

  }
}
