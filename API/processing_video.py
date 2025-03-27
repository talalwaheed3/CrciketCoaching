import cv2
from ultralytics import YOLO
import numpy as np
from API import angles

# Load the YOLOv8 model
model = YOLO('yolov8x.pt')


def process_video(video_path):
    """
    Process the video to find the frame where the bat and ball are closest.

    :param video_path: Path to the input video.
    :return: The frame with the shortest Euclidean distance between bat and ball.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Unable to open video at path '{video_path}'. Please check the file path.")
        return None

    min_distance = float('inf')  # Initialize with a large value
    best_frame = None  # Variable to store the best frame
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:  # If no frame is returned, end of video
            break

        frame_count += 1

        # Run inference on the frame
        results = model(frame)

        # Extract bat and ball positions
        bat_center, ball_center = None, None
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])  # Class ID
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2  # Center of the bounding box

                # Assign the center coordinates based on class
                if class_id == 34:  # Class 34 is bat
                    bat_center = (center_x, center_y)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue for bat
                    cv2.circle(frame, bat_center, 5, (255, 0, 0), -1)
                    cv2.putText(frame, "Bat", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                elif class_id == 32:  # Class 32 is ball
                    ball_center = (center_x, center_y)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green for ball
                    cv2.circle(frame, ball_center, 5, (0, 255, 0), -1)
                    cv2.putText(frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Calculate Euclidean distance if both bat and ball are detected
        if bat_center and ball_center:
            distance = np.sqrt((bat_center[0] - ball_center[0]) ** 2 + (bat_center[1] - ball_center[1]) ** 2)

            # Annotate distance on the frame
            cv2.putText(frame, f"Distance: {distance:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Update the best frame if a shorter distance is found
            if distance < min_distance:
                min_distance = distance
                best_frame = frame.copy()

        # Show the frame with annotations
        cv2.imshow("Tracking Bat and Ball", frame)

        # Press 'q' to exit the video early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if best_frame is not None:
        print(f"Best frame found after processing {frame_count} frames.")
    else:
        print("No frame with both bat and ball detected.")

    return angles.processing_image(best_frame, min_distance)


# Example usage
# video_path = r"./videos/Babar Azam Best Cover Drives.mp4"  # Replace with your input video path
# best_frame = process_video(video_path)
#
# if best_frame is not None:
#     # Save or process the best frame further
#     output_image_path = r"best_frame.jpg"
#     cv2.imwrite(output_image_path, best_frame)
#     print(f"Best frame saved as {output_image_path}.")
# else:
#     print("No suitable frame found.")
