import cv2
import os
import glob

def get_usb_camera_index():
    # Start searching from higher video indices where UVC webcams usually sit on this board
    for path in sorted(glob.glob('/dev/video*'), reverse=True):
        idx = int(''.join(filter(str.isdigit, path)))
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w = frame.shape[:2]
                if w >= 640:
                    cap.release()
                    print(f"[INFO] Auto-selected USB Camera index: {idx} ({w}x{h})")
                    return idx
            cap.release()
    return 6 # Fallback to detected index 6

def main():
    cam_idx = get_usb_camera_index()
    cap = cv2.VideoCapture(cam_idx, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    os.makedirs("calibration_images", exist_ok=True)
    img_count = len(glob.glob("calibration_images/*.jpg"))

    print(f"[INFO] Capture session active on device index {cam_idx}. Press 's' to save, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
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
