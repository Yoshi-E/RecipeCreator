import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecipeEditorComponent } from './recipe-editor.component';

describe('RecipeEditorComponent', () => {
  let component: RecipeEditorComponent;
  let fixture: ComponentFixture<RecipeEditorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecipeEditorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecipeEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
