# 🖱️ Virtual Mouse Using Hand Gesture

A computer vision-based **Virtual Mouse** that allows users to control the computer mouse using **hand gestures** through a webcam.

The project uses **Python, OpenCV, MediaPipe, NumPy, and PyAutoGUI** to detect hand landmarks and translate specific finger gestures into mouse actions.

## ✨ Features

* 🖱️ Move the mouse cursor using the index finger
* 👆 Perform left click using index + middle finger
* 👉 Perform right click using three fingers
* 📜 Scroll using two fingers
* ✋ Pause mouse control using an open palm
* 🎥 Real-time webcam hand tracking
* 📊 Displays current gesture mode and FPS
* ⚙️ Configurable sensitivity and gesture thresholds

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – Webcam capture and image processing
* **MediaPipe** – Hand landmark detection
* **NumPy** – Coordinate mapping and calculations
* **PyAutoGUI** – Mouse control

## 📋 Gesture Controls

| Hand Gesture              | Action              |
| ------------------------- | ------------------- |
| ☝️ Index finger only      | Move cursor         |
| ✌️ Index + middle fingers | Left click / scroll |
| 🤟 Three fingers          | Right click         |
| 🖐️ Open palm             | Pause               |
| No recognized gesture     | Idle                |

### Left Click

Bring the **index finger and middle finger close together** to perform a left click.

### Scrolling

Keep the **index and middle fingers raised and separated**, then move the fingers vertically to scroll.

### Right Click

Raise **three fingers** to perform a right click.

### Pause

Show an **open palm** to temporarily pause mouse movement.

## 📁 Project Structure

```text
Virtual-Mouse/
│
├── virtual_mouse.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 💻 Requirements

* Python 3.9+
* Working webcam
* Windows / Linux / macOS
* Internet connection for installing dependencies

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Virtual-Mouse.git
```

### 2. Open the project folder

```bash
cd Virtual-Mouse
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Run the program

```bash
python virtual_mouse.py
```

A webcam window will open and start detecting your hand.

## 🎮 How to Use

1. Connect your webcam.
2. Run `virtual_mouse.py`.
3. Place your hand in front of the webcam.
4. Use the supported gestures to control the mouse.
5. Press **Q** to exit the application.

## ⚙️ Configuration

The project contains several settings that can be adjusted according to your webcam and preferred sensitivity.

```python
CAM_INDEX = 0
CAM_W, CAM_H = 640, 480
FRAME_MARGIN = 100
SMOOTHING = 6
CLICK_RATIO = 0.25
SCROLL_RATIO = 0.45
CLICK_COOLDOWN = 0.35
RIGHT_CLICK_COOLDOWN = 0.6
SCROLL_SPEED = 60
```

### Configuration Details

| Setting                | Purpose                              |
| ---------------------- | ------------------------------------ |
| `CAM_INDEX`            | Selects the webcam                   |
| `CAM_W`, `CAM_H`       | Webcam resolution                    |
| `FRAME_MARGIN`         | Defines the active hand-control area |
| `SMOOTHING`            | Controls cursor smoothness           |
| `CLICK_RATIO`          | Controls left-click finger distance  |
| `SCROLL_RATIO`         | Controls scroll gesture detection    |
| `CLICK_COOLDOWN`       | Prevents repeated left clicks        |
| `RIGHT_CLICK_COOLDOWN` | Prevents repeated right clicks       |
| `SCROLL_SPEED`         | Controls scrolling speed             |

## 🔍 How It Works

The application captures video frames from the webcam using OpenCV.

MediaPipe detects the hand and provides hand landmark coordinates. The program checks which fingers are raised and identifies the current gesture.

The index finger coordinates are converted from webcam coordinates to screen coordinates. PyAutoGUI then moves the system cursor to the corresponding position.

Simplified workflow:

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Detection
   ↓
Hand Landmark Detection
   ↓
Gesture Recognition
   ↓
Mouse Action
   ↓
Computer Screen
```

## 🧠 Gesture Detection Logic

The program identifies different hand states:

```text
Index finger only
        ↓
   Cursor Movement

Index + Middle fingers
        ↓
   Click / Scroll

Three fingers
        ↓
    Right Click

Open Palm
        ↓
      Pause
```

## ⚠️ Limitations

* Requires a working webcam.
* Performance depends on lighting conditions.
* Hand detection may become less accurate when the hand is partially outside the camera frame.
* Cursor movement can feel different depending on screen resolution and webcam position.
* Gesture recognition may require threshold adjustments for different users.

## 🔮 Future Improvements

Possible future enhancements include:

* Add double-click gesture
* Add drag-and-drop gesture
* Add volume control
* Add brightness control
* Add customizable gestures
* Support multiple hands
* Add a graphical settings interface
* Improve gesture stability
* Add voice commands
* Package the project as a standalone `.exe`

## 📜 License

This project is open-source and intended for educational and personal use.
