import cv2
import numpy as np
import glob

def get_usb_camera_index():
    for path in sorted(glob.glob('/dev/video*')):
        idx = int(''.join(filter(str.isdigit, path)))
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w = frame.shape[:2]
                if w >= 640:
                    cap.release()
                    return idx
            cap.release()
    return 0

def main():
    try:
        data = np.load("calib_data.npz")
        mtx, dist = data['mtx'], data['dist']
    except IOError:
        print("[ERROR] 'calib_data.npz' not found! Run calibrate.py first.")
        return

    cam_idx = get_usb_camera_index()
    cap = cv2.VideoCapture(cam_idx, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    print(f"[INFO] Running live undistortion on index {cam_idx}. Press 'q' to quit.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
        dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)

        x, y, rw, rh = roi
        if rw > 0 and rh > 0:
            dst = dst[y:y+rh, x:x+rw]
            dst = cv2.resize(dst, (w, h))

        combined = np.hstack((frame, dst))
        cv2.imshow('Original Full HD (Left) vs Clean Undistorted (Right)', cv2.resize(combined, (1280, 480)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
