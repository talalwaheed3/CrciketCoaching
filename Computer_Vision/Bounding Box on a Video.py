import mediapipe as mp
import cv2 as cv
import math
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    return angle + 360 if angle < 0 else angle


def processing_image(frame, bx, by, bw, bh, full_image):
    # Crop the ROI from the frame
    roi = frame[by:by + bh, bx:bx + bw]
    image = cv.cvtColor(roi, cv.COLOR_RGB2BGR)

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.27) as pose:
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            # Map landmarks to full image by scaling and offsetting with the bounding box
            landmarks = results.pose_landmarks.landmark
            image_width, image_height = full_image.shape[1], full_image.shape[0]

            # Draw landmarks and lines within the bounding box region in the full image
            for landmark in results.pose_landmarks.landmark:
                # Skip face landmarks (you can ignore specific indexes or types)
                if landmark.visibility > 0.5:  # Only draw visible landmarks
                    x = int(landmark.x * bw + bx)
                    y = int(landmark.y * bh + by)
                    cv.circle(full_image, (x, y), 5, (0, 255, 0), -1)  # Draw joint as a small circle

            # Draw the pose connections (lines between connected landmarks), excluding face connections
            for connection in mp_pose.POSE_CONNECTIONS:
                start_idx, end_idx = connection
                # Skip connections involving face landmarks (known landmark indices)
                if start_idx in [mp_pose.PoseLandmark.LEFT_EYE, mp_pose.PoseLandmark.RIGHT_EYE,
                                 mp_pose.PoseLandmark.MOUTH_LEFT, mp_pose.PoseLandmark.MOUTH_RIGHT,
                                 mp_pose.PoseLandmark.NOSE] or \
                   end_idx in [mp_pose.PoseLandmark.LEFT_EYE, mp_pose.PoseLandmark.RIGHT_EYE,
                               mp_pose.PoseLandmark.MOUTH_LEFT, mp_pose.PoseLandmark.MOUTH_RIGHT,
                               mp_pose.PoseLandmark.NOSE]:
                    continue

                start_point = landmarks[start_idx]
                end_point = landmarks[end_idx]

                # Convert normalized coordinates to pixel coordinates
                start_coords = (int(start_point.x * bw + bx), int(start_point.y * bh + by))
                end_coords = (int(end_point.x * bw + bx), int(end_point.y * bh + by))

                # Draw line between landmarks
                cv.line(full_image, start_coords, end_coords, (0, 255, 255), 2)

            # Define key points with adjusted coordinates for angle calculations
            left_wrist = (int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * bw + bx),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * bh + by))
            left_elbow = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * bw + bx),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * bh + by))
            left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * bw + bx),
                             int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * bh + by))
            right_wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * bw + bx),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * bh + by))
            right_elbow = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * bw + bx),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * bh + by))
            right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * bw + bx),
                              int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * bh + by))
            left_hip = (int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * bw + bx),
                        int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * bh + by))
            left_knee = (int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * bw + bx),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * bh + by))
            left_ankle = (int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x * bw + bx),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y * bh + by))
            right_hip = (int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * bw + bx),
                         int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * bh + by))
            right_knee = (int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x * bw + bx),
                          int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y * bh + by))
            right_ankle = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x * bw + bx),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y * bh + by))

            # Calculate the four angles
            left_arm_angle = calculate_angle(left_wrist, left_elbow, left_shoulder)
            right_arm_angle = calculate_angle(right_wrist, right_elbow, right_shoulder)
            left_leg_angle = calculate_angle(left_ankle, left_knee, left_hip)
            right_leg_angle = calculate_angle(right_ankle, right_knee, right_hip)

            # Display angles on the full image
            cv.putText(full_image, f"Left Arm Angle: {int(left_arm_angle)}", (left_elbow[0]+50, left_elbow[1]), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(full_image, f"Right Arm Angle: {int(right_arm_angle)}", (right_shoulder[0]-250, right_shoulder[1]), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(full_image, f"Left Leg Angle: {int(left_leg_angle)}", (left_knee[0]+50, left_knee[1]), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(full_image, f"Right Leg Angle: {int(right_leg_angle)}", (right_knee[0]-250, right_knee[1]), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Display the result image with landmarks and angles
            cv.imshow("Full Image with Landmarks", full_image)
            if cv.waitKey(0) & 0xFF == ord('q'):
                a=1

            # Create a dictionary of angles
            angle_dict = {
                'Left Arm Angle': int(left_arm_angle),
                'Right Arm Angle': int(right_arm_angle),
                'Left Leg Angle': int(left_leg_angle),
                'Right Leg Angle': int(right_leg_angle)
            }

            return angle_dict, full_image
        else:
            print("No pose landmarks detected.")
            return None, full_image


drawing = False
ix, iy = -1, -1
bx, by, bw, bh = 0, 0, 0, 0


def draw_rectangle(event, x, y, flags, param):
    global ix, iy, bx, by, bw, bh, drawing

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            bx, by = ix, iy
            bw, bh = x - ix, y - iy

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        bw, bh = x - ix, y - iy
        cv.rectangle(frame, (bx, by), (bx + bw, by + bh), (255, 255, 0))


video = cv.VideoCapture("../Videos/Reverse Sweep Shot/reverse sweep shot-4.mp4")
fps = video.get(cv.CAP_PROP_FPS)

start_time, end_time = 60+60+50, 60+60+54
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)
# forward_or_rewind_frames = int(2 * fps)

cv.namedWindow("Reverse Sweep Shot")
cv.setMouseCallback("Reverse Sweep Shot", draw_rectangle)

video.set(cv.CAP_PROP_POS_FRAMES, start_frame)
paused = False
my_angles = {}
while video.isOpened():

    current_frame = int(video.get(cv.CAP_PROP_POS_FRAMES))
    if current_frame >= end_frame:
        break

    if not paused:
        isTrue, frame = video.read()
        if not isTrue:
            print("Here break")
            break
    frame_with_box = frame.copy()

    if bw > 0 and bh > 0:
        cv.rectangle(frame_with_box, (bx, by), (bx + bw, by + bh), (255, 255, 0), 2)

    key = cv.waitKey(50) & 0xFF
    if key == ord("q"):
        break
    elif key == ord(' '):
        paused = not paused
    elif key == ord('n'):
        my_angles, image = processing_image(frame_with_box, bx, by, bw, bh, frame_with_box)
        frame_with_box = image
    cv.imshow("Reverse Sweep Shot", frame_with_box)

video.release()
cv.destroyAllWindows()
