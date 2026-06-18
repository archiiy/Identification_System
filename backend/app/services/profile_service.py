import re
import ollama

from app.logger.elastic_logger import (
    push_log
)


def extract_name(text):

    try:

        # strip everything after Issue Date to reduce noise
        cleaned = re.sub(
            r"Issue\s*Date.*",
            "",
            text,
            flags=re.I
        )

        # strip everything before Government of India
        cleaned = re.sub(
            r".*?Government\s+of\s+India\s*",
            "",
            cleaned,
            flags=re.I
        )

        response = ollama.chat(

            model="qwen2.5",

            messages=[
                {
                    "role": "user",
                    "content":
f"""Extract the full name of the Aadhaar card holder.
- Return ONLY the person's name, nothing else
- Ignore: Government of India, OCR noise like HRHR RCR SITTT and any random letters or numbers, and any text related
- Ignore: dates, numbers, DOB, gender words
- No explanation, no labels, just the name

OCR: {cleaned}"""
                }
            ],

            options={
                "temperature": 0
            }

        )

        name = (
            response["message"]["content"]
            .strip()
        )

        # remove LLM preamble like "The name is..." or "Name: ..."
        name = re.sub(
            r"(?:name\s*[:\-]?\s*|the\s+\w+\s+name\s+is\s+)",
            "",
            name,
            flags=re.I
        )

        # keep only letters and spaces
        name = re.sub(
            r"[^A-Za-z ]",
            "",
            name
        ).strip()

        blocked = [
            "government",
            "india",
            "male",
            "female",
            "dob",
            "aadhaar",
            "issue",
            "issued"
        ]

        words = [
            x for x in name.split()
            if x.lower() not in blocked
            and re.match(r"^[A-Za-z]+$", x)
        ]

        if words:
            return " ".join(words)

    except Exception as e:

        push_log({
            "event": "name_extraction_error",
            "error": str(e)
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
    # label required (not optional) to avoid picking Issue Date
    # handles D0B (zero), DB, DOB, Date ofBirth, no separator before date

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
    # \b\d{12}\b correctly skips VID (16 digits)

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

    name = extract_name(text)

    if name:

        profile[
            "name"
        ] = name

    # ---------------- LOG ----------------

    fields_found = (

        int(
            bool(
                profile.get("name")
            )
        )

        +

        int(
            bool(
                profile.get("dob")
            )
        )

        +

        int(
            bool(
                profile.get("aadhaar")
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
        bool(profile.get("name")),

        "dob_found":
        bool(profile.get("dob")),

        "gender_found":
        bool(profile.get("gender")),

        "aadhaar_found":
        bool(profile.get("aadhaar")),

        "fields_found":
        fields_found

    })

    return profile