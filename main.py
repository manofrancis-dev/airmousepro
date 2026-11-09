import os
import sys
import threading
import time


# Compatibility fix for older MediaPipe Solutions with newer protobuf.
# Keeps the existing gesture/mouse logic unchanged.
try:
    from google.protobuf import symbol_database, message_factory

    if not hasattr(symbol_database.SymbolDatabase, "GetPrototype"):
        def _get_prototype(self, descriptor):
            return message_factory.GetMessageClass(descriptor)
        symbol_database.SymbolDatabase.GetPrototype = _get_prototype

    if not hasattr(message_factory.MessageFactory, "GetPrototype"):
        def _factory_get_prototype(self, descriptor):
            return message_factory.GetMessageClass(descriptor)
        message_factory.MessageFactory.GetPrototype = _factory_get_prototype
except Exception:
    pass

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
import pystray
from PIL import Image, ImageDraw

from src.config_manager import ConfigManager
from src.gesture_engine import GestureEngine


class AirMouseApp:
    """Background AirMouse app with a Windows system-tray Exit control."""

    def __init__(self):
        self.stop_event = threading.Event()
        self.worker = threading.Thread(
            target=self._run_camera,
            name="AirMouseCamera",
            daemon=True,
        )
        self.icon = None
        self.engine = None
        self.cap = None

    @staticmethod
    def _create_tray_image():
        """Create a small tray icon without requiring a separate .ico file."""
        image = Image.new("RGBA", (64, 64), (18, 18, 18, 255))
        draw = ImageDraw.Draw(image)

        # Simple hand/cursor-style symbol.
        draw.ellipse((10, 10, 54, 54), outline=(0, 220, 140, 255), width=4)
        draw.ellipse((27, 14, 37, 24), fill=(0, 220, 140, 255))
        draw.line((32, 20, 32, 44), fill=(255, 255, 255, 255), width=5)
        draw.line((32, 44, 45, 51), fill=(255, 255, 255, 255), width=5)
        draw.line((32, 38, 20, 45), fill=(255, 255, 255, 255), width=5)
        return image

    def _run_camera(self):
        config = ConfigManager()
        cap = cv2.VideoCapture(config.cam_index)
        self.cap = cap

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.cam_height)

        if not cap.isOpened():
            return

        engine = GestureEngine(config)
        self.engine = engine

        try:
            while not self.stop_event.is_set() and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.01)
                    continue

                img_h, img_w, _ = frame.shape
                # Preview remains intentionally disabled.
                engine.process_frame(frame, img_w, img_h)
        finally:
            cap.release()
            if engine.mouse.is_left_down:
                engine.mouse.release_left()
            cv2.destroyAllWindows()
            self.cap = None
            self.engine = None

    def _exit(self, icon, _item):
        self.stop_event.set()

        if self.cap is not None:
            self.cap.release()

        if self.worker.is_alive():
            self.worker.join(timeout=3)

        icon.stop()

    def run(self):
        self.worker.start()

        menu = pystray.Menu(
            pystray.MenuItem(
                "AirMouse Pro",
                None,
                enabled=False,
            ),
            pystray.MenuItem(
                "Exit",
                self._exit,
            ),
        )

        self.icon = pystray.Icon(
            "AirMousePro",
            self._create_tray_image(),
            "AirMouse Pro - Running",
            menu,
        )
        self.icon.run()


def main():
    app = AirMouseApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop_event.set()
    finally:
        if app.worker.is_alive():
            app.worker.join(timeout=3)


if __name__ == "__main__":
    main()
