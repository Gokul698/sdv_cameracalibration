import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.fonts.warning=false"
import cv2

def find_available_cameras(max_tested=4):
    available_cameras = []
    print("Scanning for available USB cameras...")
    for i in range(max_tested):
        cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f" -> Working USB camera found at index {i}")
                available_cameras.append(i)
            cap.release()
    return available_cameras

def main():
    cameras = find_available_cameras()
    if not cameras:
        print("Error: No active USB cameras detected!")
        return

    cam_index = cameras[0]
    print(f"Using camera index: {cam_index}. Press 'q' to exit.")
    cap = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(f"USB Camera Feed (Index {cam_index})", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
