import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PessoasPersistenciaComponent } from './pessoas-persistencia.component';

describe('PessoasPersistenciaComponent', () => {
  let component: PessoasPersistenciaComponent;
  let fixture: ComponentFixture<PessoasPersistenciaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PessoasPersistenciaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PessoasPersistenciaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
