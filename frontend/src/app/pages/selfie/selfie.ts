import {
    Component,
    ElementRef,
    ViewChild,
    AfterViewInit,
    OnDestroy, // Added for clean up
    NgZone,
    ChangeDetectorRef
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Api } from '../../services/api';

@Component({
    selector: 'app-selfie',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './selfie.html',
    styleUrls: ['./selfie.css']
})
export class Selfie implements AfterViewInit, OnDestroy {

    @ViewChild('video') video!: ElementRef<HTMLVideoElement>;

    loading = false;
    verified = false;
    failed = false;
    score: number | null = null;
    stream!: MediaStream;
    cameraError = false; // Added to handle blocked cameras

    constructor(
        private api: Api,
        private router: Router,
        private ngZone: NgZone,
        private cdr: ChangeDetectorRef
    ) { }

    async ngAfterViewInit() {
        // Wrapped in try/catch to handle camera errors or user rejections gracefully
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 1280 }, height: { ideal: 720 } } // Optimized resolution
            });
            
            if (this.video?.nativeElement) {
                this.video.nativeElement.srcObject = this.stream;
            }
        } catch (error) {
            console.error('Camera access error:', error);
            this.cameraError = true;
            this.failed = true;
            this.cdr.detectChanges();
        }
    }

    // Automatically triggers when the user leaves the page/route
    ngOnDestroy() {
        this.stopCamera();
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => {
                track.stop();
                this.stream.removeTrack(track);
            });
        }
    }

    capture() {
        if (!this.video?.nativeElement || this.cameraError) return;

        this.loading = true;
        this.verified = false;
        this.failed = false;
        this.score = null;

        const video = this.video.nativeElement;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;

        const ctx = canvas.getContext('2d');
        if (!ctx) {
            this.loading = false;
            return;
        }
        
        ctx.drawImage(video, 0, 0);

        canvas.toBlob(
            (blob) => {
                if (!blob) {
                    this.loading = false;
                    this.cdr.detectChanges();
                    return;
                }

                const file = new File([blob], 'selfie.jpg', { type: 'image/jpeg' });

                this.api.verifySelfie(file).subscribe({
                    next: (res: any) => {
                        console.log('SELFIE RESULT', res);
                        
                        this.loading = false;
                        this.score = res.score;
                        this.verified = res.verified === true;
                        this.failed = !this.verified;
                        
                        this.cdr.detectChanges();

                        setTimeout(() => {
                            this.stopCamera();
                        }, 300);
                    },
                    error: (err) => {
                        console.error('API Error:', err);
                        this.loading = false;
                        this.failed = true;
                        this.stopCamera();
                        this.cdr.detectChanges();
                    }
                });
            },
            'image/jpeg',
            0.95 // Keeps image quality crisp for facial recognition
        );
    }

    continue() {
        this.router.navigate(['/liveness']);
    }
}
