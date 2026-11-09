import ctypes
import math

class MouseController:
    """Win32 Mouse Controller with Dynamic Velocity Adaptive Precision"""
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_WHEEL = 0x0800

    def __init__(self, margin=80):
        self.user32 = ctypes.windll.user32
        self.screen_width = self.user32.GetSystemMetrics(0)
        self.screen_height = self.user32.GetSystemMetrics(1)
        self.margin = margin
        self.is_left_down = False

        self.prev_x = None
        self.prev_y = None

    def map_coordinates(self, cx, cy, img_w, img_h):
        clamped_x = max(self.margin, min(cx, img_w - self.margin))
        clamped_y = max(self.margin, min(cy, img_h - self.margin))
        
        target_x = (img_w - self.margin - clamped_x) / (img_w - 2 * self.margin) * self.screen_width
        target_y = (clamped_y - self.margin) / (img_h - 2 * self.margin) * self.screen_height
        return target_x, target_y

    def move(self, target_x, target_y):
        # MediaPipe landmarks naturally move by a few pixels even when the
        # hand is almost still. Ignore tiny cursor changes and use stronger
        # smoothing to prevent visible shake, especially during drag.
        if self.prev_x is None or self.prev_y is None:
            curr_x, curr_y = target_x, target_y
        else:
            dx = target_x - self.prev_x
            dy = target_y - self.prev_y
            distance = math.hypot(dx, dy)

            # Small tracking noise: keep the pointer still.
            if distance < 2.0:
                curr_x, curr_y = self.prev_x, self.prev_y
            else:
                # Smooth enough to suppress landmark jitter while retaining
                # responsive movement. Faster movement gets a higher response.
                if distance < 15:
                    smoothing = 0.22
                elif distance < 40:
                    smoothing = 0.35
                else:
                    smoothing = 0.50

                curr_x = self.prev_x + smoothing * dx
                curr_y = self.prev_y + smoothing * dy

        self.prev_x, self.prev_y = curr_x, curr_y
        self.user32.SetCursorPos(int(curr_x), int(curr_y))

    def press_left(self):
        if not self.is_left_down:
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            self.is_left_down = True

    def release_left(self):
        if self.is_left_down:
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            self.is_left_down = False

    def right_click(self):
        self.user32.mouse_event(self.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        self.user32.mouse_event(self.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def scroll(self, amount):
        self.user32.mouse_event(self.MOUSEEVENTF_WHEEL, 0, 0, amount, 0)