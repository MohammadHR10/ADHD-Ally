from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import threading
from .audio import SpeechEmotionRecognizer
from .video_emotion import VideoEmotionRecognizer, EmotionResult

@dataclass
class CombinedEmotionResult:
    timestamp: datetime
    audio_emotion: Optional[str] = None
    audio_confidence: Optional[float] = None
    video_emotion: Optional[str] = None
    video_confidence: Optional[float] = None
    
    @property
    def dominant_emotion(self) -> Optional[str]:
        """Get the dominant emotion based on confidence scores"""
        if not self.audio_emotion and not self.video_emotion:
            return None
            
        if not self.audio_emotion:
            return self.video_emotion
        if not self.video_emotion:
            return self.audio_emotion
            
        # If both are present, use the one with higher confidence
        if self.audio_confidence and self.video_confidence:
            return self.video_emotion if self.video_confidence > self.audio_confidence else self.audio_emotion
            
        return self.video_emotion or self.audio_emotion

class MultimodalEmotionRecognizer:
    def __init__(self,
                 camera_id: int = 0,
                 video_detection_interval: float = 1.0,
                 audio_detection_interval: float = 1.0,
                 save_frames: bool = False):
        """
        Initialize the multimodal emotion recognizer
        
        Args:
            camera_id: ID of the camera to use
            video_detection_interval: Time between video emotion detections
            audio_detection_interval: Time between audio emotion detections
            save_frames: Whether to save video frames
        """
        self.video_recognizer = VideoEmotionRecognizer(
            camera_id=camera_id,
            detection_interval=video_detection_interval,
            save_frames=save_frames
        )
        
        self.audio_recognizer = SpeechEmotionRecognizer(
            detection_interval=audio_detection_interval
        )
        
        self.emotion_history: List[CombinedEmotionResult] = []
        self.current_emotion: Optional[CombinedEmotionResult] = None
        self._lock = threading.Lock()
        self._sync_thread: Optional[threading.Thread] = None
        self.is_running = False
        
    def start(self) -> None:
        """Start both audio and video emotion recognition"""
        if self.is_running:
            return
            
        self.video_recognizer.start()
        self.audio_recognizer.start()
        
        self.is_running = True
        self._sync_thread = threading.Thread(target=self._sync_loop)
        self._sync_thread.daemon = True
        self._sync_thread.start()
        
    def stop(self) -> None:
        """Stop both audio and video emotion recognition"""
        self.is_running = False
        if self._sync_thread:
            self._sync_thread.join()
            
        self.video_recognizer.stop()
        self.audio_recognizer.stop()
        
    def _sync_loop(self) -> None:
        """Synchronize audio and video emotion results"""
        while self.is_running:
            video_emotion = self.video_recognizer.get_current_emotion()
            audio_emotion = self.audio_recognizer.get_current_emotion()
            
            if video_emotion or audio_emotion:
                combined_result = CombinedEmotionResult(
                    timestamp=datetime.now(),
                    video_emotion=video_emotion.emotion if video_emotion else None,
                    video_confidence=video_emotion.confidence if video_emotion else None,
                    audio_emotion=audio_emotion.emotion if audio_emotion else None,
                    audio_confidence=audio_emotion.confidence if audio_emotion else None
                )
                
                with self._lock:
                    self.current_emotion = combined_result
                    self.emotion_history.append(combined_result)
                    
    def get_current_emotion(self) -> Optional[CombinedEmotionResult]:
        """Get the most recent combined emotion result"""
        with self._lock:
            return self.current_emotion
            
    def get_emotion_history(self, 
                          duration_seconds: Optional[float] = None) -> List[CombinedEmotionResult]:
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
        Get combined emotion statistics for the specified duration
        
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
            dominant = e.dominant_emotion
            if not dominant:
                continue
                
            if dominant not in emotion_counts:
                emotion_counts[dominant] = 0
                emotion_confidences[dominant] = 0
                
            emotion_counts[dominant] += 1
            # Use the higher confidence score
            confidence = max(
                e.audio_confidence or 0,
                e.video_confidence or 0
            )
            emotion_confidences[dominant] += confidence
            
        return {
            emotion: emotion_confidences[emotion] / emotion_counts[emotion]
            for emotion in emotion_counts
        } 