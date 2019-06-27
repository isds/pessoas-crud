import { Component, OnInit } from '@angular/core';
import { PessoasService } from './pessoas.service';
import { FormBuilder } from '@angular/forms';


@Component({
  selector: 'app-pessoas-listagem',
  templateUrl: './pessoas-listagem.component.html',
  styleUrls: ['./pessoas-listagem.component.scss']
})


export class PessoasListagemComponent implements OnInit {
  resposta$;
  pessoas$;
  searchForm;
  parameters;
  telefone;
  constructor(private pessoasService: PessoasService, private formBuilder: FormBuilder) {
    this.searchForm = this.formBuilder.group({
      nome: '', cpf: ''
    })
  }

  onSubmit(formData) {
    console.log('ON SUBMIT')
    let telefone = {
      nome: formData.nome,
      cpf: formData.cpf,
    };
    this.telefone = telefone;
    this.getPessoas();
  }

  preparaUrl() {
    console.log('ON PREPARA')
    let params = '';
    if (this.telefone !== undefined) {
      console.log('TELEFONE', this.telefone)

      if (this.telefone.nome !== "") {
        console.log('NOME', this.telefone.nome)
        params = params + `?nome=${this.telefone.nome}`
        
        if (this.telefone.cpf !== "") {
          params = params + `&cpf=${this.telefone.cpf}`
        }

      }else if (this.telefone.cpf !== "") {
        params = params + `?cpf=${this.telefone.cpf}`
      }
      this.parameters = params;
    }
  }

  getIdade(dataNascimento: any) {
    const hoje = new Date();
    dataNascimento = new Date(dataNascimento);
    let idade = hoje.getFullYear() - dataNascimento.getFullYear();
    const m = hoje.getMonth() - dataNascimento.getMonth();

    if (m < 0 || (m === 0 && hoje.getDate() < dataNascimento.getDate())) {
      idade--;
    }
    return idade;
  }

  getPessoas() {
    this.preparaUrl();
    console.log('URL', this.parameters)
    this.pessoasService.fetchPessoas(this.parameters).subscribe(
      (response) => {
        this.resposta$ = response;
        this.pessoas$ = this.resposta$.data;
      }
    );
  }

  deletePessoa(pessoa) {
    this.pessoasService.deletePessoa(pessoa).subscribe(
      (response) => {
        this.resposta$ = response;
        this.getPessoas();
      }
    )
  }

  editarPessoa(pessoa) {
    this.pessoasService.editarPessoa(pessoa).subscribe(
      (response) => {
        this.resposta$ = response;
      }
    )
  }

  ngOnInit() {
    this.getPessoas();
  }

}
