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
    localStorage.setItem('currentUser', JSON.stringify(user));
    this.userSource.next(user);
  }

  getUser() {
    if (!this.userSource.getValue().id) {
      const user: LoggedUser = JSON.parse(localStorage.getItem('currentUser'));
      if (user) {
        this.userSource.next(user);
      } else {
        this.userSource.next(new LoggedUser());
      }
    }
    return this.currentUser;
  }
}
