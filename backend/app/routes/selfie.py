from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.facematch_service import compare_faces


router = APIRouter()

UPLOAD_DIR = "app/uploads"
CROPPED_DIR = "app/cropped_faces"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/verify-selfie")
async def verify_selfie(file: UploadFile = File(...)):

    selfie_path = os.path.join(
        UPLOAD_DIR,
        "selfie.jpg"
    )

    with open(selfie_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    cropped_files = [

        os.path.join(CROPPED_DIR, f)

        for f in os.listdir(CROPPED_DIR)

        if f.endswith(".jpg")

    ]

    if not cropped_files:

        return {
            "verified": False,
            "reason": "No Aadhaar face found"
        }

    latest_crop = max(
        cropped_files,
        key=os.path.getctime
    )

    print(
        "USING:",
        latest_crop
    )

    score = compare_faces(
        latest_crop,
        selfie_path
    )

    if score is None:

        return {
            "verified": False,
            "reason": "Face not detected"
        }

    THRESHOLD = 0.45

    return {

        "score": round(score, 3),

        "threshold": THRESHOLD,

        "verified": score >= THRESHOLD,

        "confidence": (

            "high"

            if score >= 0.80

            else

            "medium"

            if score >= THRESHOLD

            else

            "low"

        )

    }