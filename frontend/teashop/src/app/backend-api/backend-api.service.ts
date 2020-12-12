import { LoggedUser } from './../classes/logged-user';
import { LoginComponent } from './../login/login.component';
import { User } from './interfaces/user';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Order } from '../classes/order';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {

  rootUrl = 'http://idb.blazejszymala.pl:8000';
  public key: any;

  constructor(private http: HttpClient) {
  }

  postLogin(login: string, password: string) {
    const body = {
      loginOrEmail: login,
      password,
    };
    return this.http.post<any>(this.rootUrl + '/login', body);
  }

  getPhoto(tea: any) {
    const params = new HttpParams()
      .set('tea_id', tea.id);
    return this.http.get<any>(this.rootUrl + '/photo/' + tea.id, { params, responseType: 'arraybuffer' as 'json' });
  }

  putOrder(order) {
    if (!this.key) {
      this.key = JSON.parse(localStorage.getItem('key'));
    }
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    let params = new HttpParams().set('order_id', order.id.toString());
    const body = {
      status: order.status,
      details: order.details,
      orderedBy: order.orderedBy,
      address: order.address,
      orderedTeas: order.ordered_teas
    };
    return this.http.put<any>(this.rootUrl + '/order', body, { params, headers });
  }

  postOrder(order: Order, user: LoggedUser) {
    if (!this.key) {
      this.key = JSON.parse(localStorage.getItem('key'));
    }
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    const body = {
      status: 1,
      details: order.details,
      orderedBy: user.id,
      address: order.address,
      orderedTeas: order.teas
    };
    return this.http.post<any>(this.rootUrl + '/order', body, { headers });
  }

  getOrder(orderId) {
    if (!this.key) {
      this.key = JSON.parse(localStorage.getItem('key'));
    }
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    let params = new HttpParams()
      .set('order_id', orderId.toString());
    return this.http.get<any>(this.rootUrl + '/order', { params, headers });
  }

  getOrders(pageNumber: number, perPage: number, userId?: number) {
    if (!this.key) {
      this.key = JSON.parse(localStorage.getItem('key'));
    }
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    let params = new HttpParams()
      .set('pageNumber', pageNumber.toString())
      .set('perPage', perPage.toString());
    if (userId) {
      params = params.set('orderedBy', userId.toString());
    }
    return this.http.get<any>(this.rootUrl + '/orders', { params, headers });
  }

  getTea(teaId: number) {
    let params = new HttpParams()
      .set('tea_id', teaId.toString());
    return this.http.get<any>(this.rootUrl + '/tea', { params });
  }

  putTea(teaId: number, body) {
    if (!this.key) {
      this.key = JSON.parse(localStorage.getItem('key'));
    }
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    let params = new HttpParams().set('tea_id', teaId.toString());
    return this.http.put<any>(this.rootUrl + '/tea', body, { params, headers });
  }

  postTea(body) {
    if (!this.key) {
      this.key = JSON.parse(localStorage.getItem('key'));
    }
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    return this.http.post<any>(this.rootUrl + '/tea', body, { headers });
  }

  deleteTea(tea_id: number) {
    if (!this.key) {
      this.key = JSON.parse(localStorage.getItem('key'));
    }
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    let params = new HttpParams().set('tea_id', tea_id.toString());
    return this.http.delete<any>(this.rootUrl + '/tea', { params, headers });
  }

  getTeas(pageNumber: number, perPage: number, filters?: any) {
    let params = new HttpParams()
      .set('pageNumber', pageNumber.toString())
      .set('perPage', perPage.toString());
    if (filters) {
      if (filters.teaType !== '') {
        params = params.append('teaType', filters.teaType);
      }
      if (filters.country !== '') {
        params = params.append('country', filters.country);
      }
      if (filters.minPrice !== null) {
        params = params.append('minPrice', filters.minPrice);
      }
      if (filters.maxPrice !== null) {
        params = params.append('maxPrice', filters.maxPrice);
      }
    }
    return this.http.get<any>(this.rootUrl + '/teas', { params });
  }

  getUser(userId: number) {
    const params = new HttpParams()
      .set('user_id', userId.toString());
    return this.http.get<any>(this.rootUrl + '/user', { params });
  }

  postUser(user: User) {
    user.user_type = 2;
    user.default_address = {
      country: '',
      city: '',
      street: '',
      number: '',
      postal_code: ''
    };
    return this.http.post<any>(this.rootUrl + '/user', user);
  }
}
