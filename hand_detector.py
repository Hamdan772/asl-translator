"""
Hand Detector Module
Detects and tracks hand landmarks using MediaPipe
Enhanced with advanced smoothing, stability detection, and outlier rejection
"""
import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque


class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.7):
        """
        Initialize the hand detector with BALANCED accuracy settings
        
        Args:
            mode: Static image mode or video mode
            max_hands: Maximum number of hands to detect
            detection_con: Minimum detection confidence (balanced at 0.7)
            track_con: Minimum tracking confidence (balanced at 0.7)
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        
        # Initialize MediaPipe hands with higher confidence thresholds
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # ENHANCED: Kalman-style smoothing buffer for landmark positions
        self.landmark_buffer = deque(maxlen=7)  # Increased from 5 to 7
        self.smoothed_landmarks = None
        
        # NEW: Outlier detection
        self.outlier_threshold = 0.15  # 15% deviation threshold
        
        # NEW: Hand stability tracking
        self.stability_buffer = deque(maxlen=10)
        self.is_hand_stable = True  # Start as True to allow initial detection
        self.stability_threshold = 0.15  # 15% movement threshold (very lenient)
        self.require_stability = False  # Can be toggled
        
        # Wave detection
        self.hand_x_history = deque(maxlen=15)  # Track hand X position
        self.wave_threshold = 50  # Minimum movement for wave
        self.wave_cooldown = 3.0  # Seconds between wave detections
        self.last_wave_time = 0
        
        # Thumbs up/down detection
        self.hand_y_history = deque(maxlen=10)  # Track vertical position
        self.last_thumbs_gesture = ""
        self.thumbs_cooldown = 2.0
        self.last_thumbs_time = 0
        
    def find_hands(self, img, draw=True):
        """
        Find hands in the image
        
        Args:
            img: Input image (BGR format)
            draw: Whether to draw landmarks on the image
            
        Returns:
            Image with landmarks drawn (if draw=True)
        """
        # Convert to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        # Draw landmarks if hands detected
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Custom drawing with better visibility
                self.mp_draw.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                    self.mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
                )
        
        return img
    
    def get_hand_label(self, hand_no=0):
        """
        Get whether the hand is left or right
        
        Args:
            hand_no: Which hand to check
            
        Returns:
            'Left' or 'Right' or None
        """
        if self.results.multi_handedness:
            if hand_no < len(self.results.multi_handedness):
                return self.results.multi_handedness[hand_no].classification[0].label
        return None
    
    def is_back_of_hand(self, landmarks):
        """
        Determine if viewing the back of the hand based on landmark positions
        
        Args:
            landmarks: List of landmarks [[id, x, y], ...]
            
        Returns:
            True if back of hand, False if palm
        """
        if len(landmarks) < 21:
            return False
        
        # Use wrist (0) and middle finger MCP (9) to determine orientation
        # If thumb is on the expected side for palm view, it's palm
        # Otherwise, it's back of hand
        
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]
        pinky_mcp = landmarks[17]
        
        # Calculate if thumb is between index and pinky horizontally
        # For palm view: thumb should be on the side
        # For back view: thumb position is reversed
        
        hand_width = abs(index_mcp[1] - pinky_mcp[1])
        thumb_offset = thumb_tip[1] - wrist[1]
        
        # Simple heuristic: if thumb appears on "wrong" side, it's back of hand
        # This works when hand is relatively upright
        return abs(thumb_offset) < hand_width * 0.3
    
    def detect_wave(self, landmarks):
        """
        Detect waving motion by tracking horizontal hand movement
        
        Args:
            landmarks: List of landmarks [[id, x, y], ...]
            
        Returns:
            True if wave detected, False otherwise
        """
        if len(landmarks) < 21:
            self.hand_x_history.clear()
            return False
        
        # Use wrist position for tracking
        wrist_x = landmarks[0][1]
        self.hand_x_history.append(wrist_x)
        
        # Need enough history to detect wave
        if len(self.hand_x_history) < 10:
            return False
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_wave_time < self.wave_cooldown:
            return False
        
        # Analyze movement pattern - looking for left-right oscillation
        positions = list(self.hand_x_history)
        
        # Count direction changes (wave should have multiple)
        direction_changes = 0
        total_movement = 0
        
        for i in range(1, len(positions) - 1):
            # Check if direction changed
            prev_diff = positions[i] - positions[i-1]
            curr_diff = positions[i+1] - positions[i]
            
            if prev_diff * curr_diff < 0:  # Sign change = direction change
                direction_changes += 1
            
            total_movement += abs(curr_diff)
        
        # Wave detected if:
        # 1. Multiple direction changes (at least 2 for a wave)
        # 2. Significant total movement
        # 3. Hand is extended (fingers visible)
        
        is_waving = (
            direction_changes >= 2 and 
            total_movement > self.wave_threshold
        )
        
        if is_waving:
            self.last_wave_time = current_time
            self.hand_x_history.clear()  # Clear for next detection
        
        return is_waving
    
    def detect_thumbs_gesture(self, landmarks):
        """
        Detect thumbs up or thumbs down gesture
        
        Args:
            landmarks: List of landmarks [[id, x, y], ...]
            
        Returns:
            'THUMBS_UP', 'THUMBS_DOWN', or ''
        """
        if len(landmarks) < 21:
            return ""
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_thumbs_time < self.thumbs_cooldown:
            return ""
        
        # Get key points
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        index_mcp = landmarks[5]
        middle_mcp = landmarks[9]
        ring_mcp = landmarks[13]
        pinky_mcp = landmarks[17]
        wrist = landmarks[0]
        
        # Check if other fingers are closed (thumb gesture)
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Fingers should be bent (tips below MCPs)
        fingers_closed = (
            index_tip[2] > index_mcp[2] and
            middle_tip[2] > middle_mcp[2] and
            ring_tip[2] > ring_mcp[2] and
            pinky_tip[2] > pinky_mcp[2]
        )
        
        if not fingers_closed:
            return ""
        
        # Check thumb orientation
        # Thumbs up: thumb tip is above wrist and extended upward
        # Thumbs down: thumb tip is below wrist and extended downward
        
        thumb_extended = abs(thumb_tip[1] - wrist[1]) > 60  # Thumb out to side
        
        if thumb_extended:
            # Check vertical position
            thumb_wrist_vertical = thumb_tip[2] - wrist[2]
            
            if thumb_wrist_vertical < -100:  # Thumb significantly above wrist
                gesture = 'THUMBS_UP'
            elif thumb_wrist_vertical > 50:  # Thumb below wrist
                gesture = 'THUMBS_DOWN'
            else:
                return ""
            
            self.last_thumbs_time = current_time
            self.last_thumbs_gesture = gesture
            return gesture
        
        return ""
    
    def find_position(self, img, hand_no=0, smooth=True):
        """
        Find the position of hand landmarks with optional smoothing
        
        Args:
            img: Input image
            hand_no: Which hand to get landmarks from (default: 0)
            smooth: Apply temporal smoothing
            
        Returns:
            List of landmarks with [id, x, y] format
        """
        landmark_list = []
        
        if self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                hand = self.results.multi_hand_landmarks[hand_no]
                
                for id, lm in enumerate(hand.landmark):
                    h, w, c = img.shape
                    # Convert normalized coordinates to pixel coordinates
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmark_list.append([id, cx, cy])
                
                # Apply ENHANCED smoothing with outlier rejection
                if smooth and len(landmark_list) == 21:
                    # Check for outliers before adding to buffer
                    if len(self.landmark_buffer) > 0:
                        if not self._is_outlier(landmark_list):
                            self.landmark_buffer.append(landmark_list)
                    else:
                        self.landmark_buffer.append(landmark_list)
                    
                    # Enhanced weighted averaging (more recent frames have more weight)
                    if len(self.landmark_buffer) >= 3:
                        smoothed = []
                        buffer_size = len(self.landmark_buffer)
                        
                        for i in range(21):
                            # Weighted average: recent frames weighted higher
                            weighted_x = 0
                            weighted_y = 0
                            total_weight = 0
                            
                            for j, frame in enumerate(self.landmark_buffer):
                                weight = (j + 1) / buffer_size  # Linear weighting
                                weighted_x += frame[i][1] * weight
                                weighted_y += frame[i][2] * weight
                                total_weight += weight
                            
                            avg_x = int(weighted_x / total_weight)
                            avg_y = int(weighted_y / total_weight)
                            smoothed.append([i, avg_x, avg_y])
                        
                        landmark_list = smoothed
                        
                        # Update stability tracking
                        self._update_stability(landmark_list)
        
        return landmark_list
    
    def _is_outlier(self, current_landmarks):
        """
        Check if current landmarks are outliers compared to recent history
        
        Args:
            current_landmarks: Current frame landmarks
            
        Returns:
            True if outlier, False otherwise
        """
        if len(self.landmark_buffer) == 0:
            return False
        
        # Compare with most recent frame
        last_frame = self.landmark_buffer[-1]
        
        # Calculate average distance between corresponding landmarks
        total_distance = 0
        for i in range(21):
            dx = current_landmarks[i][1] - last_frame[i][1]
            dy = current_landmarks[i][2] - last_frame[i][2]
            distance = np.sqrt(dx**2 + dy**2)
            total_distance += distance
        
        avg_distance = total_distance / 21
        
        # Calculate hand size for normalization
        wrist = last_frame[0]
        middle_mcp = last_frame[9]
        hand_size = np.sqrt((middle_mcp[1] - wrist[1])**2 + (middle_mcp[2] - wrist[2])**2)
        
        # Outlier if average movement is more than threshold% of hand size
        if hand_size > 0:
            normalized_distance = avg_distance / hand_size
            return normalized_distance > self.outlier_threshold
        
        return False
    
    def _update_stability(self, landmarks):
        """
        Update hand stability tracking
        
        Args:
            landmarks: Current smoothed landmarks
        """
        if len(self.landmark_buffer) < 2:
            self.is_hand_stable = False
            return
        
        # Calculate movement from previous frame
        prev_frame = self.landmark_buffer[-2]
        
        total_movement = 0
        for i in range(21):
            dx = landmarks[i][1] - prev_frame[i][1]
            dy = landmarks[i][2] - prev_frame[i][2]
            movement = np.sqrt(dx**2 + dy**2)
            total_movement += movement
        
        avg_movement = total_movement / 21
        
        # Calculate hand size
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        hand_size = np.sqrt((middle_mcp[1] - wrist[1])**2 + (middle_mcp[2] - wrist[2])**2)
        
        # Normalize movement
        if hand_size > 0:
            normalized_movement = avg_movement / hand_size
            self.stability_buffer.append(normalized_movement)
            
            # Hand is stable if recent movements are all below threshold
            if len(self.stability_buffer) >= 3:  # Reduced from 5 to 3 frames
                recent_movements = list(self.stability_buffer)[-3:]
                self.is_hand_stable = all(m < self.stability_threshold for m in recent_movements)
        else:
            self.is_hand_stable = False
    
    def get_landmark_features(self, img, hand_no=0):
        """
        Extract normalized landmark features for classification
        
        Args:
            img: Input image
            hand_no: Which hand to get features from
            
        Returns:
            Normalized feature vector (numpy array)
        """
        landmarks = self.find_position(img, hand_no)
        
        if len(landmarks) == 0:
            return None
        
        # Extract x, y coordinates
        coords = np.array([[lm[1], lm[2]] for lm in landmarks])
        
        # Normalize relative to wrist (landmark 0)
        wrist = coords[0]
        normalized = coords - wrist
        
        # Scale based on hand size (distance from wrist to middle finger MCP)
        if len(coords) > 9:
            scale = np.linalg.norm(coords[9] - wrist)
            if scale > 0:
                normalized = normalized / scale
        
        # Flatten to feature vector
        features = normalized.flatten()
        
        return features
