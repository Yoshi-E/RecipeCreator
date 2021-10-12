import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LdamodelComponent } from './ldamodel.component';

describe('LdamodelComponent', () => {
  let component: LdamodelComponent;
  let fixture: ComponentFixture<LdamodelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LdamodelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LdamodelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
