import cv2
import pyrealsense2 as rs

def main():
    print("[INFO] Initializing Combined Session 4 Diagnostics...")
    
    # Check USB Camera
    cap = cv2.VideoCapture(0)
    usb_status = "ONLINE" if cap.isOpened() else "OFFLINE"
    if cap.isOpened(): cap.release()

    # Check RealSense D435i
    ctx = rs.context()
    devices = ctx.query_devices()
    rs_status = f"ONLINE ({len(devices)} device(s))" if len(devices) > 0 else "OFFLINE"

    print("------------------------------------------")
    print(f" Full HD USB Camera Status : {usb_status}")
    print(f" Intel RealSense D435i Status: {rs_status}")
    print("------------------------------------------")
    print("[INFO] Sensor validation diagnostics complete.")

if __name__ == "__main__":
    main()
