import os
import json

class ConfigManager:
    """Loads and manages configurations from JSON file"""
    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path
        self.cam_index = 0
        self.cam_width = 640
        self.cam_height = 480
        self.smoothing = 5
        self.margin = 80
        self.pinch_threshold = 30
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                    self.cam_index = data.get("camera", {}).get("device_index", 0)
                    self.cam_width = data.get("camera", {}).get("width", 640)
                    self.cam_height = data.get("camera", {}).get("height", 480)
                    self.smoothing = data.get("mouse", {}).get("smoothing_factor", 5)
                    self.margin = data.get("mouse", {}).get("frame_margin", 80)
                    self.pinch_threshold = data.get("mouse", {}).get("pinch_threshold_px", 30)
            except Exception as e:
                print(f"[ERROR] Config load failed: {e}. Using defaults.")
        else:
            print("[WARNING] Config file not found. Running on defaults.")