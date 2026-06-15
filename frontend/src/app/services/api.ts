import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class Api {

  http = inject(HttpClient);

  url = 'http://127.0.0.1:8000';

  verifyAadhaar(file: File) {
    const form = new FormData();
    form.append('file', file);
    return this.http.post(`${this.url}/verify-aadhaar`, form);
  }

  verifySelfie(file: File) {
    const form = new FormData();
    form.append('file', file);
    return this.http.post(`${this.url}/verify-selfie`, form);
  }

  // ✅ Added — sends the recorded video blob to /verify-live
  verifyLive(file: File) {
    const form = new FormData();
    form.append('file', file);
    return this.http.post(`${this.url}/verify-live`, form);
  }

}


