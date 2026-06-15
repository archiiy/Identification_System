from paddleocr import PaddleOCR
import cv2
from app.logger.elastic_logger import push_log

ocr = PaddleOCR(use_angle_cls=True, lang="en")


def preprocess(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2)
    return gray


def extract_text(image_path):
    img = preprocess(image_path)
    result = ocr.ocr(img, cls=True)

    if not result:
        print("OCR PUSH EXECUTED")
        push_log({
            "event": "ocr_extraction",
            "verification": "failed",
            "reason": "No text detected"
        })
        return ""

    text = []

    for block in result:
        if block:
            for line in block:
                try:
                    detected = line[1][0]
                    confidence = line[1][1]
                    if confidence > 0.5:
                        text.append(detected)
                except:
                    pass

    final = " ".join(text)

    push_log({
        "event": "ocr_extraction",
        "verification": "passed" if final else "failed",
        "characters": len(final),
        "text_found": bool(final)
    })

    print("\nOCR:\n", final)
    return final