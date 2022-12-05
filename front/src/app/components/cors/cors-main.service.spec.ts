import { TestBed } from '@angular/core/testing';

import { CorsMainService } from './cors-main.service';

describe('CorsMainService', () => {
  let service: CorsMainService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CorsMainService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
