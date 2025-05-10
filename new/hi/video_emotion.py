import cv2
import numpy as np
from deepface import DeepFace
from typing import Dict, List, Optional, Tuple
import threading
import time
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmotionResult:
    emotion: str
    confidence: float
    timestamp: datetime
    frame: Optional[np.ndarray] = None

class VideoEmotionRecognizer:
    def __init__(self, 
                 camera_id: int = 0,
                 detection_interval: float = 1.0,
                 save_frames: bool = False):
        """
        Initialize the video emotion recognizer
        
        Args:
            camera_id: ID of the camera to use (default: 0 for primary camera)
            detection_interval: Time between emotion detections in seconds
            save_frames: Whether to save frames with detected emotions
        """
        self.camera_id = camera_id
        self.detection_interval = detection_interval
        self.save_frames = save_frames
        self.cap = None
        self.is_running = False
        self.emotion_history: List[EmotionResult] = []
        self.current_emotion: Optional[EmotionResult] = None
        self._lock = threading.Lock()
        
    def start(self) -> None:
        """Start the video capture and emotion detection"""
        if self.is_running:
            return
            
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera")
            
        self.is_running = True
        self._detection_thread = threading.Thread(target=self._detection_loop)
        self._detection_thread.daemon = True
        self._detection_thread.start()
        
    def stop(self) -> None:
        """Stop the video capture and emotion detection"""
        self.is_running = False
        if self._detection_thread:
            self._detection_thread.join()
        if self.cap:
            self.cap.release()
            
    def _detection_loop(self) -> None:
        """Main detection loop that runs in a separate thread"""
        last_detection_time = 0
        
        while self.is_running:
            current_time = time.time()
            
            if current_time - last_detection_time >= self.detection_interval:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                    
                try:
                    # Convert frame to RGB for DeepFace
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Analyze emotions
                    result = DeepFace.analyze(
                        rgb_frame,
                        actions=['emotion'],
                        enforce_detection=False,
                        silent=True
                    )
                    
                    if isinstance(result, list):
                        result = result[0]
                        
                    emotion = result['dominant_emotion']
                    confidence = result['emotion'][emotion]
                    
                    # Create emotion result
                    emotion_result = EmotionResult(
                        emotion=emotion,
                        confidence=confidence,
                        timestamp=datetime.now(),
                        frame=frame if self.save_frames else None
                    )
                    
                    # Update current emotion and history
                    with self._lock:
                        self.current_emotion = emotion_result
                        self.emotion_history.append(emotion_result)
                        
                    last_detection_time = current_time
                    
                except Exception as e:
                    print(f"Error in emotion detection: {e}")
                    continue
                    
    def get_current_emotion(self) -> Optional[EmotionResult]:
        """Get the most recent emotion detection result"""
        with self._lock:
            return self.current_emotion
            
    def get_emotion_history(self, 
                          duration_seconds: Optional[float] = None) -> List[EmotionResult]:
        """
        Get emotion history for the specified duration
        
        Args:
            duration_seconds: If specified, only return emotions from the last N seconds
        """
        with self._lock:
            if duration_seconds is None:
                return self.emotion_history.copy()
                
            cutoff_time = datetime.now() - timedelta(seconds=duration_seconds)
            return [e for e in self.emotion_history if e.timestamp > cutoff_time]
            
    def get_emotion_stats(self, 
                         duration_seconds: Optional[float] = None) -> Dict[str, float]:
        """
        Get emotion statistics for the specified duration
        
        Args:
            duration_seconds: If specified, only analyze emotions from the last N seconds
            
        Returns:
            Dictionary mapping emotions to their average confidence
        """
        emotions = self.get_emotion_history(duration_seconds)
        if not emotions:
            return {}
            
        emotion_counts = {}
        emotion_confidences = {}
        
        for e in emotions:
            if e.emotion not in emotion_counts:
                emotion_counts[e.emotion] = 0
                emotion_confidences[e.emotion] = 0
            emotion_counts[e.emotion] += 1
            emotion_confidences[e.emotion] += e.confidence
            
        return {
            emotion: emotion_confidences[emotion] / emotion_counts[emotion]
            for emotion in emotion_counts
        } 