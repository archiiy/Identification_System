import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Selfie } from './selfie';

describe('Selfie', () => {
  let component: Selfie;
  let fixture: ComponentFixture<Selfie>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Selfie],
    }).compileComponents();

    fixture = TestBed.createComponent(Selfie);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
