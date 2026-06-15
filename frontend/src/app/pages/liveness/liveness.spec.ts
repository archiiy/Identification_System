import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Liveness } from './liveness';

describe('Liveness', () => {
  let component: Liveness;
  let fixture: ComponentFixture<Liveness>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Liveness],
    }).compileComponents();

    fixture = TestBed.createComponent(Liveness);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
