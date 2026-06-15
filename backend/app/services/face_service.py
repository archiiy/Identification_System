import cv2
import os
import time
from app.logger.elastic_logger import (
    push_log
)

def crop_face(image_path, save_dir="app/cropped_faces"):
    os.makedirs(save_dir, exist_ok=True)

    img = cv2.imread(image_path)
    if img is None:
        push_log({
            "event": "face_cropping",
            "image": image_path,
            "status": "failed",
            "reason": "Image not found"
        })
        return None

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(80, 80)
    )

    if len(faces) == 0:
        push_log({
            "event": "face_cropping",
            "verification": "failed",
            "reason": "No faces detected"
        })
        return None

    x, y, w, h = faces[0]
    pad = 40

    face = img[
        max(0, y-pad):min(img.shape[0], y+h+pad),
        max(0, x-pad):min(img.shape[1], x+w+pad)
    ]

    face = cv2.resize(face, (320, 320))

    filename = f"aadhaar_{int(time.time())}.jpg"

    path = os.path.join(save_dir, filename)

    cv2.imwrite(path, face)

    push_log({
        "event": "face_cropping",
        "saved_path": path,
        "verification": "passed",
        "faces_found": len(faces)
    })
    
    print("faces saved:", path)

    return path
