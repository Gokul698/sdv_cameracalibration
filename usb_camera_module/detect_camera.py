import cv2

def scan_cameras():
    print("[INFO] Dynamically scanning for active USB camera streams (Indices 0 to 5)...")
    available_cameras = []
    
    for i in range(6):
        cap = cv2.VideoCapture(i, cv2.CAP_ANY)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print(f"[SUCCESS] Active camera discovered at: /dev/video{i} (Resolution: {w}x{h})")
                available_cameras.append(i)
            cap.release()
            
    if not available_cameras:
        print("[ERROR] No active USB video capture devices found.")
    else:
        print(f"[INFO] Scan complete. Valid camera indices: {available_cameras}")

if __name__ == "__main__":
    scan_cameras()
