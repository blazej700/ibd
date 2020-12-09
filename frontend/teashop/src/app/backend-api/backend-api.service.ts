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

  postOrder(order: Order, user: LoggedUser ) {
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    const body = {
      status: 1,
      details: order.details,
      orderedBy: user.id,
      address: order.address,
      teaIds: order.teas
    };
    return this.http.post<any>(this.rootUrl + '/order', body, {headers});
  }

  getOrder(orderId){
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    let params = new HttpParams()
      .set('order_id', orderId.toString());
    return this.http.get<any>(this.rootUrl + '/order', { params, headers });
  }

  getOrders(userId: number, pageNumber: number, perPage: number,){
    const headers = new HttpHeaders().set('Magic-key', this.key.toString());
    let params = new HttpParams()
      .set('pageNumber', pageNumber.toString())
      .set('perPage', perPage.toString())
      .set('orderedBy', userId.toString());
    return this.http.get<any>(this.rootUrl + '/orders', { params, headers });
  }

  getTea(teaId: number) {
    let params = new HttpParams()
      .set('tea_id', teaId.toString());
    return this.http.get<any>(this.rootUrl + '/tea', { params });
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
