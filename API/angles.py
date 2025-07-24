# <-------------------------------------------- USING YOLOV11 ---------------------------------------------->
# <-------------------------------------------- USING YOLOV11 ---------------------------------------------->
# <-------------------------------------------- USING YOLOV11 ---------------------------------------------->

from ultralytics import YOLO
import os
import cv2
import numpy as np
import mediapipe as mp

model_path = "D:\BIIT\Semester-7(FYP-1)\CrciketCoaching\API\yolo11x-pose.pt"

# The 17 COCO keypoint names, in order
JOINT_NAMES = [
    'NOSE', 'LEFT_EYE', 'RIGHT_EYE', 'LEFT_EAR', 'RIGHT_EAR',
    'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW',
    'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_HIP', 'RIGHT_HIP',
    'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE'
]

# Load the pose model once at module‐scope
if os.path.exists(model_path):
    _pose_model = YOLO(model_path)
else:
    raise FileNotFoundError(f"Model not found at {model_path}")


def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine, -1.0, 1.0))
    return np.degrees(angle)


def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def processing_image_using_yolov11(image, bat_center, stance="right"):
    """
    :param image:   BGR image numpy array
    :param bat_center: (x,y) of bat—provided by your video pipeline
    :param stance: "right" or "left"
    :return: dict of rounded angles, and draws on `image`
    """
    print('inside processing_image() function')
    # 1) Run pose inference
    results = _pose_model(image)
    if not results or results[0].keypoints is None:
        print("No keypoints detected.")
        return None
    print('landmarks detected')
    # 2) Pull out the first person's 17×3 tensor: [x, y, confidence]
    kpts = results[0].keypoints.data  # shape: (num_people, 17, 3)
    if kpts.shape[0] == 0:
        print("No people detected.")
        return None

    person = kpts[0].cpu().numpy()  # now a (17,3) array
    coords = person[:, :2]  # drop confidence → (17,2)

    # 3) Build a name→(x,y) dict
    landmarks = {name: tuple(coords[i]) for i, name in enumerate(JOINT_NAMES)}

    # 4) Helper to fetch with fallback
    def get_point(name):
        return landmarks.get(name, (0.0, 0.0))

    # 5) Pick the “front” side joints
    if stance.lower() == "right":
        wrist, elbow, shoulder = get_point('LEFT_WRIST'), get_point('LEFT_ELBOW'), get_point('LEFT_SHOULDER')
        hip, knee, ankle = get_point('LEFT_HIP'), get_point('LEFT_KNEE'), get_point('LEFT_ANKLE')
        opp_shldr = get_point('RIGHT_SHOULDER')
    else:
        wrist, elbow, shoulder = get_point('RIGHT_WRIST'), get_point('RIGHT_ELBOW'), get_point('RIGHT_SHOULDER')
        hip, knee, ankle = get_point('RIGHT_HIP'), get_point('RIGHT_KNEE'), get_point('RIGHT_ANKLE')
        opp_shldr = get_point('LEFT_SHOULDER')

    finger = wrist  # crude proxy

    # 6) Compute your six metrics
    angles = {
        "Front Elbow Angle": round(calculate_angle(shoulder, elbow, wrist)),
        "Front Wrist Angle": round(calculate_angle(elbow, wrist, finger)),
        "Shoulder Inclination": round(calculate_angle(opp_shldr, shoulder, hip)),
        "Front Hip Angle": round(calculate_angle(shoulder, hip, knee)),
        "Front Knee Angle": round(calculate_angle(hip, knee, ankle)),
        "Bat-Hip Distance": round(euclidean_distance(bat_center, hip))
    }

    # 7) Draw **all** joints so you can visually confirm
    for name, (x, y) in landmarks.items():
        cv2.circle(image, (int(x), int(y)), 3, (0, 255, 0), -1)

    # 8) Re‐use your old annotation logic to draw the angle lines + text
    annotated = {
        "Front Elbow Angle": (shoulder, elbow, wrist),
        "Front Wrist Angle": (elbow, wrist, finger),
        "Shoulder Inclination": (opp_shldr, shoulder, hip),
        "Front Hip Angle": (shoulder, hip, knee),
        "Front Knee Angle": (hip, knee, ankle),
    }
    for i, (label, (p1, p2, p3)) in enumerate(annotated.items()):
        cv2.line(image, tuple(map(int, p1)), tuple(map(int, p2)), (255, 255, 0), 2)
        cv2.line(image, tuple(map(int, p3)), tuple(map(int, p2)), (255, 255, 0), 2)
        x2, y2 = map(int, p2)
        cv2.putText(image, f"{label}: {angles[label]}°",
                    (x2 + 10, y2 - 10 - i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # 9) Finally draw the bat⇄hip distance
    cv2.line(image, tuple(map(int, bat_center)), tuple(map(int, hip)), (0, 255, 255), 2)
    cv2.putText(image,
                f"Bat-Hip Dist: {angles['Bat-Hip Distance']}px",
                (int(bat_center[0]), int(bat_center[1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

    # Show result
    cv2.imshow("result using yolov11", image)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return angles, image


# <-------------------------------------------- USING YOLOV11 ---------------------------------------------->
# <-------------------------------------------- USING YOLOV11 ---------------------------------------------->
# <-------------------------------------------- USING YOLOV11 ---------------------------------------------->


# <-------------------------------------------- USING MEDIAPIPE ---------------------------------------------->
# <-------------------------------------------- USING MEDIAPIPE ---------------------------------------------->
# <-------------------------------------------- USING MEDIAPIPE ---------------------------------------------->

def processing_image_using_mediapipe(image, bat_center, stance="right"):
    """
    Process the image to calculate angles for prominent joints based on the batter's stance.
    Also draws landmarks and displays angles on the frame.

    :param image: Frame containing the batter.
    :param bat_center: Center coordinate of bat from YOLO.
    :param stance: 'right' or 'left' handed batter.
    :return: Dictionary of calculated angles.
    """

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            print("No pose landmarks detected.")
            return {}

        lm = results.pose_landmarks.landmark

        def get_point(name):
            landmark = getattr(mp_pose.PoseLandmark, name)
            return int(lm[landmark].x * image.shape[1]), int(lm[landmark].y * image.shape[0])

        # Choose joints based on stance
        if stance.lower() == "right":
            wrist = get_point('LEFT_WRIST')
            elbow = get_point('LEFT_ELBOW')
            shoulder = get_point('LEFT_SHOULDER')
            hip = get_point('LEFT_HIP')
            knee = get_point('LEFT_KNEE')
            ankle = get_point('LEFT_ANKLE')
            opposite_shoulder = get_point('RIGHT_SHOULDER')
        else:  # left-handed
            wrist = get_point('RIGHT_WRIST')
            elbow = get_point('RIGHT_ELBOW')
            shoulder = get_point('RIGHT_SHOULDER')
            hip = get_point('RIGHT_HIP')
            knee = get_point('RIGHT_KNEE')
            ankle = get_point('RIGHT_ANKLE')
            opposite_shoulder = get_point('LEFT_SHOULDER')

        finger = wrist  # For now we assume finger ≈ wrist

        # Calculate and convert angles to regular floats
        angles = {
            "Front Elbow Angle": round(float(calculate_angle(shoulder, elbow, wrist))),
            "Front Wrist Angle": round(float(calculate_angle(elbow, wrist, finger))),
            "Shoulder Inclination": round(float(calculate_angle(opposite_shoulder, shoulder, hip))),
            "Front Hip Angle": round(float(calculate_angle(shoulder, hip, knee))),
            "Front Knee Angle": round(float(calculate_angle(hip, knee, ankle))),
            "Bat-Hip Distance": round(float(euclidean_distance(bat_center, hip)))
        }

        # Draw pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Draw lines and annotate angles
        annotated_points = {
            "Front Elbow Angle": (shoulder, elbow, wrist),
            "Front Wrist Angle": (elbow, wrist, finger),
            "Shoulder Inclination": (opposite_shoulder, shoulder, hip),
            "Front Hip Angle": (shoulder, hip, knee),
            "Front Knee Angle": (hip, knee, ankle),
        }

        for i, (name, (p1, p2, p3)) in enumerate(annotated_points.items()):
            cv2.line(image, p1, p2, (255, 255, 0), 2)
            cv2.line(image, p3, p2, (255, 255, 0), 2)
            x, y = p2
            angle = angles[name]
            cv2.putText(image, f"{name}: {angle:.1f}", (x + 10, y - 10 - i * 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Draw bat-hip line
        cv2.line(image, bat_center, hip, (0, 255, 255), 2)
        dist_text = f"Bat-Hip Dist: {angles['Bat-Hip Distance']:.1f}"
        cv2.putText(image, dist_text, (bat_center[0], bat_center[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

        cv2.imshow("result using mediapipe", image)
        cv2.waitKey(0)
        # key = cv2.waitKey(0)
        # if key == ord('s'):
        #     cv2.imwrite(path, image)
        return angles, image


#
# image = cv2.imread(r"D:\BIIT\Semester-7(FYP-1)\CrciketCoaching\API\Videos\straight drive GT.png")
# all_angles, img = processing_image_using_mediapipe(image, (573, 390))
# print('angles are:', all_angles)
#


# image_path = r"D:\BIIT\Semester-7(FYP-1)\CrciketCoaching\API\best_frame.jpg"
# image = cv2.imread(image_path)
# angles = processing_image(image)
# print("✅ Calculated Angles:", angles)
# cv2.imshow("Processed Image", image)
# cv2.waitKey(0)
# img = cv2.imread(r"D:\BIIT\Semester-7(FYP-1)\CrciketCoaching\API\best_frame.jpg")
# cv2.imshow("img", img)
# cv2.waitKey(0)
# def processing_image(img):
#
#     image = cv.cvtColor(img, cv.COLOR_RGB2BGR)
#     # cv.imshow(img, "best frane")
#     print("here in ANGLES FILES")
#     # Initialize pose detection model
#     with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.27) as pose:
#         # image = cv.imread(image)
#         # image = cv.resize(image, (640, 480))
#
#         image_height, image_width = image.shape[:2]
#         print("here in ANGLES FILES 2")
#         image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#
#         results = pose.process(image_rgb)
#
#         if results.pose_landmarks:
#             mp_drawing.draw_landmarks(
#                 image,
#                 results.pose_landmarks,
#                 mp_pose.POSE_CONNECTIONS,
#                 mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
#                 mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
#             )
#
#             landmarks = results.pose_landmarks.landmark
#
#             # Define key points
#             left_wrist = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width),
#                           int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height))
#             left_elbow = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * image_width),
#                           int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * image_height))
#             left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width),
#                              int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height))
#             right_wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width),
#                            int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height))
#             right_elbow = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * image_width),
#                            int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * image_height))
#             right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width),
#                               int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height))
#             left_hip = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * image_width),
#                         int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * image_height))
#             left_knee = (int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * image_width),
#                          int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * image_height))
#             left_ankle = (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * image_width),
#                           int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * image_height))
#             right_hip = (int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width),
#                          int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height))
#             right_knee = (int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_width),
#                           int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y * image_height))
#             right_ankle = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image_width),
#                            int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image_height))
#
#             # Calculate the four angles
#             left_arm_angle = calculate_angle(left_wrist, left_elbow, left_shoulder)
#             right_arm_angle = calculate_angle(right_wrist, right_elbow, right_shoulder)
#             left_leg_angle = calculate_angle(left_ankle, left_knee, left_hip)
#             right_leg_angle = calculate_angle(right_ankle, right_knee, right_hip)
#             print("here in ANGLES FILES 3")
#
#             dict = {
#                 'Left Arm Angle': int(left_arm_angle),
#                 'Right Arm Angle': int(right_arm_angle),
#                 'Left Leg Angle': int(left_leg_angle),
#                 'Right Leg Angle': int(right_leg_angle)
#             }
#
#             return dict
#
#         else:
#             print("No pose landmarks detected.")
#
#         # Release resources
#     cv.destroyAllWindows()


# <-------------------------------------------- USING MEDIAPIPE ---------------------------------------------->
# <-------------------------------------------- USING MEDIAPIPE ---------------------------------------------->
# <-------------------------------------------- USING MEDIAPIPE ---------------------------------------------->
