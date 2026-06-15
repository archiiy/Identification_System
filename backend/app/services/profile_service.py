import re

from app.logger.elastic_logger import (
    push_log
)


def extract_profile(text):

    profile = {}

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # ---------------- DOB ----------------

    dob = re.search(

    r"(?:DOB|DoB|Date\s*of\s*Birth)"

    r"\s*:?\s*"

    r"(\d{2}[/-]\d{2}[/-]\d{4})",

    text,

    re.I

)
    if dob:

        profile[
            "dob"
        ] = dob.group(1)

    # ---------------- GENDER ----------------

    gender = re.search(

        r"\b(Male|Female)\b",

        text,

        re.I
    )

    if gender:

        profile[
            "gender"
        ] = gender.group()

    # ---------------- AADHAAR ----------------

    aadhaar = re.search(

        r"\d{4}\s?\d{4}\s?\d{4}",

        text
    )

    if aadhaar:

        num = re.sub(
            r"\D",
            "",
            aadhaar.group()
        )

        profile[
            "aadhaar"
        ] = (

            "XXXX XXXX "

            +

            num[-4:]

        )

    # ---------------- NAME ----------------

    blocked = [

        "government",
        "india",
        "dob",
        "male",
        "female",
        "aadhaar",
        "issue",
        "date"
    ]

    lines = [

        x.strip()

        for x in text.split()

        if x.strip()

    ]

    candidates = []

    for i in range(
        len(lines)-1
    ):

        candidate = (

            lines[i]

            + " "

            +

            lines[i+1]

        )

        low = candidate.lower()

        if (

            all(
                w not in low
                for w in blocked
            )

            and

            re.match(
                r"^[A-Za-z ]+$",
                candidate
            )

        ):

            candidates.append(
                candidate
            )

    if candidates:

        profile[
            "name"
        ] = candidates[0]

    # ---------------- LOG ----------------

    push_log({

        "event":
        "profile_extraction",

        "verification":
        (
            "passed"
            if profile
            else
            "failed"
        ),

        "name_found":
        (
            "name"
            in profile
        ),

        "dob_found":
        (
            "dob"
            in profile
        ),

        "gender_found":
        (
            "gender"
            in profile
        ),

        "aadhaar_found":
        (
            "aadhaar"
            in profile
        )

    })

    return profile