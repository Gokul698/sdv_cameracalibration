import cv2
import os
import glob

def find_usb_camera():
    # Dynamically find any working camera that isn't a RealSense metadata channel
    for path in glob.glob('/dev/video*'):
        idx = int(''.join(filter(str.isdigit, path)))
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Standard USB cameras typically have a valid color frame width >= 640
                h, w = frame.shape[:2]
                if w >= 640:
                    cap.release()
                    print(f"[INFO] Auto-detected USB Camera at index {idx} ({w}x{h})")
                    return idx
            cap.release()
    return 0 # Fallback default

def main():
    cam_idx = find_usb_camera()
    cap = cv2.VideoCapture(cam_idx, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    os.makedirs("calibration_images", exist_ok=True)
    img_count = len(glob.glob("calibration_images/*.jpg"))

    print(f"[INFO] Calibration Capture active using device index {cam_idx}.")
    print("[INFO] Press 's' to save a chessboard snapshot, or 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame from camera.")
            break

        cv2.imshow("Calibration Capture - Press 's' to save", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = f"calibration_images/img_{img_count:02d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"[SAVED] {filename}")
            img_count += 1
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
