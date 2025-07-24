# import threading
# from tkinter import Tk, Label
# from PIL import Image, ImageTk
import os

import cv2
import numpy as np
from ultralytics import YOLO
from API import angles
from API.Controller.CoachController import CoachController

model = YOLO("yolov8x.pt")


def save_clip(frames, output_path, fps):
    """
    Save a list of frames as a video clip.

    :param frames: List of video frames (numpy arrays)
    :param output_path: Path where the clip should be saved
    :param fps: Frames per second of the video
    :param frame_size: Tuple (width, height)
    """
    height, width = frames[0].shape[:2]
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    for frame in frames:
        out.write(frame)

    out.release()


def process_video(video_path, video_name, session_id, shot_name, coach_id):
    cap = cv2.VideoCapture(video_path)
    print("in process_video, cap is:", cap)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames_to_skip = 0
    # frames_to_skip = int((0 / 100) * fps)

    if not cap.isOpened():
        print(f"Error: Unable to open video at path '{video_path}'")
        return None

    # fps = int(cap.get(cv2.CAP_PROP_FPS))  # Typically 60
    # frames_to_skip = int(fps / 6)  # Process 6 frames per second

    print("Total frames:", fps)
    print("Frames to skip:", frames_to_skip)

    frames_per_clip = 1 * fps

    # min_distance = float('inf')
    # best_frame = None
    # best_bat_center = None
    # frame_count = 0

    index = 0
    frames = []
    clip_index = 1

    clips_folder = r"Videos\\Clips\\" + os.path.splitext(video_name)[0]
    print("clips_folder is:", clips_folder)

    # list_of_results = []
    if not os.path.exists(clips_folder):
        os.makedirs(clips_folder)

    if not os.listdir(clips_folder):
        while True:
            print(f"clip no: {clip_index}")
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

            index += 1
            print(f"Frame no:{index}")
            if index == frames_per_clip:
                index = 0
                save_clip(frames, rf"{clips_folder}\\{shot_name}-{session_id}-{clip_index}.mp4", fps)  # output_path, fps
                clip_index += 1
                frames = []
        if frames:
            save_clip(frames, rf"{clips_folder}\\{shot_name}-{session_id}-{clip_index}.mp4", fps)
            print(f"[+] Saved final clip #{clip_index} with {len(frames)} frames.")
            clip_index += 1

        cap.release()
    else:
        print("Don't need to divide clips, clips already exists.")

    list_of_results = []

    index = 0
    results = {"Result": []}
    # Loop through every file in the clips folder
    for clip_index, filename in enumerate(sorted(os.listdir(clips_folder))):
        if not filename.lower().endswith((".mp4", ".mkv")):
            continue

        # if index == 3:
        #     break
        index += 1

        clip_path = os.path.join(clips_folder, filename)
        shot_clip = cv2.VideoCapture(clip_path)
        if not shot_clip.isOpened():
            print(f"[!] Could not open clip #{clip_index}: {filename}")
            continue

        print(f"→ Processing clip #{clip_index}: {filename}")

        min_distance = float("inf")
        best_frame = None
        best_bat_center = None
        frame_count = 0

        # Read through the clip frame-by-frame
        while True:
            ret, frame = shot_clip.read()
            if not ret:
                break
            frame_count += 1

            # Run YOLO inference
            results = model(frame)
            bat_center, ball_center = None, None

            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                    if class_id == 34:  # Bat
                        bat_center = (cx, cy)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.circle(frame, bat_center, 5, (255, 0, 0), -1)
                        cv2.putText(frame, "Bat", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    elif class_id == 32:  # Ball
                        ball_center = (cx, cy)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, ball_center, 5, (0, 255, 0), -1)
                        cv2.putText(frame, "Ball", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if bat_center and ball_center:
                    distance = np.hypot(bat_center[0] - ball_center[0],
                                        bat_center[1] - ball_center[1])

                    cv2.putText(frame, f"Distance: {distance:.2f}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    if distance < min_distance:
                        min_distance = distance
                        best_frame = frame.copy()
                        best_bat_center = bat_center

                cv2.imshow(f"Tracking Bat and Ball of clip no:{index}", frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break

        shot_clip.release()

        # If we found a best frame, run angle processing
        if best_frame is not None:
            print(f"  • Best distance {min_distance:.1f}px in clip #{clip_index}")
            angles_dict, annotated_img = angles.processing_image_using_mediapipe(
                best_frame, best_bat_center, stance="right"
            )
            print("\nin proceessing_video, shot_name, angles_dict, coach_id is:", shot_name, angles_dict, coach_id)
            shot_results = CoachController.compare_shot_angles(shot_name, angles_dict, coach_id)
            result = CoachController.add_shot_result(shot_results, session_id, annotated_img, filename)
            results["Result"].append(result)

            list_of_results.append({
                "clip_name": filename,
                "angles": angles_dict,
                "image": annotated_img
            })
        else:
            print(f"  ⚠️ No valid bat-ball pair in clip #{clip_index}")

    cv2.destroyAllWindows()
    return results


def process_video1(video_path, session_id, shot_name):
    """
    Process the video to find the frame where the bat and ball are closest,
    analyzing only every 10th frame per 60 fps for optimization.

    :param video_path: Path to the input video.
    :return: Angle analysis on the best frame.
    """
    cap = cv2.VideoCapture(video_path)
    print("in process_video, cap is:", cap)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames_to_skip = 0
    # frames_to_skip = int((0 / 100) * fps)

    if not cap.isOpened():
        print(f"Error: Unable to open video at path '{video_path}'")
        return None

    # fps = int(cap.get(cv2.CAP_PROP_FPS))  # Typically 60
    # frames_to_skip = int(fps / 6)  # Process 6 frames per second

    print("Total frames:", fps)
    print("Frames to skip:", frames_to_skip)

    frames_per_clip = 1 * fps
    # list_of_clips = []

    min_distance = float('inf')
    best_frame = None
    best_bat_center = None
    frame_count = 0

    index = 0
    frames = []
    clip_index = 0

    list_of_results = []
    # while True:
    #     print(f"clip no: {clip_index}")
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     frames.append(frame)
    #
    #     index += 1
    #     print(f"Frame no:{index}")
    #     if index == frames_per_clip:
    #         index = 0
    #         clip_index += 1
    #         save_clip(frames, rf"Videos\Clips\{shot_name}-{session_id}-{clip_index}.mp4", fps)     # output_path, fps
    #         frames = []
    cap.release()

    index = 0

    clips_folder = r"Videos\Clips"
    for filename in os.listdir(clips_folder):
        if filename.endswith((".mp4", ".mkv")):
            video_clip_path = os.path.join(clips_folder, filename)

            shot_clip = cv2.VideoCapture(video_clip_path)
            if not shot_clip.isOpened():
                print(f"Error: Unable to open clip no:{index + 1}")

            if index == 3:
                break

            while True:
                frame_count += 1
                ret, frame = shot_clip.read()
                if not ret:
                    break

                # Skip frames to reduce processing
                # if frame_count % frames_to_skip != 0:
                #     continue
                results = model(frame)
                bat_center, ball_center = None, None

                print("bat_center", bat_center)

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

                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break

                if best_frame is not None:
                    print(f"Best frame found after processing {frame_count} frames.")
                    print(f"Bat center at closest approach: {best_bat_center}")
                    # cv2.imshow("img", img)
                    # cv2.imshow("best_frame", best_frame)
                    # cv2.waitKey(0)
                    # print('sending frame')

                    # mediapipe_angles, mediapipe_image = angles.processing_image_using_mediapipe(best_frame, best_bat_center, stance="right")
                    # yolo_angles, yolo_image = angles.processing_image_using_yolo(best_frame, best_bat_center, stance="right")
                    # combined_image = np.hstack((mediapipe_image, yolo_image))
                    #
                    # # Display
                    # cv2.imshow("MediaPipe Detection vs YOLO Detection", combined_image)
                    # cv2.waitKey(0)

                    # return mediapipe_angles, yolo_angles
                    all_angles, image = angles.processing_image_using_mediapipe(best_frame, best_bat_center,
                                                                                stance="right")
                    list_of_results.append({'angles': all_angles, 'image': image})
                    index += 1

                    # all_angles, image = angles.processing_image_using_yolov11(best_frame, best_bat_center, stance="right")
                    # return all_angles
                    # return angles.processing_image_using_mediapipe(best_frame, best_bat_center, stance="right")
                else:
                    print(f"No frame with both bat and ball detected for this clip no {index + 1}.")

    shot_clip.release()
    cv2.destroyAllWindows()

    return list_of_results

# <----------------------------------------------------------------------------->
# <----------------------------------------------------------------------------->
# <----------------------------------------------------------------------------->


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
