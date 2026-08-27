import cv2
import os

def capture_images():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    os.makedirs("calibration_images", exist_ok=True)
    count = 0
    print("[INFO] Press 's' to capture frame, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame from USB camera.")
            break

        cv2.imshow("Calibration Capture - Press 's' to save", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = f"calibration_images/img_{count:02d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"[SAVED] {filename}")
            count += 1
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_images()
