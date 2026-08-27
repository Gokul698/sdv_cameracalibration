import cv2
import pyrealsense2 as rs
import glob

def check_usb_camera():
    # Use smart reverse-scanning to find the UVC USB camera dynamically
    for path in sorted(glob.glob('/dev/video*'), reverse=True):
        idx = int(''.join(filter(str.isdigit, path)))
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w = frame.shape[:2]
                if w >= 640:
                    cap.release()
                    return True, f"ONLINE (Index {idx} - {w}x{h})"
            cap.release()
    return False, "OFFLINE"

def check_realsense():
    try:
        ctx = rs.context()
        devices = ctx.query_devices()
        if len(devices) > 0:
            dev = devices[0]
            name = dev.get_info(rs.camera_info.name)
            usb_type = dev.get_info(rs.camera_info.usb_type_descriptor)
            return True, f"ONLINE ({name} | USB {usb_type})"
    except Exception as e:
        pass
    return False, "OFFLINE"

def main():
    print("[INFO] Initializing Combined Session 4 Diagnostics (Dynamic Mode)...")
    
    usb_status_bool, usb_msg = check_usb_camera()
    rs_status_bool, rs_msg = check_realsense()
    
    print("-" * 50)
    print(f" Full HD USB Camera Status : {usb_msg}")
    print(f" Intel RealSense D435i Status: {rs_msg}")
    print("-" * 50)
    
    print("[INFO] Sensor validation diagnostics complete.")

if __name__ == "__main__":
    main()
