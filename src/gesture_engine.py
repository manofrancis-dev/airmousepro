import cv2
import math
from collections import deque
from src.mouse_controller import MouseController
from src.hand_tracker import HandTracker

class GestureEngine:
    """Ultra-Focus Engine with Finger Trace Trail & Micro Target Crosshair"""
    def __init__(self, config):
        self.config = config
        self.tracker = HandTracker()
        self.mouse = MouseController(margin=config.margin)
        self.pinch_threshold = config.pinch_threshold
        
        self.right_click_cooldown = 0
        self.prev_scroll_y = None
        self.left_pinch_active = False
        
        # Neon Motion Trail Memory (Stores last 12 index finger coordinates)
        self.trace_points = deque(maxlen=12)

    def process_frame(self, frame, img_w, img_h):
        frame = cv2.flip(frame, 1)
        results = self.tracker.process(frame)
        status_text = "ULTRA FOCUS ACTIVE"

        if not results.multi_hand_landmarks:
            if self.mouse.is_left_down:
                self.mouse.release_left()
            self.left_pinch_active = False
            self.prev_scroll_y = None
            self.trace_points.clear()
            cv2.putText(frame, "STATUS: SEARCHING HAND...", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return frame

        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = hand_landmarks.landmark

        # 1. Render Full Hand Skeleton Connections (Visual Accuracy Mesh)
        self.tracker.mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            self.tracker.mp_hands.HAND_CONNECTIONS,
            self.tracker.mp_styles.get_default_hand_landmarks_style(),
            self.tracker.mp_styles.get_default_hand_connections_style()
        )

        # Key Finger Landmarks: 4=Thumb, 8=Index Tip, 12=Middle Tip
        thumb = landmarks[4]
        index = landmarks[8]
        middle = landmarks[12]

        tx, ty = int(thumb.x * img_w), int(thumb.y * img_h)
        ix, iy = int(index.x * img_w), int(index.y * img_h)
        mx, my = int(middle.x * img_w), int(middle.y * img_h)

        # Append Index position for neon tracing
        self.trace_points.appendleft((ix, iy))

        # Cursor Position Calculation
        raw_ix = img_w - ix 
        target_x, target_y = self.mouse.map_coordinates(raw_ix, iy, img_w, img_h)
        self.mouse.move(target_x, target_y)

        # Distances
        index_thumb_dist = math.hypot(ix - tx, iy - ty)
        middle_thumb_dist = math.hypot(mx - tx, my - ty)
        index_middle_dist = math.hypot(ix - mx, iy - my)

        if self.right_click_cooldown > 0:
            self.right_click_cooldown -= 1

        # --- GESTURE LOGIC ---
        if middle_thumb_dist < self.pinch_threshold and self.right_click_cooldown == 0:
            self.mouse.right_click()
            self.right_click_cooldown = 15
            status_text = "RIGHT CLICK"

        # Use hysteresis for the left pinch so tiny landmark noise does not
        # repeatedly press/release the mouse while dragging.
        pinch_release_threshold = self.pinch_threshold + 7
        if self.left_pinch_active:
            if index_thumb_dist > pinch_release_threshold:
                self.left_pinch_active = False
                self.mouse.release_left()
            else:
                self.mouse.press_left()
                status_text = "DRAG / LEFT CLICK"
        elif index_thumb_dist < self.pinch_threshold:
            self.left_pinch_active = True
            self.mouse.press_left()
            status_text = "DRAG / LEFT CLICK"
        else:
            self.mouse.release_left()

        if index_middle_dist < 45 and index_thumb_dist > self.pinch_threshold:
            if self.prev_scroll_y is not None:
                dy = self.prev_scroll_y - iy
                if abs(dy) > 4:
                    self.mouse.scroll(int(dy * 12))
                    status_text = "SCROLLING"
            self.prev_scroll_y = iy
        else:
            self.prev_scroll_y = None

        # --- ULTRA FOCUS VISUAL TRACE & TARGET HUD ---

        # A. Draw Neon Motion Trail behind Index Finger
        for i in range(1, len(self.trace_points)):
            if self.trace_points[i - 1] is None or self.trace_points[i] is None:
                continue
            thickness = int(math.sqrt(12 / float(i + 1)) * 2.5)
            cv2.line(frame, self.trace_points[i - 1], self.trace_points[i], (0, 255, 255), thickness)

        # B. Target Crosshair / Reticle Scope over Index Finger Tip
        cv2.circle(frame, (ix, iy), 12, (0, 255, 0), 2)
        cv2.line(frame, (ix - 18, iy), (ix + 18, iy), (0, 255, 0), 1)
        cv2.line(frame, (ix, iy - 18), (ix, iy + 18), (0, 255, 0), 1)

        # C. Status Display
        cv2.putText(frame, f"MODE: {status_text}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return frame