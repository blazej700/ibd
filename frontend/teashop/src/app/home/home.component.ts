import { BackendApiService } from './../backend-api/backend-api.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  teas = [];

  constructor(private backendApiService: BackendApiService) { }

  ngOnInit(): void {
    this.backendApiService.getTeas(0, 100).subscribe(res => {
      this.teas = res.items;
    });
  }

  filterSelection(filters) {
    this.backendApiService.getTeas(0, 100, filters).subscribe(res => {
      this.teas = res.items;
    });
  }
}
