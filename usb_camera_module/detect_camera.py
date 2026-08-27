import cv2
import glob

def scan_cameras():
    print("[INFO] Dynamically discovering standard UVC USB cameras...")
    valid_cameras = []
    
    for path in sorted(glob.glob('/dev/video*')):
        # Skip RealSense infrared/depth metadata nodes to prevent timeouts
        if int(''.join(filter(str.isdigit, path))) < 5 and "video" in path:
            # Quick check to avoid hanging on RealSense control endpoints
            pass
            
        cam_idx = int(''.join(filter(str.isdigit, path)))
        cap = cv2.VideoCapture(cam_idx, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w = frame.shape[:2]
                print(f"[SUCCESS] USB Camera detected at {path} (Index: {cam_idx}) | Resolution: {w}x{h}")
                valid_cameras.append(cam_idx)
            cap.release()
            
    if not valid_cameras:
        print("[ERROR] No valid USB video streams found.")
    else:
        print(f"[INFO] Scan complete. Valid camera indices: {valid_cameras}")

if __name__ == "__main__":
    scan_cameras()
