# import mediapipe as mp
# import cv2 as cv
# import math
#
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose
#
#
# def calculate_angle(pointA, pointB, pointC):
#     # Create vectors AB and BC
#     AB = [pointA[0] - pointB[0], pointA[1] - pointB[1]]
#     BC = [pointC[0] - pointB[0], pointC[1] - pointB[1]]
#
#     # Calculate the dot product and magnitudes
#     dot_product = AB[0] * BC[0] + AB[1] * BC[1]
#     magnitude_AB = math.sqrt(AB[0] ** 2 + AB[1] ** 2)
#     magnitude_BC = math.sqrt(BC[0] ** 2 + BC[1] ** 2)
#
#     # Calculate the cosine of the angle
#     cos_angle = dot_product / (magnitude_AB * magnitude_BC)
#
#     # Get the angle in radians and then convert to degrees
#     angle = math.degrees(math.acos(cos_angle))
#
#     return angle
#
#
# # Load the image
# image_path = r"D:\BIIT\Semester 7(FYP-1)\PythonLibraries\images\Coverdrive\coverdrive-4.jpg"
# image = cv.imread(image_path)
# image = cv.resize(image, (640, 480))  # Resize to 640x480
#
# # Get image dimensions
# image_height, image_width = image.shape[:2]
#
# # Convert the image to RGB
# image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#
# # Initialize pose detection model
# with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
#     # Make pose detections
#     results = pose.process(image_rgb)
#
#     # Check if pose landmarks are detected
#     if results.pose_landmarks:
#         # Drawing pose landmarks on the image
#         mp_drawing.draw_landmarks(
#             image,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS,
#             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
#             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2),
#         )
#
#         # Extract key landmarks for cover drive analysis
#         landmarks = results.pose_landmarks.landmark
#
#         # Example of extracting specific joints and converting to pixel coordinates
#         front_foot = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
#         back_foot = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
#         front_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
#         back_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
#         lead_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#         lead_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#
#         # Convert normalized coordinates to pixel coordinates
#         front_foot_pixel = (int(front_foot.x * image_width), int(front_foot.y * image_height))
#         back_foot_pixel = (int(back_foot.x * image_width), int(back_foot.y * image_height))
#         front_knee_pixel = (int(front_knee.x * image_width), int(front_knee.y * image_height))
#         back_knee_pixel = (int(back_knee.x * image_width), int(back_knee.y * image_height))
#         lead_shoulder_pixel = (int(lead_shoulder.x * image_width), int(lead_shoulder.y * image_height))
#         lead_elbow_pixel = (int(lead_elbow.x * image_width), int(lead_elbow.y * image_height))
#
#         # Print joint pixel coordinates
#         print(f"Front Foot (pixels): {front_foot_pixel}")
#         print(f"Back Foot (pixels): {back_foot_pixel}")
#         print(f"Front Knee (pixels): {front_knee_pixel}")
#         print(f"Back Knee (pixels): {back_knee_pixel}")
#         print(f"Lead Shoulder (pixels): {lead_shoulder_pixel}")
#         print(f"Lead Elbow (pixels): {lead_elbow_pixel}")
#
#         # Optionally, add text to the image for better visualization
#         cv.putText(image, 'Front Foot', front_foot_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv.putText(image, 'Back Foot', back_foot_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv.putText(image, 'Front Knee', front_knee_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv.putText(image, 'Back Knee', back_knee_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv.putText(image, 'Lead Shoulder', lead_shoulder_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv.putText(image, 'Lead Elbow', lead_elbow_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#
#         cv.imshow('Pose Detection', image)
#         cv.waitKey(0)
#     else:
#         print("nothing detected")
#
#
# # Release resources
# cv.destroyAllWindows()


