from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.liveness_service import check_liveness


router = APIRouter()

UPLOAD_DIR = "app/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/verify-live")
async def verify_live(
    file: UploadFile = File(...)
):

    path = os.path.join(
        UPLOAD_DIR,
        "live.mp4"
    )

    with open(path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = check_liveness(
        path
    )

    return {

        "live": result

    }