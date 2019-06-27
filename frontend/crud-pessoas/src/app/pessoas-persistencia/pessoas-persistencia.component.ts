import { Component, OnInit } from '@angular/core';
import { ParamMap, ActivatedRoute, Router, } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FormBuilder } from '@angular/forms';


let headers = new HttpHeaders({
  'Content-Type': 'application/json'
});
let options = { headers: headers };

@Component({
  selector: 'app-pessoas-persistencia',
  templateUrl: './pessoas-persistencia.component.html',
  styleUrls: ['./pessoas-persistencia.component.scss']
})

export class PessoasPersistenciaComponent implements OnInit {

  urlPessoa = 'http://0.0.0.0:5000/pessoas';
  urlTelefone = 'http://0.0.0.0:5000/telefones';
  pessoa$;
  telefones;
  resposta$;
  button_text$;
  telefoneForm;
  pessoaForm;

  constructor(
    private http: HttpClient, private route: ActivatedRoute,
    private router: Router, private formBuilder: FormBuilder) {

    this.telefoneForm = this.formBuilder.group({
      ddd: '', numero: ''
    })

    this.pessoaForm = this.formBuilder.group({
      nome: '', email: '', cpf: '', datanascimento: ''
    })
  }

  onTelefoneFormSubmit(formData) {
    let telefone = {
      numero: formData.numero,
      ddd: formData.ddd,
      pessoa_id: this.pessoa$.id
    };
    this.addTelefone(telefone);
    this.telefoneForm.reset();
  }

  onPessoaFormSubmit(formData) {
    let pessoa = {
      nome: formData.nome,
      email: formData.email,
      cpf: formData.cpf,
      datanascimento: formData.datanascimento
    };
    if (this.button_text$ === 'Cadastrar') {
      this.addPessoa(pessoa);
      // NAVIGATES to list page the reloads it content
      this.router.navigate(['/']).then(
        (evn) => { window.location.reload(); }
      );
    } else {
      this.updatePessoa(pessoa);
    }

  }

  createTelefoneObservable(telefone): Observable<Object> {
    return this.http.post(`${this.urlTelefone}`, telefone);
  }

  createPessoaObservable(pessoa): Observable<Object> {
    return this.http.post(`${this.urlPessoa}`, pessoa);
  }

  updatePessoaObservable(pessoa): Observable<Object> {
    return this.http.put(`${this.urlPessoa}/${this.pessoa$.id}`, pessoa);
  }

  fetchPessoa(id): Observable<Object> {
    return this.http.get(`${this.urlPessoa}/${id}`)
  }

  fetchTelefonesObservable(pessoa_id): Observable<Object> {
    return this.http.get(`${this.urlTelefone}?pessoa_id=${pessoa_id}`)
  }

  deleteTelefoneObservable(id): Observable<Object> {
    return this.http.delete(`${this.urlTelefone}/${id}`)
  }

  getTelefones(pessoa_id) {

    this.fetchTelefonesObservable(pessoa_id).subscribe(
      (response) => {
        this.resposta$ = response;
        this.telefones = this.resposta$.data;
      }
    )
  }

  addTelefone(telefone) {
    this.createTelefoneObservable(telefone).subscribe(
      (response) => {
        this.getTelefones(this.pessoa$.id);
      }
    )
  }

  addPessoa(pessoa) {
    this.createPessoaObservable(pessoa).subscribe(
      (response) => { })
  }

  updatePessoa(pessoa) {
    console.log(pessoa.cpf);
    this.updatePessoaObservable(pessoa).subscribe(
      (response) => { 
        console.log(pessoa.cpf)
      })
  }


  deleteTelefone(telefone) {
    this.deleteTelefoneObservable(telefone.id).subscribe(
      (response) => {
        this.getTelefones(this.pessoa$.id);
      }
    )
  }


  ngOnInit() {

    this.pessoa$ = this.route.paramMap.subscribe(
      (params: ParamMap) => {
        if (params.has('id')) {
          this.button_text$ = 'Alterar';
          this.fetchPessoa(params.get('id')).subscribe(
            (response) => {
              this.resposta$ = response;
              this.pessoa$ = this.resposta$.data;
            }
          );
          this.getTelefones(params.get('id'));
        } else {
          this.button_text$ = 'Cadastrar';
        }
      }
    )

  }


}