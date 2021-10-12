import { TestBed } from '@angular/core/testing';

import { RecipeEditorService } from './recipe-editor.service';

describe('RecipeEditorService', () => {
  let service: RecipeEditorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RecipeEditorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
