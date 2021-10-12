import { TestBed } from '@angular/core/testing';

import { LDAModelService } from './ldamodel.service';

describe('LDAModelService', () => {
  let service: LDAModelService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LDAModelService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
