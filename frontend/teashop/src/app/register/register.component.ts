import { BackendApiService } from './../backend-api/backend-api.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  userFormGroup: FormGroup;

  constructor(private formBuilder: FormBuilder,
              private backendApiService: BackendApiService,
              private router: Router,
              private infoSnackBar: MatSnackBar) { }

  ngOnInit(): void {
    this.userFormGroup = this.formBuilder.group({
      login: ['', [Validators.required]],
      email: ['', [Validators.required]],
      password: ['', [Validators.required]],
      passwordConfirmed: ['', [Validators.required]],
      accept: [false, [Validators.required]],
    });
  }

  submitUser(): void {
    if(this.userFormGroup.get('accept').value){
      this.backendApiService.postUser(this.userFormGroup.value).subscribe(res => {
        this.router.navigate(['/login']);
        this.infoSnackBar.open('Utworzono nowego użytkownika', '', {
          duration: 5000,
        });
      }, error => {
        console.error(error);
        this.infoSnackBar.open('Błąd przy tworzeniu użytkownika', '', {
          duration: 5000,
        });
      });
    } else {
      this.infoSnackBar.open('Zaakceptuj regulamin sklepu', '', {
        duration: 5000,
      });
    }
  }

}
