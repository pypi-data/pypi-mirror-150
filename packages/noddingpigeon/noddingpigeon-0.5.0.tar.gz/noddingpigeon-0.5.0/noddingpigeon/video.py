"""
Video utilities.
"""
from enum import auto, Enum
from typing import List, Optional, Union

import cv2
import numpy as np
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import face_detection as mp_face

from noddingpigeon.config import Config


class VideoSegment(Enum):
    BEGINNING = auto()
    LAST = auto()


def video_to_landmarks(
        video_path: Optional[Union[int, str]],
        max_num_frames: Optional[int] = Config.seq_length,
        video_segment: VideoSegment = VideoSegment.BEGINNING,
        end_padding: bool = True,
        drop_consecutive_duplicates: bool = False
) -> List[List[float]]:
    assert video_segment in VideoSegment
    video_path = video_path if video_path else 0  # For 0, webcam will be used.
    font_scale = 0.6
    line_thickness = 1

    valid_frame_count = 0
    prev_features: List[float] = []
    landmarks: List[List[float]] = []
    cap = cv2.VideoCapture(video_path)  # pylint: disable=no-member
    with mp_face.FaceDetection(model_selection=0,
                               min_detection_confidence=0.5) as face_detection:

        while cap.isOpened():
            ret, bgr_frame = cap.read()
            if not ret:
                if video_path == 0:
                    continue  # Ignore empty frame of webcam.
                break  # End of given video.
            if max_num_frames and video_segment == VideoSegment.BEGINNING \
                    and valid_frame_count >= max_num_frames:
                break

            frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)  # pylint: disable=no-member
            result = face_detection.process(frame)

            if result and result.detections and len(result.detections) == 1:
                detection = result.detections[0]

                right_eye_rel = mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EYE)
                left_eye_rel = mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EYE)
                nose_tip_rel = mp_face.get_key_point(detection, mp_face.FaceKeyPoint.NOSE_TIP)
                mouth_center_rel = mp_face.get_key_point(detection, mp_face.FaceKeyPoint.MOUTH_CENTER)
                right_ear_rel = mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EAR_TRAGION)
                left_ear_rel = mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EAR_TRAGION)

                face_box_rel = detection.location_data.relative_bounding_box
                face_box_rel = [
                    max(0.0, face_box_rel.xmin),
                    max(0.0, face_box_rel.ymin),
                    face_box_rel.width,
                    face_box_rel.height,
                ]
                xs = [
                    right_eye_rel.x,
                    left_eye_rel.x,
                    nose_tip_rel.x,
                    mouth_center_rel.x,
                    right_ear_rel.x,
                    left_ear_rel.x,
                ]
                ys = [
                    right_eye_rel.y,
                    left_eye_rel.y,
                    nose_tip_rel.y,
                    mouth_center_rel.y,
                    right_ear_rel.y,
                    left_ear_rel.y,
                ]

                features = [*face_box_rel, *xs, *ys]
                assert len(features) == Config.num_original_features

                if drop_consecutive_duplicates and np.array_equal(
                        np.round(features, decimals=2),
                        np.round(prev_features, decimals=2)
                ):
                    continue

                landmarks.append(features)
                prev_features = features

                valid_frame_count += 1
            else:
                detection = None

            if video_path != 0:
                continue

            if detection:
                mp_drawing.draw_detection(frame, detection)

            flipped_frame = cv2.flip(frame, 1)  # pylint: disable=no-member

            text = f"{valid_frame_count} / {max_num_frames}" \
                if max_num_frames else str(valid_frame_count)
            cv2.putText(  # pylint: disable=no-member
                flipped_frame, text, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,  # pylint: disable=no-member
                font_scale, (0, 0, 255),
                line_thickness, cv2.LINE_AA  # pylint: disable=no-member
            )

            cv2.imshow(  # pylint: disable=no-member
                "Webcam",
                cv2.cvtColor(flipped_frame, cv2.COLOR_RGB2BGR)  # pylint: disable=no-member
            )

            if cv2.waitKey(1) == ord("q"):  # pylint: disable=no-member
                break

    cap.release()
    cv2.destroyAllWindows()  # pylint: disable=no-member

    if not landmarks:
        return []

    if max_num_frames and video_segment == VideoSegment.LAST:
        landmarks = landmarks[-max_num_frames:]

    if max_num_frames and end_padding and len(landmarks) < max_num_frames:
        last = landmarks[-1]
        landmarks = landmarks + [last] * (max_num_frames - len(landmarks))

    return landmarks


if __name__ == "__main__":
    video_to_landmarks(None, None)
