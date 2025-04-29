🏏 Gesture-Based Cricket Coaching System
This project is a Cricket Shot Analysis System that automatically evaluates a batsman's technique by analyzing their body posture during cricket shots (like Cover Drive, Pull Shot, Straight Drive, Sweep).
It uses computer vision models to detect body landmarks and calculate joint angles, providing feedback based on ideal standards.

📚 Project Overview
**Body Detection**:

YOLOv11 Pose Model and MediaPipe Pose are used to detect key body points.

Shot Analysis:

Calculates important joint angles (elbow, wrist, shoulder, hip, knee).

Measures bat-to-hip distance for bat position analysis.

Comparison:

Compares player's angles to ideal angle ranges based on professional players' datasets.

Identifies incorrect posture and suggests corrections.

Visualization:

Draws landmarks and angles on images for visual feedback.

Displays side-by-side results from YOLO and MediaPipe.

🛠️ Technologies Used
Python 3.11

OpenCV

MediaPipe

Ultralytics YOLOv11

Flask (Backend API)

Torch (PyTorch)

📂 Project Structure
