import mediapipe as mp
import cv2 as cv
import math

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



# Load the image
folder_path = r"D:\BIIT\CrciketCoahing\images\Coverdrive\coverdrive-"
image_count = 1
total_detection_count = 0
total_non_detection_count = 0

dict = {}
df = {}

# Initialize pose detection model
with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.27) as pose:
    for i in range(0, 20):
        image_path = folder_path + str(image_count) + ".jpg"
        image_count += 1

        image = cv.imread(image_path)
        # image = cv.resize(image, (640, 480))

        image_height, image_width = image.shape[:2]
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        results = pose.process(image_rgb)

        if results.pose_landmarks:
            total_detection_count += 1
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
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


            # def processing_image(frame, bx, by, bw, bh, full_image):
            #     # Crop the ROI from the frame
            #     roi = frame[by:by + bh, bx:bx + bw]
            #     image = cv.cvtColor(roi, cv.COLOR_RGB2BGR)
            #
            #     with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.27) as pose:
            #         image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            #         results = pose.process(image_rgb)
            #
            #         if results.pose_landmarks:
            #             # Offset the landmarks to full image coordinates
            #             for landmark in results.pose_landmarks.landmark:
            #                 landmark.x = landmark.x * bw + bx
            #                 landmark.y = landmark.y * bh + by
            #
            #             # Draw landmarks back on the full image within the ROI
            #             mp_drawing.draw_landmarks(
            #                 full_image,
            #                 results.pose_landmarks,
            #                 mp_pose.POSE_CONNECTIONS,
            #                 mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
            #                 mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
            #             )
            #
            #             # Get image dimensions for landmark calculations
            #             image_width, image_height = full_image.shape[1], full_image.shape[0]
            #             landmarks = results.pose_landmarks.landmark
            #
            #             # Define key points with the offset coordinates
            #             left_wrist = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x),
            #                           int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y))
            #             left_elbow = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x),
            #                           int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y))
            #             left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x),
            #                              int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y))
            #             right_wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x),
            #                            int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y))
            #             right_elbow = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x),
            #                            int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y))
            #             right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x),
            #                               int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y))
            #             left_hip = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x),
            #                         int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y))
            #             left_knee = (int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x),
            #                          int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y))
            #             left_ankle = (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x),
            #                           int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y))
            #             right_hip = (int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x),
            #                          int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y))
            #             right_knee = (int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x),
            #                           int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y))
            #             right_ankle = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x),
            #                            int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y))
            #
            #             # Calculate the four angles
            #             left_arm_angle = calculate_angle(left_wrist, left_elbow, left_shoulder)
            #             right_arm_angle = calculate_angle(right_wrist, right_elbow, right_shoulder)
            #             left_leg_angle = calculate_angle(left_ankle, left_knee, left_hip)
            #             right_leg_angle = calculate_angle(right_ankle, right_knee, right_hip)
            #
            #             # Display angles on the full image
            #             cv.putText(full_image, f"Left Arm Angle: {int(left_arm_angle)}", left_shoulder,
            #                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            #             cv.putText(full_image, f"Right Arm Angle: {int(right_arm_angle)}", right_shoulder,
            #                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            #             cv.putText(full_image, f"Left Leg Angle: {int(left_leg_angle)}", left_knee,
            #                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            #             cv.putText(full_image, f"Right Leg Angle: {int(right_leg_angle)}", right_knee,
            #                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            #
            #             # Display the result image with landmarks and angles
            #             cv.imshow("Full Image with Landmarks", full_image)
            #             cv.waitKey(0)
            #
            #             # Create a dictionary of angles
            #             angle_dict = {
            #                 'Left Arm Angle': int(left_arm_angle),
            #                 'Right Arm Angle': int(right_arm_angle),
            #                 'Left Leg Angle': int(left_leg_angle),
            #                 'Right Leg Angle': int(right_leg_angle)
            #             }
            #
            #             return angle_dict, full_image
            #         else:
            #             print("No pose landmarks detected.")
            #             return None, full_image


            # 1. Angle between Front and Back Foot (Ankles)
            foot_angle = calculate_angle(front_foot_pixel, back_foot_pixel, front_knee_pixel)

            # 2. Front and Back Knee Angles (Hip-Knee-Ankle)
            front_knee_angle = calculate_angle(hip_pixel, front_knee_pixel, front_foot_pixel)
            back_knee_angle = calculate_angle(hip_pixel, back_knee_pixel, back_foot_pixel)

            # 3. Shoulder angle (Elbow-Shoulder-Hip)
            shoulder_angle = calculate_angle(lead_elbow_pixel, lead_shoulder_pixel, hip_pixel)

            # 4. Elbow angle (Shoulder-Elbow-Wrist)
            elbow_angle = calculate_angle(lead_shoulder_pixel, lead_elbow_pixel, lead_wrist_pixel)
            dict["coverdrive-"+str(image_count-1)+".jpg"] = {
                'Foot Angle': int(foot_angle),
                'Front Knee Angle': int(front_knee_angle),
                'Back Knee Angle': int(back_knee_angle),
                'Shoulder Angle': int(shoulder_angle),
                'Elbow Angle': int(elbow_angle)
            }
            # Display the angles on the image
            cv.putText(image, f'Foot Angle: {int(foot_angle)}', back_foot_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.7,
                       (0, 0, 0), 2)
            cv.putText(image, f'Front Knee Angle: {int(front_knee_angle)}', front_knee_pixel,
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.putText(image, f'Back Knee Angle: {int(back_knee_angle)}', back_knee_pixel, cv.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 0, 0), 2)
            cv.putText(image, f'Shoulder Angle: {int(shoulder_angle)}', lead_shoulder_pixel,
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cv.putText(image, f'Elbow Angle: {int(elbow_angle)}', lead_elbow_pixel, cv.FONT_HERSHEY_SIMPLEX, 0.5,
                       (0, 0, 0), 2)

            # Display the image with angles
            cv.imshow("coverdrive-"+str(image_count-1), image)
            cv.waitKey(0)
        else:
            print("No pose landmarks detected.")
            total_non_detection_count += 1
            print("Image is:", folder_path)


# Release resources
cv.destroyAllWindows()
print("Total Detected images are:", total_detection_count)
print("Total Non-Detected images are:", total_non_detection_count, "\n\n")

# for key, value in dict.items():
#     print("Image:",key)
#     print("Angles:",value,"\n\n")
#
# data = {
#                 'Foot Angle': [],
#                 'Front Knee Angle': [],
#                 'Back Knee Angle': [],
#                 'Shoulder Angle': [],
#                 'Elbow Angle': []
#      }
# counter_index = 0
# for key, value in dict.items():
#     for k, v in value.items():
#         if k == "Foot Angle":
#             data["Foot Angle"].append(v)
#         elif k == "Front Knee Angle":
#             data["Front Knee Angle"].append(v)
#
#         elif k == "Back Knee Angle":
#             data["Back Knee Angle"].append(v)
#
#         elif k == "Shoulder Angle":
#             data["Shoulder Angle"].append(v)
#
#         elif k == "Elbow Angle":
#             data["Elbow Angle"].append(v)
#
#
# for key, value in data.items():
#     print(key+":", min(value), max(value))

