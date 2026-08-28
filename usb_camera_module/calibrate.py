import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.fonts.warning=false"
import numpy as np
import cv2
import glob

def calibrate_camera():
    checkerboard_sizes = [(9, 6), (8, 6), (7, 5), (9, 7)]
    images = glob.glob('calibration_images/*.jpg') + glob.glob('calibration_images/*.png')

    if not images:
        print("Error: No calibration images found in 'calibration_images/'!")
        return

    print(f"Found {len(images)} images. Auto-detecting checkerboard pattern...")
    chosen_pattern = None
    gray = None

    for fname in images:
        img = cv2.imread(fname)
        if img is None: continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for CHECKERBOARD in checkerboard_sizes:
            ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, 
                cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK)
            if ret:
                chosen_pattern = CHECKERBOARD
                break
        if chosen_pattern: break

    if not chosen_pattern:
        print("Error: Could not match any checkerboard pattern. Ensure the full grid is clear and well-lit in multiple images.")
        return

    print(f"Matched checkerboard size: {chosen_pattern}")
    objp = np.zeros((chosen_pattern[0] * chosen_pattern[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chosen_pattern[0], 0:chosen_pattern[1]].T.reshape(-1, 2)

    objpoints, imgpoints = [], []
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chosen_pattern, None)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
            print(f" -> Processed: {fname}")
        else:
            print(f" -> Skipped (Pattern not found): {fname}")

    if not objpoints:
        print("Error: Calibration failed. No valid corners extracted.")
        return

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez("calib_data.npz", mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    print(f"\nCalibration successful using {len(objpoints)} valid images! Saved data to 'calib_data.npz'")

if __name__ == "__main__":
    calibrate_camera()
