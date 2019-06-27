import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';



@Injectable()
export class PessoasService {
    urlBase = 'http://0.0.0.0:5000/pessoas';
    constructor(private http: HttpClient) { }

    fetchPessoas(): Observable<Object> {
        return this.http.get(`${this.urlBase}`)
    }

    fetchPessoa(id): Observable<Object> {
        return this.http.get(`${this.urlBase}/${id}`)
    }

    editarPessoa(pessoa): Observable<Object> {
        return this.http.put(`${this.urlBase}/${pessoa.id}`, pessoa)
    }

    deletePessoa(pessoa): Observable<Object> {
        return this.http.delete(`${this.urlBase}/${pessoa.id}`)
    }

}