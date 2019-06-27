import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PessoasPersistenciaComponent } from './pessoas-persistencia/pessoas-persistencia.component';
import { PessoasListagemComponent } from './pessoas-listagem/pessoas-listagem.component'

const routes: Routes = [
  { path: '', component: PessoasListagemComponent },
  { path: 'pessoa-persistencia/:id', component: PessoasPersistenciaComponent },
  { path: 'pessoa-cadastro', component: PessoasPersistenciaComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

}
