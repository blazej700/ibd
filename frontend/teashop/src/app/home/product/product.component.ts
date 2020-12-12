import { LoggedUser } from './../../classes/logged-user';
import { UserService } from './../../services/user.service';
import { OrderService } from './../../services/order.service';
import { ProductDetailsComponent } from './../../product-details/product-details.component';
import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { BackendApiService } from 'src/app/backend-api/backend-api.service';
import { Order } from 'src/app/classes/order';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {

  @Input() tea: any;
  @Input() index: any;
  img: any;
  currentOrder: Order;
  currentUser: LoggedUser;

  constructor(private backendApiService: BackendApiService,
    private dialog: MatDialog,
    private userService: UserService,
    private orderService: OrderService) { }

  ngOnInit(): void {
    this.backendApiService.getPhoto(this.tea).subscribe(res => {
      var arrayBufferView = new Uint8Array(res);
      var blob = new Blob([arrayBufferView], { type: "image/jpeg" });
      var urlCreator = window.URL || window.webkitURL;
      var imageUrl = urlCreator.createObjectURL(blob);
      const img = document.getElementById('img' + this.index) as HTMLImageElement;
      img.src = imageUrl;
      this.img = imageUrl;
    });
    this.userService.getUser().subscribe(value => {
      this.currentUser = value;
      if (this.currentUser.id) {
        this.orderService.getOrder().subscribe(v => this.currentOrder = v);
      }
    });
  }

  openDetailsDialog() {
    this.dialog.open(ProductDetailsComponent, {
      data: { tea: this.tea, img: this.img }
    });
  }

  addToOrder(teaId: number) {
    const tea = this.currentOrder.teas.find(el => el.teaId === teaId);
    if (tea) {
      tea.quantity++;
    } else {
      this.currentOrder.teas.push({ teaId: teaId, quantity: 1 });
    }
    localStorage.setItem('currentOrder', JSON.stringify(this.currentOrder));
  }

}
