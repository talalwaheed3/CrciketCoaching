🏏 Gesture-Based Cricket Coaching System
This project is a Cricket Shot Analysis System that automatically evaluates a batsman's technique by analyzing their body posture during cricket shots (like Cover Drive, Pull Shot, Straight Drive, Sweep).
It uses computer vision models to detect body landmarks and calculate joint angles, providing feedback based on ideal standards.

# 📚Project Overview

**Body Detection:**

YOLOv11 Pose Model and MediaPipe Pose are used to detect key body points.

**Shot Analysis:**

Calculates important joint angles (elbow, wrist, shoulder-inclination, hip, knee).

Measures bat-to-hip distance for bat position analysis((for correcting the ideal distance of bat frome the body)).

**Comparison:**

Compares player's angles to ideal angle ranges based on professional players' datasets.

Identifies incorrect posture and suggests corrections.

**Visualization:**

Draws landmarks and angles on images for visual feedback.

Displays side-by-side results from YOLOv8(bat-ball detection for finding the best frame for angle calculation) and MediaPipe(for drawing landmarks on the 'best frmae' coming from the Yolov8 model).

**🛠️ Technologies Used:**
Python 3.11

OpenCV

MediaPipe

Numpy

Ultralytics YOLOv8

Flask (Backend API)

📂 Project Structure:

API/

├── app.py                # Main Flask application

├── processing_video.py   # Video processing and frame extraction using Yolov8

├── angles.py             # Angle calculations and pose detection using Mediapipe

├── templates/            # (Optional) For Flask frontend



🚀 **How to Run**
Install required libraries:

pip install opencv-python mediapipe torch ultralytics flask
Download YOLOv11 pose model (yolov11x-pose.pt) and place it in the project folder.

**Run the application:**

python app.py
Use the Flask endpoints or directly run the processing scripts to analyze a cricket shot video.

**✨ Features**
- Dual-model comparison: YOLO vs MediaPipe landmark detection.

- Real-time or pre-recorded video analysis.

- Detection of improper postures with suggestions for improvement.

- Extensible to other cricket shots in the future.

- Train custom YOLOv11 model fine-tuned on cricket players for further improving accuracy of our Ground Truth of our Model.

- Each Coach can add their own Ideal angles(Ground Truth) to test their player on.

Some Visual Dashboard Representation: 

# Arranged Sessions (For Live recording or uploading videos of different Sessions)
![12](https://github.com/user-attachments/assets/ed0ce033-f794-4461-8068-95178abf703e)  

# Selecting a shot video
![13](https://github.com/user-attachments/assets/25824917-b12c-4dc2-bd58-35917ee0c9d3)  

 # Resulting "best frame" of with euclidean distance of bat-ball
![14](https://github.com/user-attachments/assets/f1b1837e-bf7c-4d6f-99a6-e5c758d9a7ad) 

# Drawing landmarks of that 'best frame' and calculating angles
![15](https://github.com/user-attachments/assets/d08b27eb-279f-4015-8174-08d355a5736d)  

# Showing results
-- Angle Results Table
<img width="1895" height="844" alt="18" src="https://github.com/user-attachments/assets/a8c6063d-f9e4-49f8-9b17-593f26cafa7b" />

-- Best Frame of the player's shot
<img width="1896" height="846" alt="19" src="https://github.com/user-attachments/assets/b30e8d40-846b-4315-bcf3-a953c9dbe35c" />

-- Corresponding Shot Tutorial for improving performance
<img width="1895" height="842" alt="20" src="https://github.com/user-attachments/assets/3aebc760-f9ed-4dc0-849b-cb17edfa0a85" />
