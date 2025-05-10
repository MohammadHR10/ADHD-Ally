import cv2
import time

def test_camera():
    print("Testing camera access...")
    # Try to open the default camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return False
    
    print("Camera opened successfully")
    
    # Try to read a frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        cap.release()
        return False
    
    print("Successfully captured a frame")
    print(f"Frame shape: {frame.shape}")
    
    # Release the camera
    cap.release()
    return True

if __name__ == "__main__":
    print("Starting camera test...")
    success = test_camera()
    if success:
        print("Camera test completed successfully!")
    else:
        print("Camera test failed!")