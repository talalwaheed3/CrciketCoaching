import mediapipe as mp
import cv2 as cv

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        # BGR 2 RGB
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # flip on horizontal
        image = cv.flip(image, 1)

        # Set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB 2 BGR
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # Detections
        print(results)

        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 70), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )
        cv.imshow("hand Tracking", image)
        if cv.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv.destroyAllWindows()
#
#
# # Video capture
# # cap = cv.VideoCapture(0)
#
# # # Initialize pose detection model
# # with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.5) as pose:
# #     while cap.isOpened():
# #         ret, frame = cap.read()
# #
# #         # Convert BGR to RGB
# #         image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
# #
# #         # Flip the image horizontally for a natural view
# #         image = cv.flip(image, 1)
# #
# #         # Set flag for write protection
# #         image.flags.writeable = False
# #
# #         # Make pose detections
# #         results = pose.process(image)
# #
# #         # Set flag to true for drawing
# #         image.flags.writeable = True
# #
# #         # Convert back to BGR for rendering
# #         image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
# #
# #         # Check if pose landmarks are detected
# #         if results.pose_landmarks:
# #             # Drawing pose landmarks on the frame
# #             mp_drawing.draw_landmarks(
# #                 image,
# #                 results.pose_landmarks,
# #                 mp_pose.POSE_CONNECTIONS,
# #                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
# #                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2),
# #             )
# #
# #             # Extract key landmarks for cover drive analysis
# #             landmarks = results.pose_landmarks.landmark
# #
# #             # You can access specific joints by their indices from the pose model
# #             # For example:
# #             front_foot = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
# #             back_foot = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
# #             front_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
# #             back_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
# #             lead_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
# #             lead_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
# #
# #             # Example of printing joint coordinates
# #             print(f"Front Foot: {front_foot.x}, {front_foot.y}")
# #             print(f"Back Foot: {back_foot.x}, {back_foot.y}")
# #             print(f"Front Knee: {front_knee.x}, {front_knee.y}")
# #             print(f"Back Knee: {back_knee.x}, {back_knee.y}")
# #             print(f"Lead Shoulder: {lead_shoulder.x}, {lead_shoulder.y}")
# #             print(f"Lead Elbow: {lead_elbow.x}, {lead_elbow.y}")
# #
# #         # Display the image
# #         cv.imshow("Cricket Shot Tracking", image)
# #
# #         if cv.waitKey(10) & 0xFF == ord('q'):
# #             break
#
# # # Release resources
# # cap.release()
# # cv.destroyAllWindows()


# data = {
#                 'Foot Angle': [],
#                 'Front Knee Angle': [],
#                 'Back Knee Angle': [],
#                 'Shoulder Angle': [],
#                 'Elbow Angle': []
#      }
#
# min_foot_angle = 0
# max_foot_angle = 0
#
# min_back_knee_angle = 0
# max_back_knee_angle = 0
#
# min_front_knee_angle = 0
# max_front_knee_angle = 0
#
# min_shoulder_angle = 0
# max_shoulder_angle = 0
#
# min_elbow_angle = 0
# max_elbow_angle = 0
#
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
#     print(key+":", value)
#
# min_foot_angle = min(data["Foot Angle"])
# max_foot_angle = max(data["Foot Angle"])
#
# min_back_knee_angle = min(data["Back Knee Angle"])
# max_back_knee_angle = max(data["Back Knee Angle"])
#
# min_front_knee_angle = min(data["Front Knee Angle"])
# max_front_knee_angle = max(data["Front Knee Angle"])
#
# min_shoulder_angle = min(data["Shoulder"])
# max_shoulder_angle = max(data["Shoulder"])
#
# min_elbow_angle = min(data["Elbow"])
# max_elbow_angle = max(data["Elbow"])
#
# df = {
#     "Shots": , "Angle_from": ,"Angle_to":
# }
# csv_file_name = "Angles.csv"
# # df.to_csv(csv_file_name, index=False)

# min_foot_angle = 0
# max_foot_angle = 0
#
# min_back_knee_angle = 0
# max_back_knee_angle = 0
#
# min_front_knee_angle = 0
# max_front_knee_angle = 0
#
# min_shoulder_angle = 0
# max_shoulder_angle = 0
#
# min_elbow_angle = 0
# max_elbow_angle = 0
#
# min_foot_angle = min(data["Foot Angle"])
# max_foot_angle = max(data["Foot Angle"])
#
# min_back_knee_angle = min(data["Back Knee Angle"])
# max_back_knee_angle = max(data["Back Knee Angle"])
#
# min_front_knee_angle = min(data["Front Knee Angle"])
# max_front_knee_angle = max(data["Front Knee Angle"])
#
# min_shoulder_angle = min(data["Shoulder"])
# max_shoulder_angle = max(data["Shoulder"])
#
# min_elbow_angle = min(data["Elbow"])
# max_elbow_angle = max(data["Elbow"])
#
# print("Foot Angle from:", min_foot_angle)
# print("Foot Angle to:", max_foot_angle)
#
# print("Front Knee Angle from:", min_front_knee_angle)
# print("Front Knee Angle to:", max_front_knee_angle)
#
# print("Back Knee Angle from:", min_back_knee_angle)
# print("Back Knee Angle to:", max_back_knee_angle)
#
# print("Shoulder Angle from:", min_shoulder_angle)
# print("Shoulder Angle to:", max_shoulder_angle)
#
# print("Elbow Angle from:", min_elbow_angle)
# print("Elbow Angle to:", max_elbow_angle)
#
# foot_max = 111
# foot_min = 20
#
# front_knee_max = 173
# front_knee_min = 81
#
# back_knee_max = 177
# back_knee_min = 108
#
# shoulder_max = 177
# shoulder_min = 37
#
# elbow_max = 162
# elbow_min = 24