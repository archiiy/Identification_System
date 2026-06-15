from operator import is_

import cv2
import mediapipe as mp

from app.logger.elastic_logger import (
    push_log
)

mp_face = mp.solutions.face_mesh


def check_liveness(video_path):

    cap = cv2.VideoCapture(video_path)

    detector = mp_face.FaceMesh()

    positions = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        result = detector.process(
            rgb
        )

        if result.multi_face_landmarks:

            nose = (

                result
                .multi_face_landmarks[0]
                .landmark[1]
            )

            positions.append(
                (
                    nose.x,
                    nose.y
                )
            )

    cap.release()

    if len(positions) < 5:
        push_log({
            "event": "liveness_check",
            "verification": "failed",
            "reason": "Insufficient facial data for liveness detection"
        })

        return False

    movement = (

        max(
            p[0]
            for p in positions
        )
        -
        min(
            p[0]
            for p in positions
        )

    )

    is_live = (movement > 0.03)
    print("\nLIVENESS MOVEMENT SCORE:", movement)
    push_log({
        "event": "liveness_check",
        "verification": "passed" if is_live else "failed",
        "movement_score": round(movement, 4)
    })
    
    return is_live






    