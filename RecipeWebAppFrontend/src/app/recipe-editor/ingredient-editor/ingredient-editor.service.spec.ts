import { TestBed } from '@angular/core/testing';

import { IngredientEditorService } from './ingredient-editor.service';

describe('IngredientEditorService', () => {
  let service: IngredientEditorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(IngredientEditorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
