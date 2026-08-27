import pyrealsense2 as rs
import numpy as np
import cv2

def get_median_distance(depth_frame, x, y, radius=5):
    distances = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            d = depth_frame.get_distance(x + dx, y + dy)
            if d > 0:
                distances.append(d)
    return np.median(distances) if distances else 0.0

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)
    align = rs.align(rs.stream.color)

    print("[INFO] Advanced D435i Alignment & Distance Measurement active. Press 'q' to exit.")
    try:
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            color_image = np.asanyarray(color_frame.get_data())
            h, w, _ = color_image.shape
            cx, cy = w // 2, h // 2
            
            dist = get_median_distance(depth_frame, cx, cy, radius=5)

            cv2.circle(color_image, (cx, cy), 5, (0, 255, 0), -1)
            cv2.putText(color_image, f"Center Distance: {dist:.2f} m", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("D435i Aligned View with Real-Time Distance", color_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
