import {
  Component,
  ElementRef,
  ViewChild,
  AfterViewInit,
  OnDestroy,
  ChangeDetectorRef
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Api } from '../../services/api';

@Component({
  selector: 'app-liveness',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './liveness.html',
  styleUrls: ['./liveness.css']
})
export class Liveness implements AfterViewInit, OnDestroy {

  @ViewChild('video') video!: ElementRef<HTMLVideoElement>;

  loading = false;
  verified = false;
  failed = false;
  cameraError = false;
  stream!: MediaStream;

  constructor(
    private api: Api,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) { }

  async ngAfterViewInit() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 } }
      });
      if (this.video?.nativeElement) {
        this.video.nativeElement.srcObject = this.stream;
      }
    } catch (err) {
      console.error('Camera access error:', err);
      this.cameraError = true;
      this.failed = true;
      this.cdr.detectChanges();
    }
  }

  ngOnDestroy() {
    this.stopCamera();
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(t => {
        t.stop();
        this.stream.removeTrack(t);
      });
    }
  }

  capture() {
    if (!this.stream || this.cameraError) return;

    this.loading = true;
    this.verified = false;
    this.failed = false;
    this.cdr.detectChanges(); // Immediately shows "Processing..." layout

    const recorder = new MediaRecorder(this.stream, {
      mimeType: 'video/webm'
    });
    
    const chunks: Blob[] = [];

    recorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) {
        chunks.push(e.data);
      }
    };

    recorder.onstop = () => {
      // Camera stays active here so the user can still see themselves while waiting for the API
      const blob = new Blob(chunks, { type: 'video/webm' });
      const file = new File([blob], 'live.webm', { type: 'video/webm' });

      this.api.verifyLive(file).subscribe({
        next: (res: any) => {
          console.log('LIVENESS RESULT:', res);
          
          this.loading = false;
          this.verified = res.live === true;
          this.failed = !this.verified;
          
          this.cdr.detectChanges(); // 1. Refresh UI to show verification success/fail first
          this.stopCamera();        // 2. Shut off camera hardware immediately after rendering
        },
        error: (err) => {
          console.error('API Error:', err);
          this.loading = false;
          this.failed = true;
          
          this.cdr.detectChanges(); // 1. Refresh UI to show error layout
          this.stopCamera();        // 2. Shut off camera hardware
        }
      });
    };

    recorder.start();

    // Records the user for exactly 3 seconds before ending the stream segment
    setTimeout(() => {
      if (recorder.state !== 'inactive') {
        recorder.stop();
      }
    }, 3000);
  }

  continue() {
    this.router.navigate(['/result']);
  }
}



