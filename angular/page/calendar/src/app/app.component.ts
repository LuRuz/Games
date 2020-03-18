import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'calendar';
  mesActual = 2;
  empiezeMes =  2;
  nombreMes = [
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre'
  ];
  transform(value, start) : any {
    let res = [];
    for (let i = start; i < value+start; i++) {
      if (i!==31){
        res.push(i);
      }
    }
      return res;
  }
}

