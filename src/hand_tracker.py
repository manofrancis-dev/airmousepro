import cv2
import mediapipe as mp

class HandTracker:
    """High-Precision MediaPipe Hand Tracker with High Model Complexity"""
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        
        # Max Accuracy & Tracking Stability Settings
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,           # Ultra High Accuracy Landmark Detection
            min_detection_confidence=0.8,  # High Confidence threshold
            min_tracking_confidence=0.8
        )

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb_frame)