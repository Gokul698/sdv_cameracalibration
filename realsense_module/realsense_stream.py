import pyrealsense2 as rs
import numpy as np
import cv2

def main():
    pipeline = rs.pipeline()
    config = rs.config()

    # Enable depth stream only for stable USB 2.0 performance
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    print("[INFO] Starting RealSense Depth-only stream (USB 2.0 optimized)...")
    pipeline.start(config)
    print("[SUCCESS] Stream active! Press 'q' to exit.")

    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            
            if not depth_frame:
                continue

            # Convert depth to numpy array
            depth_image = np.asanyarray(depth_frame.get_data())

            # Apply colormap on depth image (Jet colormap)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            # Show depth map
            cv2.imshow('Intel RealSense D435i - Live Depth Map', depth_colormap)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
