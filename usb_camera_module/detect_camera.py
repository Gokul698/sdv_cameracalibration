import cv2
import glob
import os

def scan_cameras():
    print("[INFO] Dynamically scanning all system video nodes for USB cameras...")
    
    # Automatically find all video devices on the system (e.g., /dev/video0, /dev/video1, etc.)
    video_paths = glob.glob('/dev/video*')
    # Sort them numerically so /dev/video2 comes before /dev/video10
    video_paths.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    
    valid_cameras = []
    
    for path in video_paths:
        # Extract the integer index from the path (e.g., '/dev/video6' -> 6)
        cam_idx = int(''.join(filter(str.isdigit, path)))
        
        cap = cv2.VideoCapture(cam_idx, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                # RealSense video nodes usually output specific raw/metadata streams or smaller control feeds,
                # whereas a standard USB webcam outputs standard image frames (like 640x480, 1280x720, or 1920x1080).
                # We log active frames and let you see which is your standard USB camera.
                print(f"[SUCCESS] Active video stream found at {path} (Index: {cam_idx}) | Resolution: {w}x{h}")
                valid_cameras.append(cam_idx)
            cap.release()
            
    if not valid_cameras:
        print("[ERROR] No readable video capture streams found.")
    else:
        print(f"[INFO] Universal scan complete. Discovered active indices: {valid_cameras}")

if __name__ == "__main__":
    scan_cameras()
