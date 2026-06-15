import cv2
import numpy as np
from insightface.app import FaceAnalysis
from app.logger.elastic_logger import push_log


model = FaceAnalysis()
model.prepare(ctx_id=0, det_size=(640, 640))


def compare_faces(aadhaar_path, selfie_path):
    aadhaar = cv2.imread(aadhaar_path)
    selfie = cv2.imread(selfie_path)

    if aadhaar is None or selfie is None:
        push_log({
            "event": "face_comparison",
            "status": "failed",
            "reason": "One or both images not found"
        })
        return None

    face1 = model.get(aadhaar)
    print("AADHAAR FACES:", len(face1))

    face2 = model.get(selfie)
    print("SELFIE FACES:", len(face2))

    if not face1 or not face2:
        push_log({
            "event": "face_comparison",
            "status": "failed",
            "reason": "No faces detected in one or both images"
        })
        return None

    emb1 = face1[0].embedding
    emb2 = face2[0].embedding

    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    similarity = float(similarity)

    verification = "passed" if similarity >= 0.70 else "failed"

    push_log({
        "event": "face_match",
        "verification": verification,
        "similarity": round(similarity, 3)
    })

    print("\nFACE SIMILARITY SCORE:", similarity)
    return similarity