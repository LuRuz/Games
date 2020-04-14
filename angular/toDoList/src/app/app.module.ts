import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MesComponent } from './mes/mes.component';
import { SemanaComponent } from './semana/semana.component';
import { DiaComponent } from './dia/dia.component';
import { RouterModule } from '@angular/router';

const routes: Routes = [
  { path: '', component: MesComponent },
  { path: 'mes', component: MesComponent },
  { path: 'semana', component: SemanaComponent },
  { path: 'dia', component: DiaComponent },
  { path: '**', redirectTo: '/', pathMatch: 'full' }
];

@NgModule({
  declarations: [
    AppComponent,
    MesComponent,
    SemanaComponent,
    DiaComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
