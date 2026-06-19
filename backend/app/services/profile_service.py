import re

from app.logger.elastic_logger import (
    push_log
)


def extract_name(text):

    try:

        cleaned = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        # remove everything before Government of India
        cleaned = re.sub(
            r".*?Government\s*of\s*India",
            "",
            cleaned,
            flags=re.I
        )

        # stop reading once DOB / Gender starts
        cleaned = re.split(

            r"(Issue\s*Date|DOB|D[O0]B|DB|Date\s*of\s*Birth|Male|Female)",

            cleaned,

            flags=re.I

        )[0]

        # remove numbers
        cleaned = re.sub(
            r"\d+",
            " ",
            cleaned
        )

        # keep only letters
        cleaned = re.sub(
            r"[^A-Za-z ]",
            " ",
            cleaned
        )

        words = cleaned.split()

        blocked = [

            "government",
            "india",
            "male",
            "female",
            "dob",
            "aadhaar",
            "issue",
            "issued",
            "date",
            "vid"

        ]

        words = [

            x

            for x in words

            if (

                x.lower()
                not in blocked

            )

        ]

        # remove OCR prefixes
        while (

            words

            and

            (
                len(words[0]) <= 3
                or
                words[0].isupper()
            )

        ):

            words.pop(
                0
            )

        if words:

            return " ".join(
                words
            )

    except Exception as e:

        push_log({

            "event":
            "name_extraction_error",

            "error":
            str(e)

        })

    return None


def extract_profile(text):

    profile = {}

    text = re.sub(

        r"\s+",

        " ",

        text

    ).strip()

    # ---------------- DOB ----------------

    dob = re.search(

        r"(?:D[O0]B|DB|Date\s*of\s*Birth)"
        r"[:/\s]*"
        r"(\d{2}[/\-]\d{2}[/\-]\d{4})",

        text,

        re.I

    )

    if dob:

        profile[
            "dob"
        ] = dob.group(1)

    # ---------------- GENDER ----------------

    gender = re.search(

        r"(male|female)",

        text,

        re.I

    )

    if gender:

        g = gender.group().lower()

        if "female" in g:

            profile[
                "gender"
            ] = "Female"

        elif "male" in g:

            profile[
                "gender"
            ] = "Male"

    # ---------------- AADHAAR ----------------

    aadhaar = re.search(

        r"\b\d{12}\b",

        text

    )

    if aadhaar:

        num = aadhaar.group()

        profile[
            "aadhaar"
        ] = (

            "XXXX XXXX "

            +

            num[-4:]

        )

    # ---------------- NAME ----------------

    name = extract_name(
        text
    )

    if name:

        profile[
            "name"
        ] = name

    # ---------------- LOG ----------------

    fields_found = (

        int(
            bool(
                profile.get(
                    "name"
                )
            )
        )

        +

        int(
            bool(
                profile.get(
                    "dob"
                )
            )
        )

        +

        int(
            bool(
                profile.get(
                    "aadhaar"
                )
            )
        )

    )

    push_log({

        "event":
        "profile_extraction",

        "verification":

        (

            "passed"

            if fields_found >= 2

            else

            "failed"

        ),

        "name_found":

        bool(
            profile.get(
                "name"
            )
        ),

        "dob_found":

        bool(
            profile.get(
                "dob"
            )
        ),

        "gender_found":

        bool(
            profile.get(
                "gender"
            )
        ),

        "aadhaar_found":

        bool(
            profile.get(
                "aadhaar"
            )
        ),

        "fields_found":

        fields_found

    })

    return profile


