import cv2
import numpy as np
import os

def main():
    if not os.path.exists("calib_data.npz"):
        print("Error: 'calib_data.npz' not found! Run calibrate.py first.")
        return

    with np.load("calib_data.npz") as X:
        mtx, dist = [X[i] for i in ('mtx', 'dist')]

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Running Live Undistort. Press 'q' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret: break

        h, w = frame.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)

        x, y, w, h = roi
        if w > 0 and h > 0:
            dst = dst[y:y+h, x:x+w]

        cv2.imshow("Original Frame", frame)
        cv2.imshow("Undistorted Frame", dst)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
