import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { PessoasListagemComponent } from './pessoas-listagem/pessoas-listagem.component';
import { PessoasService } from './pessoas-listagem/pessoas.service';
import { PessoasPersistenciaComponent } from './pessoas-persistencia/pessoas-persistencia.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    PessoasListagemComponent,
    PessoasPersistenciaComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [PessoasService],
  bootstrap: [AppComponent]
})
export class AppModule { }
