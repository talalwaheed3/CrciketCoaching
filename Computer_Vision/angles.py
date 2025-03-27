import mediapipe as mp
import cv2 as cv
import math
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(point1, point2, point3):
    """Calculate the angle between three points (in degrees)."""
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Calculate the angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    return angle + 360 if angle < 0 else angle


def processing_image(frame, bx, by, bw, bh):

    roi = frame[by:by + bh, bx:bx + bw]
    if isinstance(roi, np.ndarray):
        image = cv.cvtColor(roi, cv.COLOR_RGB2BGR)
    else:
        image = cv.cvtColor(np.array(roi), cv.COLOR_RGB2BGR)

    # Initialize pose detection model
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.27) as pose:
        # image = cv.imread(image)
        # image = cv.resize(image, (640, 480))

        image_height, image_width = image.shape[:2]
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        results = pose.process(image_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
            )

            landmarks = results.pose_landmarks.landmark

            # Define key points
            left_wrist = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height))
            left_elbow = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * image_width),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * image_height))
            left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width),
                             int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height))
            right_wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height))
            right_elbow = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * image_width),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * image_height))
            right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width),
                              int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height))
            left_hip = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * image_width),
                        int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * image_height))
            left_knee = (int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * image_width),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * image_height))
            left_ankle = (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * image_width),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * image_height))
            right_hip = (int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width),
                         int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height))
            right_knee = (int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_width),
                          int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y * image_height))
            right_ankle = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image_width),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image_height))

            # Calculate the four angles
            left_arm_angle = calculate_angle(left_wrist, left_elbow, left_shoulder)
            right_arm_angle = calculate_angle(right_wrist, right_elbow, right_shoulder)
            left_leg_angle = calculate_angle(left_ankle, left_knee, left_hip)
            right_leg_angle = calculate_angle(right_ankle, right_knee, right_hip)


            dict = {
                'Left Arm Angle': [int(left_arm_angle), left_shoulder],
                'Right Arm Angle': [int(right_arm_angle), right_shoulder],
                'Left Leg Angle': [int(left_leg_angle), left_knee],
                'Right Leg Angle': [int(right_leg_angle), right_knee]
            }

            return dict

        else:
            print("No pose landmarks detected.")
