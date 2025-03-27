import cv2 as cv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

cap = cv.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image = cv.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        print(results)
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hand.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 70), thickness=3, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=3)
                                          )
        cv.imshow("Hand Tracking", image)
        if cv.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv.destroyAllWindows()
