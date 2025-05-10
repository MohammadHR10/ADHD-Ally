import cv2
import time
from deepface import DeepFace

def test_camera():
    print("Testing the camera...")
    print("Please make sure you've granted camera permissions to your terminal/IDE")
    print("System Preferences -> Security & Privacy -> Camera")
    
    # Try to open the camera
    cap = cv2.VideoCapture(0)
    
    # Wait a moment for camera initialization
    time.sleep(2)
    
    if not cap.isOpened():
        print("\nError: Camera couldn't open")
        print("Possible reasons:")
        print("1. Camera permissions not granted")
        print("2. Camera is in use by another application")
        print("3. Camera hardware issue")
        return False
    
    print("\nCamera opened successfully")
    
    # Try to read a frame
    ret, frame = cap.read()
    if not ret:
        print("\nError: Could not capture frame")
        print("Please check if another application is using the camera")
        cap.release()
        return False
    
    print("\nFrame captured successfully")
    print(f"Frame dimensions: {frame.shape}")
    
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
    return True

if __name__ == "__main__":
    print("Starting camera test...")
    success = test_camera()
    if success:
        print("\nCamera test completed successfully!")
    else:
        print("\nCamera test failed!")
        print("Please check the error messages above for troubleshooting steps.")
        
        
    
