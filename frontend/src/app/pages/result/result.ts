import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-result',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './result.html',
  styleUrls: ['./result.css']
})
export class Result implements OnInit {
  userProfile: any = null;

  constructor(private router: Router) { }

  ngOnInit() {
    // 1. Grab the real string data from storage
    const storedData = sessionStorage.getItem('user_profile');
    
    if (storedData) {
      // 2. Turn it back into an active object for your HTML template
      this.userProfile = JSON.parse(storedData);
    } else {
      // Emergency fallback only if someone forces a route jump without uploading an Aadhaar
      this.userProfile = {
        name: 'No Session Found',
        dob: 'XX-XX-XXXX',
        gender: 'N/A',
        aadhaar: 'XXXX-XXXX-XXXX'
      };
    }
  }

  logout() {
    // 3. Clear data out when logging out to keep personal data secure
    sessionStorage.removeItem('user_profile');
    this.router.navigate(['/landing']);
  }
}
