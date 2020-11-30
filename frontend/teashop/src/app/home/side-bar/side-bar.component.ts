import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.css']
})
export class SideBarComponent implements OnInit {

  @Output() selectionChange = new EventEmitter<any>();
  filterFormGroup: FormGroup;

  constructor(private formBuilder: FormBuilder,) { }

  ngOnInit(): void {
    this.filterFormGroup = this.formBuilder.group({
      teaType: ['', [Validators.required]],
      country: ['', [Validators.required]],
      minPrice: [null, [Validators.required]],
      maxPrice: [null, [Validators.required]],
    });
  }

  emitSelection() {
    this.selectionChange.emit(this.filterFormGroup.value);
  }
}