# import mediapipe as mp
# import cv2 as cv
# import math
#
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose
#
#
# def calculate_angle(pointA, pointB, pointC):
#     # Create vectors AB and BC
#     AB = [pointA[0] - pointB[0], pointA[1] - pointB[1]]
#     BC = [pointC[0] - pointB[0], pointC[1] - pointB[1]]
#
#     # Calculate the dot product and magnitudes
#     dot_product = AB[0] * BC[0] + AB[1] * BC[1]
#     magnitude_AB = math.sqrt(AB[0] ** 2 + AB[1] ** 2)
#     magnitude_BC = math.sqrt(BC[0] ** 2 + BC[1] ** 2)
#
#     # Calculate the cosine of the angle
#     cos_angle = dot_product / (magnitude_AB * magnitude_BC)
#
#     # Get the angle in radians and then convert to degrees
#     angle = math.degrees(math.acos(cos_angle))
#
#     return angle
#
#
# # Load the image
# image_path = r"D:\BIIT\Semester 7(FYP-1)\PythonLibraries\images\Coverdrive\coverdrive-4.jpg"
# image = cv.imread(image_path)
# image = cv.resize(image, (640, 480))  # Resize to 640x480
#
# # Get image dimensions
# image_height, image_width = image.shape[:2]
#
# # Convert the image to RGB
# image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#
# # Initialize pose detection model
# with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
#     # Make pose detections
#     results = pose.process(image_rgb)
#
#     # Check if pose landmarks are detected
#     if results.pose_landmarks:
#         # Drawing pose landmarks on the image
#         mp_drawing.draw_landmarks(
#             image,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS,
#             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
#             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2),
#         )
#
#         # Extract key landmarks for cover drive analysis
#         landmarks = results.pose_landmarks.landmark
#
#         # Convert normalized coordinates to pixel coordinates for relevant joints
#         front_foot_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * image_width),
#                             int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * image_height))
#         back_foot_pixel = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image_width),
#                            int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image_height))
#         front_knee_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * image_width),
#                             int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * image_height))
#         back_knee_pixel = (int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_width),
#                            int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y * image_height))
#         lead_shoulder_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width),
#                                int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height))
#         lead_elbow_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * image_width),
#                             int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * image_height))
#         lead_wrist_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width),
#                             int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height))
#         hip_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * image_width),
#                      int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * image_height))
#         back_elbow_pixel = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * image_width),
#                             int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * image_height))
#
#         # Calculate angles for relevant joints
#
#         # 1. Leg angles: hip-knee-ankle
#         front_leg_angle = calculate_angle(hip_pixel, front_knee_pixel, front_foot_pixel)
#         back_leg_angle = calculate_angle(hip_pixel, back_knee_pixel, back_foot_pixel)
#
#         # 2. Arm angles: shoulder-elbow-wrist
#         lead_arm_angle = calculate_angle(lead_shoulder_pixel, lead_elbow_pixel, lead_wrist_pixel)
#
#         # Display the angles on the image
#         cv.putText(image, f'Front Leg Angle: {int(front_leg_angle)}', front_knee_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv.putText(image, f'Back Leg Angle: {int(back_leg_angle)}', back_knee_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         cv.putText(image, f'Arm Angle: {int(lead_arm_angle)}', lead_elbow_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#
#         # Print joint pixel coordinates and angles for verification
#         print(f"Front Foot (pixels): {front_foot_pixel}")
#         print(f"Back Foot (pixels): {back_foot_pixel}")
#         print(f"Front Knee (pixels): {front_knee_pixel}")
#         print(f"Back Knee (pixels): {back_knee_pixel}")
#         print(f"Lead Shoulder (pixels): {lead_shoulder_pixel}")
#         print(f"Lead Elbow (pixels): {lead_elbow_pixel}")
#         print(f"Lead Arm Angle: {lead_arm_angle:.2f}")
#         print(f"Front Leg Angle: {front_leg_angle:.2f}")
#         print(f"Back Leg Angle: {back_leg_angle:.2f}")
#
#         # Display the image with angles
#         cv.imshow('Pose Detection with Angles', image)
#         cv.waitKey(0)
#     else:
#         print("No pose landmarks detected.")
#
#
# # Release resources
# cv.destroyAllWindows()


import mediapipe as mp
import cv2 as cv
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(pointA, pointB, pointC):
    AB = [pointA[0] - pointB[0], pointA[1] - pointB[1]]
    BC = [pointC[0] - pointB[0], pointC[1] - pointB[1]]

    dot_product = AB[0] * BC[0] + AB[1] * BC[1]
    magnitude_AB = math.sqrt(AB[0] ** 2 + AB[1] ** 2)
    magnitude_BC = math.sqrt(BC[0] ** 2 + BC[1] ** 2)

    cos_angle = dot_product / (magnitude_AB * magnitude_BC)
    angle = math.degrees(math.acos(cos_angle))

    return angle


# Load the image
image_path = r"D:\BIIT\Semester 7(FYP-1)\PythonLibraries\images\Coverdrive\coverdrive-4.jpg"
image = cv.imread(image_path)
# image = cv.resize(image, (640, 480))  # Resize to 640x480

# Get image dimensions
image_height, image_width = image.shape[:2]

# Convert the image to RGB
image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

# Initialize pose detection model
with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2),
        )

        landmarks = results.pose_landmarks.landmark

        # Convert normalized coordinates to pixel coordinates
        front_foot_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * image_width),
                            int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * image_height))
        back_foot_pixel = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image_width),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image_height))
        front_knee_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * image_width),
                            int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * image_height))
        back_knee_pixel = (int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_width),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y * image_height))
        lead_shoulder_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width),
                               int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height))
        lead_elbow_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * image_width),
                            int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * image_height))
        lead_wrist_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width),
                            int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height))
        hip_pixel = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * image_width),
                     int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * image_height))

        # Calculate angles for relevant joints

        # 1. Angle between Front and Back Foot (Ankles)
        foot_angle = calculate_angle(front_foot_pixel, back_foot_pixel, front_knee_pixel)

        # 2. Front and Back Knee Angles (Hip-Knee-Ankle)
        front_knee_angle = calculate_angle(hip_pixel, front_knee_pixel, front_foot_pixel)
        back_knee_angle = calculate_angle(hip_pixel, back_knee_pixel, back_foot_pixel)

        # 3. Shoulder angle (Elbow-Shoulder-Hip)
        shoulder_angle = calculate_angle(lead_elbow_pixel, lead_shoulder_pixel, hip_pixel)

        # 4. Elbow angle (Shoulder-Elbow-Wrist)
        elbow_angle = calculate_angle(lead_shoulder_pixel, lead_elbow_pixel, lead_wrist_pixel)

        # Display the angles on the image
        cv.putText(image, f'Foot Angle: {int(foot_angle)}',back_foot_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv.putText(image, f'Front Knee Angle: {int(front_knee_angle)}', front_knee_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.putText(image, f'Back Knee Angle: {int(back_knee_angle)}', back_knee_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv.putText(image, f'Shoulder Angle: {int(shoulder_angle)}', lead_shoulder_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv.putText(image, f'Elbow Angle: {int(elbow_angle)}', lead_elbow_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Display the image with angles
        # Resize the window (for example, make it 1024x768)
        cv.namedWindow('Pose Detection with Angles', cv.WINDOW_NORMAL)
        cv.resizeWindow('Pose Detection with Angles', 1024, 768)
        resized_image = cv.resize(image, None, fx=1.5, fy=1.5, interpolation=cv.INTER_LINEAR)
        cv.imshow('Pose Detection with Angles', image)
        cv.waitKey(0)
    else:
        print("No pose landmarks detected.")

# Release resources
cv.destroyAllWindows()
