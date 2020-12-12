import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { BackendApiService } from 'src/app/backend-api/backend-api.service';

@Component({
  selector: 'app-edit-product',
  templateUrl: './edit-product.component.html',
  styleUrls: ['./edit-product.component.css']
})
export class EditProductComponent implements OnInit {

  product: any;
  img: any;

  formGroup: FormGroup;

  constructor(@Inject(MAT_DIALOG_DATA) public data,
    private matDialogRef: MatDialogRef<EditProductComponent>,
    private backendApiService: BackendApiService,
    private formBuilder: FormBuilder) {
    this.product = data;
  }

  ngOnInit(): void {
    this.formGroup = this.formBuilder.group({
      name: ['', Validators.required],
      country: ['', Validators.required],
      teaType: ['', Validators.required],
      stock: ['', Validators.required],
      price: ['', Validators.required],
      descryption: ['']
    });
    if (this.product) {
      this.backendApiService.getPhoto(this.product).subscribe(res => {
        var arrayBufferView = new Uint8Array(res);
        var blob = new Blob([arrayBufferView], { type: "image/jpeg" });
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL(blob);
        const img = document.getElementById('img') as HTMLImageElement;
        img.src = imageUrl;
        this.img = imageUrl;
      });

      this.formGroup = this.formBuilder.group({
        name: [this.product.name, Validators.required],
        country: [this.product.country, Validators.required],
        teaType: [this.product.tea_type, Validators.required],
        stock: [this.product.stock, Validators.required],
        price: [this.product.price, Validators.required],
        descryption: ['']
      });
    }
  }

  Save() {
    if (this.product) {
      this.backendApiService.putTea(this.product.id, this.formGroup.value).subscribe(res => this.matDialogRef.close())
    } else {
      this.backendApiService.postTea(this.formGroup.value).subscribe(res => this.matDialogRef.close())
    }
  }
}
