export class Order {
    id?: number
    status?: string;
    details?: string
    address?: any;
    teas?: any;

    constructor(){
        this.teas = [];
    }
}
