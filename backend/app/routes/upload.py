from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.ocr_service import extract_text
from app.services.aadhaar_service import extract_aadhaar
from app.services.face_service import crop_face
from app.services.profile_service import (extract_profile)

router = APIRouter()

UPLOAD_DIR = "app/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/verify-aadhaar")
async def verify_aadhaar(
    file: UploadFile = File(...)
):

    # Save uploaded image

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # OCR

    extracted_text = extract_text(
        file_path
    )

    # Aadhaar validation

    aadhaar_result = extract_aadhaar(
        extracted_text
    )
    # Face crop

    try:
        cropped_face = crop_face(file_path)
    
    except Exception:
        
        
        cropped_face = None

    return {

        "status":
        "success",

        "aadhaar":
        aadhaar_result,

        "cropped_face":
        cropped_face,

        "profile":
        extract_profile(extracted_text)

    }