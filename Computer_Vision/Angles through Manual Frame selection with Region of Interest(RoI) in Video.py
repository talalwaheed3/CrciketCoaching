import cv2 as cv
import mediapipe as mp
import numpy as np


video = cv.VideoCapture("../Videos/Reverse Sweep Shot/reverse sweep shot-1.mp4")
while video.isOpened():
    isTrue, frame = video.read()
    cv.imshow("Reverse Sweep Shot-1", frame)
    if cv.waitKey(50) & 0xFF == ord("q"):
        break




