import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Api } from '../../services/api';

@Component({
  selector: 'app-aadhaar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './aadhaar.html',
  styleUrl: './aadhaar.css'
})
export class Aadhaar {
  selected!: File;
  result: any = null;
  isLoading = false;

  constructor(
    private api: Api,
    private cdr: ChangeDetectorRef,
    private router: Router
  ) { }

  pick(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      this.selected = event.target.files[0];
    }
  }

  verify() {
    if (!this.selected) {
      alert('Upload Aadhaar');
      return;
    }

    this.isLoading = true;
    this.result = null;
    this.cdr.detectChanges();

    this.api.verifyAadhaar(this.selected).subscribe({
      next: (res: any) => {
        console.log('RESPONSE', res);
        this.result = res;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error(err);
        alert('Backend error');
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  goToSelfie() {
    if (this.result?.profile) {
      sessionStorage.setItem('user_profile', JSON.stringify(this.result.profile));
      this.router.navigate(['/selfie'], { state: { profile: this.result.profile } });
    }
  }
}
