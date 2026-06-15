import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Aadhaar } from './aadhaar';

describe('Aadhaar', () => {
  let component: Aadhaar;
  let fixture: ComponentFixture<Aadhaar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Aadhaar],
    }).compileComponents();

    fixture = TestBed.createComponent(Aadhaar);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
