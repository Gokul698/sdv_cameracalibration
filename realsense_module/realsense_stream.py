import pyrealsense2 as rs
import numpy as np
import cv2

def main():
    ctx = rs.context()
    devices = ctx.query_devices()
    if len(devices) == 0:
        print("[ERROR] No Intel RealSense device detected.")
        return
    
    dev = devices[0]
    usb_type = dev.get_info(rs.camera_info.usb_type_descriptor)
    print(f"[INFO] Connected RealSense: {dev.get_info(rs.camera_info.name)} (USB Type: {usb_type})")

    pipeline = rs.pipeline()
    config = rs.config()

    # Universal configuration profile safe for both USB 2.0 and USB 3.0
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)
    print("[SUCCESS] RealSense stream active. Press 'q' to exit.")

    try:
        while True:
            frames = pipeline.wait_for_frames(timeout_ms=10000)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            images = np.hstack((color_image, depth_colormap))

            cv2.imshow(f'RealSense D435i (USB {usb_type}) - Color (Left) | Depth (Right)', images)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
