import cv2
import numpy as np

try:
    data = np.load("calib_data.npz")
    mtx, dist = data['mtx'], data['dist']
except IOError:
    print("[ERROR] 'calib_data.npz' not found! Run calibrate.py first.")
    exit()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print("[INFO] Running cropped live undistortion window. Press 'q' to quit.")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    # alpha=0 crops the black borders completely
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)

    # Crop to valid region if ROI is returned
    x, y, rw, rh = roi
    if rw > 0 and rh > 0:
        dst = dst[y:y+rh, x:x+rw]
        # Resize dst to match frame height for side-by-side stack visualization
        dst = cv2.resize(dst, (w, h))

    combined = np.hstack((frame, dst))
    cv2.imshow('Original Full HD (Left) vs Clean Undistorted (Right)', cv2.resize(combined, (1280, 480)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
