# SDV Camera Calibration & Vision Fundamentals Workshop

Official codebase for **Session 4: Vision Fundamentals (Hands-On)** within the Software Defined Vehicle (SDV) curriculum.

## Repository Structure
```text
sdv_cameracalibration/
├── usb_camera_module/
│   ├── requirements.txt              # Dependencies for USB camera calibration
│   ├── detect_camera.py              # Step 1: Detect hardware index
│   ├── capture_checkerboard.py       # Step 2: Capture dataset images
│   ├── calibrate.py                  # Step 3: Compute K and distortion coefficients
│   ├── live_undistort.py             # Step 4: Live rectification display
│   └── README.md                     # Full HD USB Camera Module Documentation
├── realsense_module/
│   ├── requirements.txt              # Dependencies for RealSense SDK & pipelines
│   ├── realsense_stream.py           # Step 1: Basic RGB & Depth streams
│   ├── realsense_advanced.py         # Step 2: Alignment, distance lookup, point clouds
│   └── README.md                     # Intel RealSense D435i Module Documentation
└── combined_module/
    ├── requirements.txt              # Shared requirements for unified workspace
    ├── dual_sensor_inspector.py      # Unified script combining USB and D435i checks
    └── README.md                     # Combined System Documentation
```

## Step-by-Step Execution Guide

### 1. Virtual Environment Setup & Activation
```bash
python3 -m venv sdvai_env
source sdvai_env/bin/activate
pip install --upgrade pip
```

### 2. Track A: Full HD USB Camera Calibration
```bash
cd usb_camera_module
pip install -r requirements.txt
python3 detect_camera.py
python3 capture_checkerboard.py  # Press 's' to save snapshots, 'q' to quit
python3 calibrate.py             # Generates calib_data.npz
python3 live_undistort.py        # Live rectification validation
```

### 3. Track B: Intel RealSense D435i Workflow
```bash
cd ../realsense_module
pip install -r requirements.txt
python3 realsense_stream.py      # Basic RGB and Depth streams
python3 realsense_advanced.py    # Alignment and real-time distance lookup
```
