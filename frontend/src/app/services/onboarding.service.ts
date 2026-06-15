import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class OnboardingService {
  // This stores your Aadhaar API response profile data
  aadhaarProfile: any = null; 
}
