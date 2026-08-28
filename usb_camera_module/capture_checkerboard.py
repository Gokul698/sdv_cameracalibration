import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.fonts.warning=false"
import cv2

def find_first_camera():
    for i in range(4):
        cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                return i
    return None

def main():
    cam_index = find_first_camera()
    if cam_index is None:
        print("Error: No working USB cameras found.")
        return

    cap = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
    save_dir = "calibration_images"
    os.makedirs(save_dir, exist_ok=True)
    
    existing_files = os.listdir(save_dir) if os.path.exists(save_dir) else []
    img_counter = len([f for f in existing_files if f.endswith(('.png', '.jpg'))])
    
    print(f"\n[INFO] Press SPACE to capture checkerboard. Press 'q' to quit.")
    print(f"[INFO] Saving images into '{save_dir}/' starting at index {img_counter}\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("USB Capture - Press SPACE to Save", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord(' '):
            img_name = os.path.join(save_dir, f"img_{img_counter:02d}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"Saved: {img_name}")
            img_counter += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
