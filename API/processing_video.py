# import threading
# from tkinter import Tk, Label
# from PIL import Image, ImageTk
import cv2
import numpy as np
from ultralytics import YOLO
from API import angles

model = YOLO("yolov8x.pt")


def process_video(video_path):
    """
    Process the video to find the frame where the bat and ball are closest,
    analyzing only every 10th frame per 60 fps for optimization.

    :param video_path: Path to the input video.
    :return: Angle analysis on the best frame.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Unable to open video at path '{video_path}'")
        return None

    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Typically 60
    frames_to_skip = int(fps / 6)  # Process 6 frames per second

    min_distance = float('inf')
    best_frame = None
    best_bat_center = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Skip frames to reduce processing
        if frame_count % frames_to_skip != 0:
            continue

        results = model(frame)
        bat_center, ball_center = None, None

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

                if class_id == 34:  # Bat
                    bat_center = (center_x, center_y)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.circle(frame, bat_center, 5, (255, 0, 0), -1)
                    cv2.putText(frame, "Bat", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                elif class_id == 32:  # Ball
                    ball_center = (center_x, center_y)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, ball_center, 5, (0, 255, 0), -1)
                    cv2.putText(frame, "Ball", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if bat_center and ball_center:
            distance = np.linalg.norm(np.array(bat_center) - np.array(ball_center))
            cv2.putText(frame, f"Distance: {distance:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            if distance < min_distance:
                min_distance = distance
                best_frame = frame.copy()
                best_bat_center = bat_center

        cv2.imshow("Tracking Bat and Ball", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if best_frame is not None:
        print(f"Best frame found after processing {frame_count} frames.")
        print(f"Bat center at closest approach: {best_bat_center}")
        # cv2.imshow("img", img)
        cv2.imshow("best_frame", best_frame)
        cv2.waitKey(0)
        # print('sending frame')

        # mediapipe_angles, mediapipe_image = angles.processing_image_using_mediapipe(best_frame, best_bat_center, stance="right")
        # yolo_angles, yolo_image = angles.processing_image_using_yolo(best_frame, best_bat_center, stance="right")
        # combined_image = np.hstack((mediapipe_image, yolo_image))
        #
        # # Display
        # cv2.imshow("MediaPipe Detection vs YOLO Detection", combined_image)
        # cv2.waitKey(0)

        # return mediapipe_angles, yolo_angles
        all_angles, image = angles.processing_image_using_mediapipe(best_frame, best_bat_center, stance="right")
        return all_angles

        # all_angles, image = angles.processing_image_using_yolov11(best_frame, best_bat_center, stance="right")
        # return all_angles
        # return angles.processing_image_using_mediapipe(best_frame, best_bat_center, stance="right")
    else:
        print("No frame with both bat and ball detected.")
        return None


# class VideoApp:
#     def __init__(self, root, video_path):
#         self.root = root
#         self.root.title("Video Controller")
#
#         self.cap = cv2.VideoCapture(video_path)
#         self.running = False
#         self.capturing = False
#         self.video_thread = None
#         self.stored_frames = []
#         self.best_frame = None
#         self.best_bat_center = None
#         self.min_distance = float('inf')
#
#         self.label = Label(self.root)
#         self.label.pack()
#
#         self.root.bind('<Key>', self.key_press)
#
#     def key_press(self, event):
#         key = event.keysym.lower()
#         if key == 'c':
#             self.continue_video()
#         elif key == 's':
#             self.stop_and_process()
#         elif key == 'space':
#             self.pause_video()
#
#     def continue_video(self):
#         if not self.running:
#             self.running = True
#             self.capturing = True
#             self.video_thread = threading.Thread(target=self.play_video, daemon=True)
#             self.video_thread.start()
#
#     def pause_video(self):
#         print("⏸️ Paused")
#         self.running = False
#
#     def play_video(self):
#         while self.running:
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
#
#             display_frame = frame.copy()
#
#             if self.capturing:
#                 self.stored_frames.append(frame.copy())
#
#                 results = model(frame)
#                 for result in results:
#                     for box in result.boxes:
#                         class_id = int(box.cls[0])
#                         x1, y1, x2, y2 = map(int, box.xyxy[0])
#                         center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
#
#                         if class_id == 34:
#                             cv2.rectangle(display_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
#                             cv2.putText(display_frame, "Bat", (x1, y1 - 10),
#                                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#                         elif class_id == 32:
#                             cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                             cv2.putText(display_frame, "Ball", (x1, y1 - 10),
#                                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#
#             self.display_frame(display_frame)
#             cv2.waitKey(1)
#
#     def display_frame(self, frame):
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         img = Image.fromarray(frame_rgb)
#         imgtk = ImageTk.PhotoImage(image=img)
#         self.label.imgtk = imgtk
#         self.label.configure(image=imgtk)
#
#     def stop_and_process(self):
#         print("⛔ Stopped capturing. Processing...")
#         self.running = False
#         self.capturing = False
#         threading.Thread(target=self.analyze_shot, daemon=True).start()
#
#     def analyze_shot(self):
#         self.min_distance = float('inf')
#         self.best_frame = None
#         self.best_bat_center = None
#
#         for frame in self.stored_frames:
#             results = model(frame)
#             bat_center = ball_center = None
#
#             for result in results:
#                 for box in result.boxes:
#                     class_id = int(box.cls[0])
#                     x1, y1, x2, y2 = map(int, box.xyxy[0])
#                     center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
#
#                     if class_id == 34:
#                         bat_center = (center_x, center_y)
#                     elif class_id == 32:
#                         ball_center = (center_x, center_y)
#
#             if bat_center and ball_center:
#                 distance = np.linalg.norm(np.array(bat_center) - np.array(ball_center))
#                 if distance < self.min_distance:
#                     self.min_distance = distance
#                     self.best_frame = frame.copy()
#                     self.best_bat_center = bat_center
#
#         if self.best_frame is not None:
#             print(f"✅ Best frame found with bat-ball distance: {self.min_distance:.2f}")
#             result_frame = angles.processing_image(self.best_frame, self.best_bat_center, stance="right")
#             self.display_frame(result_frame)
#         else:
#             print("❌ No best frame found.")
#
#
# def process_video(filepath):
#     root = Tk()
#     app = VideoApp(root, filepath)
#     root.mainloop()





# all_angles, result_img = process_video(r'Videos\Clip 1.mp4')
# angles = processing_image(image)
# print("✅ Calculated Angles:", all_angles)
# cv2.imshow("result_img", result_img)
# cv2.waitKey(0)
# Example usage



# video_path = r"Videos/Clip 1.mp4"  # Replace with your input video path
# best_frame = process_video(video_path)
#
# if best_frame is not None:
#     # Save or process the best frame further
#     output_image_path = r"best_frame.jpg"
#     cv2.imwrite(output_image_path, best_frame)
#     print(f"Best frame saved as {output_image_path}.")
# else:
#     print("No suitable frame found.")
