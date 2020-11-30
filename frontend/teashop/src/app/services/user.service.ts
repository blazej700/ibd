import { LoggedUser } from './../classes/logged-user';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private userSource = new BehaviorSubject<LoggedUser>(new LoggedUser());
  public currentUser = this.userSource.asObservable();

  constructor() { }

  setUser(user: LoggedUser) {
    this.userSource.next(user);
   }
}
