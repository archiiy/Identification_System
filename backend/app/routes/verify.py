from fastapi import APIRouter

router = APIRouter()


@router.get("/final-verify")
async def final_verify():

    # temporary

    aadhaar = True
    selfie = True
    live = True

    return {

        "aadhaar": aadhaar,

        "face_match": selfie,

        "liveness": live,

        "verified":

        (

            aadhaar

            and

            selfie

            and

            live

        )

    }