import { User } from './../backend-api/interfaces/user';
export class LoggedUser implements User {
    id?: number;
    login?: string;
    email?: string;
    password?: string;
    user_type?: number;
    default_address?: any;
    orders?: any;

    constructor() {
    }
}
