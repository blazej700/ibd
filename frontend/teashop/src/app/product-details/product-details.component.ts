import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { BackendApiService } from '../backend-api/backend-api.service';

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.css']
})
export class ProductDetailsComponent implements OnInit {

  tea: any;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any, private backendApiService: BackendApiService) {
    this.tea = data.tea;
    console.log(data);
  }

  ngOnInit(): void {
    const img = document.getElementById('img') as HTMLImageElement;
    img.src = this.data.img;
  }
  
  test() {

  }
}