import numpy as np
import cv2
import glob

CHECKERBOARD = (9, 6)
square_size_m = 0.025  # 25mm physical square size

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= square_size_m

objpoints = []
imgpoints = []

images = glob.glob('calibration_images/*.jpg')
if not images:
    print("[ERROR] No calibration images found in 'calibration_images/' folder!")
    exit()

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
    else:
        print(f"[WARNING] Chessboard not found in {fname}")

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("\n[SUCCESS] Calibration Completed!")
print("Camera Matrix (K):\n", mtx)
print("\nDistortion Coefficients:\n", dist)

np.savez("calib_data.npz", mtx=mtx, dist=dist)
print("\n[INFO] Saved calibration matrices to 'calib_data.npz'")
