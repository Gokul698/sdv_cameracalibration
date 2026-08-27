# Full HD USB 2.0 Camera Calibration Module

## Workflow Instructions
1. Activate environment: `source ../sdvai_env/bin/activate`
2. Run hardware scan: `python3 detect_camera.py`
3. Collect dataset: `python3 capture_checkerboard.py` (Press **s** to capture 15-25 angles, **q** to quit)
4. Calibrate: `python3 calibrate.py` (Outputs `calib_data.npz`)
5. Validate via live rectification: `python3 live_undistort.py`
