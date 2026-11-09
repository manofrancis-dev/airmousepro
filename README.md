# AirMouse Pro 🖐️🖱️

**Control your Windows PC with webcam-based hand gestures.**

AirMouse Pro gives your Windows PC a touch-free control layer using computer vision (MediaPipe & OpenCV). Move the cursor with your index finger, pinch to click or drag, scroll smoothly with two fingers, and exit cleanly from the Windows system tray.

🌐 **Website & Documentation:** [https://manofrancis-dev.github.io/airmousepro/](https://manofrancis-dev.github.io/airmousepro/)  
📦 **Releases:** [GitHub Releases](https://github.com/manofrancis-dev/airmousepro/releases)

---

## 🚀 Installation & Running

Choose whichever installation path works best for you:

### Path A: Pre-built Windows Installer (.exe)
1. Download `AirMousePro_Setup_v1.0.0.exe` from the [Latest Release](https://github.com/manofrancis-dev/airmousepro/releases/latest) or from the [official website](https://manofrancis-dev.github.io/airmousepro/).
2. Run the installer and follow the on-screen setup wizard.
3. Launch **AirMouse Pro** from the Start Menu or desktop shortcut.

> **Note on Windows SmartScreen / Smart App Control:**  
> Since community releases are unsigned, Windows SmartScreen may show a prompt ("Windows protected your PC"). Click **More info → Run anyway**. If your Windows 11 system has **Smart App Control** enabled in strict mode (which blocks unsigned binaries completely), please use **Path B (Run from source)** below, as Smart App Control does not block Python scripts.

---

### Path B: Run from Source (Python)

Running directly from source gives you full transparency, requires no unverified `.exe`, and works seamlessly even when Smart App Control is enabled.

#### 1. Prerequisites
- **Windows 10 / 11 (64-bit)**
- **Webcam** (built-in or USB)
- **Python 3.10 – 3.12 (64-bit)**: Download from [python.org](https://www.python.org/downloads/)  
  *(Make sure to check the box **"Add python.exe to PATH"** during installation!)*

#### 2. Download the App Source
Download the source archive directly:
- **[Download Source ZIP](https://github.com/manofrancis-dev/airmousepro/archive/refs/heads/main.zip)** and extract it to a folder.

*Or clone the repository with Git:*
```bash
git clone https://github.com/manofrancis-dev/airmousepro.git
cd airmousepro
```

#### 3. Install Dependencies
Open **Command Prompt** or **PowerShell** in the project directory and install the requirements:
```bash
python -m pip install -r requirements.txt
```

*Requirements include:*
- `opencv-python`
- `mediapipe`
- `protobuf`
- `pystray`
- `Pillow`

#### 4. Launch AirMouse Pro
Start the application:
```bash
python main.py
```

The app will initialize your webcam in the background and place an icon in the **Windows system tray**.

---

## ✋ Hand Gestures Quick Reference

| Gesture | Action | Description |
| :--- | :--- | :--- |
| **Index finger pointing** | Cursor Movement | Move cursor smoothly across screen with adaptive boundary margins. |
| **Pinch (Thumb + Index)** | Left Click / Drag | Pinch and release for click; hold pinch to drag & drop files/windows. |
| **Thumb + Middle finger pinch** | Right Click | Open context menus anywhere. |
| **Index + Middle finger up** | Scroll Wheel | Move hand up or down to scroll pages smoothly. |
| **System Tray Exit** | Exit Application | Right-click the AirMouse Pro tray icon and select **Exit**. |

---

## ⚙️ Configuration

Custom settings are located in `config/settings.json`:
```json
{
  "camera": {
    "device_index": 0,
    "width": 640,
    "height": 480
  },
  "mouse": {
    "smoothing_factor": 5,
    "frame_margin": 80,
    "pinch_threshold_px": 30
  }
}
```
- `device_index`: Change if you have multiple webcams (0 = default).
- `smoothing_factor`: Increase for smoother cursor movement; decrease for more immediate response.
- `frame_margin`: Active hand boundary padding for screen mapping.
- `pinch_threshold_px`: Distance in pixels between fingertips to trigger pinch clicks.

---

## 🛠️ Building the Standalone Executable

If you want to package the app into a standalone executable or installer yourself:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build with the included spec file:
   ```bash
   pyinstaller AirMousePro.spec
   ```
   The compiled executable will be located in `dist/AirMousePro/AirMousePro.exe`.
3. (Optional) To build the Inno Setup installer, compile `AirMousePro.iss` using Inno Setup 6.

---

## 📄 License & Author

Created by **Mano Francis** ([@manofrancis-dev](https://github.com/manofrancis-dev))  
- GitHub: [https://github.com/manofrancis-dev](https://github.com/manofrancis-dev)  
- LinkedIn: [https://in.linkedin.com/in/manofrancis-dev](https://in.linkedin.com/in/manofrancis-dev)  
- Portfolio: [https://manofrancis-dev.github.io/manofrancis-portfolio/](https://manofrancis-dev.github.io/manofrancis-portfolio/)

© 2026 Mano Francis. All rights reserved.
