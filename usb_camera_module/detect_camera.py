import cv2

def check_cameras():
    print("[INFO] Scanning for connected USB video devices...")
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"[SUCCESS] Camera detected at index: /dev/video{i}")
            cap.release()
        else:
            print(f"[DEBUG] No camera at index: {i}")

if __name__ == "__main__":
    check_cameras()
