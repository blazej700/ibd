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
  img: any;
  currentOrder: Order;

  constructor(private backendApiService: BackendApiService,
    private dialog: MatDialog,
    private orderService: OrderService) { }

  ngOnInit(): void {
    this.backendApiService.getPhoto(this.tea).subscribe(res => {
      console.log(res);
      var arrayBufferView = new Uint8Array(res);
      var blob = new Blob([arrayBufferView], { type: "image/jpeg" });
      var urlCreator = window.URL || window.webkitURL;
      var imageUrl = urlCreator.createObjectURL(blob);
      const img = document.getElementById('img') as HTMLImageElement;
      img.src = imageUrl;
      this.img = imageUrl;
    });
    this.orderService.currentOrder.subscribe(value => this.currentOrder = value);

  }

  openDetailsDialog() {
    this.dialog.open(ProductDetailsComponent, {
      data: { tea: this.tea, img: this.img }
    });
  }

  addToOrder(teaId: number) {
    this.currentOrder.teas.push(teaId);
  }

}
