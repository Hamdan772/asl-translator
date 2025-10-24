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
        
        # Initialize MediaPipe hands with OPTIMIZED settings for speed
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con,
            model_complexity=0  # 0=Lite (faster), 1=Full (slower but more accurate)
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
        
    def find_hands(self, img, draw=True, enhance_visual=True):
        """
        Find hands in the image with optimized visual quality
        
        Args:
            img: Input image (BGR format)
            draw: Whether to draw landmarks on the image
            enhance_visual: Whether to enhance brightness/contrast for better visibility
            
        Returns:
            Image with landmarks drawn (if draw=True)
        """
        # OPTIMIZED: Lighter enhancement for better FPS
        if enhance_visual:
            # Quick brightness boost only (faster than filter2D)
            img = cv2.convertScaleAbs(img, alpha=1.15, beta=15)
        
        # Convert to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        # Draw landmarks if hands detected
        if self.results.multi_hand_landmarks and draw:
            h, w, c = img.shape
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Calculate hand bounding box for highlighting
                x_coords = [lm.x for lm in hand_landmarks.landmark]
                y_coords = [lm.y for lm in hand_landmarks.landmark]
                
                x_min, x_max = int(min(x_coords) * w), int(max(x_coords) * w)
                y_min, y_max = int(min(y_coords) * h), int(max(y_coords) * h)
                
                # Add padding to bounding box
                padding = 40
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)
                
                # Draw semi-transparent highlight around hand region
                overlay = img.copy()
                cv2.rectangle(overlay, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)
                cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
                
                # Draw subtle filled rectangle as background for better dot visibility
                overlay2 = img.copy()
                cv2.rectangle(overlay2, (x_min, y_min), (x_max, y_max), (255, 255, 255), -1)
                cv2.addWeighted(overlay2, 0.05, img, 0.95, 0, img)
                
                # Draw the base landmarks and connections with BRIGHTER colors
                self.mp_draw.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=3, circle_radius=5),  # Larger green landmarks
                    self.mp_draw.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=2)  # Thicker cyan connections
                )
                
                # ADD MORE DOTS: Draw intermediate dots along each connection
                for connection in self.mp_hands.HAND_CONNECTIONS:
                    start_idx = connection[0]
                    end_idx = connection[1]
                    
                    start_landmark = hand_landmarks.landmark[start_idx]
                    end_landmark = hand_landmarks.landmark[end_idx]
                    
                    start_x, start_y = int(start_landmark.x * w), int(start_landmark.y * h)
                    end_x, end_y = int(end_landmark.x * w), int(end_landmark.y * h)
                    
                    # Draw 5 intermediate dots along each connection line (100 extra dots total!)
                    for i in range(1, 6):
                        t = i / 6.0  # Position along the line (0.167, 0.333, 0.5, 0.667, 0.833)
                        mid_x = int(start_x + (end_x - start_x) * t)
                        mid_y = int(start_y + (end_y - start_y) * t)
                        cv2.circle(img, (mid_x, mid_y), 3, (255, 255, 0), -1)  # Brighter YELLOW dots, slightly larger
                
                # Label key fingertips for easy identification
                finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
                finger_tips = [4, 8, 12, 16, 20]
                
                for name, tip_idx in zip(finger_names, finger_tips):
                    tip = hand_landmarks.landmark[tip_idx]
                    tip_x, tip_y = int(tip.x * w), int(tip.y * h)
                    
                    # Draw finger label above fingertip
                    cv2.putText(img, name, (tip_x - 30, tip_y - 15),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(img, name, (tip_x - 30, tip_y - 15),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1, cv2.LINE_AA)
        
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
    
    def get_finger_states(self, landmarks):
        """
        Analyze which fingers are extended (UP) vs curled (DOWN)
        
        Args:
            landmarks: List of landmarks [[id, x, y], ...]
            
        Returns:
            Dictionary with finger names and boolean states (True = UP, False = DOWN)
        """
        if len(landmarks) < 21:
            return None
        
        # Finger tip indices: [thumb, index, middle, ring, pinky]
        tip_indices = [4, 8, 12, 16, 20]
        # Finger base indices (knuckles)
        base_indices = [2, 5, 9, 13, 17]
        # Mid-joint indices for angle calculation
        mid_indices = [3, 6, 10, 14, 18]
        
        finger_states = {}
        finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
        
        wrist = np.array([landmarks[0][1], landmarks[0][2]])
        
        for i, (tip_idx, mid_idx, base_idx, name) in enumerate(zip(tip_indices, mid_indices, base_indices, finger_names)):
            tip = np.array([landmarks[tip_idx][1], landmarks[tip_idx][2]])
            mid = np.array([landmarks[mid_idx][1], landmarks[mid_idx][2]])
            base = np.array([landmarks[base_idx][1], landmarks[base_idx][2]])
            
            if name == 'thumb':
                # IMPROVED THUMB DETECTION using angle method
                # Thumb is special - it moves perpendicular to other fingers
                # Check if thumb tip is far from palm center (landmark 9)
                palm_center = np.array([landmarks[9][1], landmarks[9][2]])
                
                # Vector from thumb base to tip
                thumb_vector = tip - base
                # Vector from wrist to palm center
                palm_vector = palm_center - wrist
                
                # Thumb is extended if:
                # 1. Tip is far from palm center
                # 2. Thumb vector is long (thumb stretched out)
                tip_to_palm_dist = np.linalg.norm(tip - palm_center)
                thumb_length = np.linalg.norm(thumb_vector)
                base_to_palm_dist = np.linalg.norm(base - palm_center)
                
                # More lenient thumb detection
                is_extended = (tip_to_palm_dist > base_to_palm_dist * 1.1) and (thumb_length > base_to_palm_dist * 0.5)
                finger_states[name] = is_extended
            else:
                # For other fingers, use improved angle + distance method
                # Calculate vectors
                v1 = mid - base  # Base to mid-joint
                v2 = tip - mid   # Mid-joint to tip
                
                # Calculate angle between joints (0 = straight, 180 = curled back)
                dot_product = np.dot(v1, v2)
                norms = np.linalg.norm(v1) * np.linalg.norm(v2)
                
                if norms > 0:
                    cos_angle = np.clip(dot_product / norms, -1.0, 1.0)
                    angle = np.arccos(cos_angle) * 180 / np.pi
                else:
                    angle = 0
                
                # Also check distance from wrist
                tip_dist = np.linalg.norm(tip - wrist)
                base_dist = np.linalg.norm(base - wrist)
                extension_ratio = tip_dist / (base_dist + 0.001)
                
                # Finger is extended if:
                # 1. Angle is relatively straight (< 160 degrees)
                # 2. Tip is farther from wrist than base
                is_extended = (angle < 160) and (extension_ratio > 1.15)
                finger_states[name] = is_extended
        
        return finger_states
    
    def draw_finger_state_indicator(self, img, landmarks, x_offset=10, y_offset=200):
        """
        Draw a visual indicator showing which fingers are UP/DOWN
        
        Args:
            img: Image to draw on
            landmarks: List of landmarks [[id, x, y], ...]
            x_offset: X position for the indicator
            y_offset: Y position for the indicator
            
        Returns:
            Image with finger state indicator drawn
        """
        finger_states = self.get_finger_states(landmarks)
        
        if not finger_states:
            return img
        
        # Create semi-transparent background panel
        panel_height = 180
        panel_width = 250
        overlay = img.copy()
        cv2.rectangle(overlay, (x_offset, y_offset), (x_offset + panel_width, y_offset + panel_height),
                     (40, 40, 40), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Draw border
        cv2.rectangle(img, (x_offset, y_offset), (x_offset + panel_width, y_offset + panel_height),
                     (255, 255, 255), 2)
        
        # Title
        cv2.putText(img, "FINGER STATUS", (x_offset + 10, y_offset + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Draw each finger state
        finger_display = [
            ('Thumb', finger_states['thumb']),
            ('Index', finger_states['index']),
            ('Middle', finger_states['middle']),
            ('Ring', finger_states['ring']),
            ('Pinky', finger_states['pinky'])
        ]
        
        y_pos = y_offset + 50
        for name, is_up in finger_display:
            # Choose color and emoji
            if is_up:
                color = (0, 255, 0)  # Green for UP
                status = "UP   "
                emoji = "👆"
            else:
                color = (100, 100, 100)  # Gray for DOWN
                status = "DOWN"
                emoji = "👇"
            
            # Draw finger name
            cv2.putText(img, f"{name}:", (x_offset + 15, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
            # Draw status with color
            cv2.putText(img, status, (x_offset + 120, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            
            # Draw emoji indicator
            cv2.putText(img, emoji, (x_offset + 200, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
            
            y_pos += 25
        
        # Count fingers UP
        fingers_up = sum(1 for _, is_up in finger_display if is_up)
        cv2.putText(img, f"Count: {fingers_up}", (x_offset + 15, y_pos + 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)
        
        return img
