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
    print(f"[INFO] RealSense Device Active | USB Protocol: {usb_type}")

    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    align = rs.align(rs.stream.color)
    pipeline.start(config)
    print("[SUCCESS] Advanced pipeline active with alignment! Press 'q' to exit.")

    try:
        while True:
            frames = pipeline.wait_for_frames(timeout_ms=10000)
            aligned_frames = align.process(frames)

            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            if not depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            height, width, _ = color_image.shape
            cx, cy = int(width / 2), int(height / 2)
            distance_meters = depth_frame.get_distance(cx, cy)

            cv2.drawMarker(color_image, (cx, cy), (0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
            text = f"Distance: {distance_meters:.2f}m (USB {usb_type})"
            cv2.putText(color_image, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            combined = np.hstack((color_image, depth_colormap))

            cv2.imshow('D435i Aligned RGB (Left) | Depth (Right)', combined)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
