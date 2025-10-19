"""
ASL Letter Classifier
Recognizes ASL letters based on hand landmark geometry
Optimized for back-of-hand view
"""
import numpy as np
import math
from collections import deque


class ASLClassifier:
    def __init__(self):
        """Initialize the ASL letter classifier with geometric rules"""
        self.current_letter = ""
        self.letter_confidence = 0
        self.letter_history = deque(maxlen=10)  # Track last 10 predictions
        self.stable_letter = ""
        self.stable_count = 0
        
    def calculate_distance(self, p1, p2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def calculate_angle(self, p1, p2, p3):
        """
        Calculate angle at p2 formed by p1-p2-p3
        Returns angle in degrees
        """
        v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        
        dot_product = np.dot(v1, v2)
        mag1 = np.linalg.norm(v1)
        mag2 = np.linalg.norm(v2)
        
        if mag1 * mag2 == 0:
            return 0
        
        cos_angle = dot_product / (mag1 * mag2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        
        return math.degrees(angle)
    
    def fingers_up(self, landmarks, is_back_of_hand=False):
        """
        Determine which fingers are extended - ENHANCED VERSION
        Adjusted for back-of-hand view with better angle detection
        
        Args:
            landmarks: List of landmarks [[id, x, y], ...]
            is_back_of_hand: Whether viewing back of hand
        
        Returns:
            List of 5 values (thumb to pinky): 1 if up, 0 if down
        """
        fingers = []
        
        if len(landmarks) < 21:
            return fingers
        
        wrist = landmarks[0]
        
        # THUMB - Enhanced detection with angle and distance
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        index_mcp = landmarks[5]
        middle_mcp = landmarks[9]
        
        # Multiple checks for thumb
        thumb_dist = self.calculate_distance(thumb_tip[1:], index_mcp[1:])
        thumb_base_dist = self.calculate_distance(thumb_mcp[1:], index_mcp[1:])
        thumb_angle = self.calculate_angle(thumb_mcp[1:], thumb_ip[1:], thumb_tip[1:])
        
        # Thumb is up if:
        # 1. Distance from palm is significantly greater than base distance
        # 2. Angle at IP joint shows extension (> 140 degrees = straight)
        thumb_extended = (thumb_dist > thumb_base_dist * 1.15) or (thumb_angle > 130)  # More lenient
        fingers.append(1 if thumb_extended else 0)
        
        # OTHER FOUR FINGERS - Enhanced with angle and multi-factor checks (MORE LENIENT)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        finger_mcps = [5, 9, 13, 17]
        finger_dips = [7, 11, 15, 19]  # Added DIP joints
        
        for tip, pip, mcp, dip in zip(finger_tips, finger_pips, finger_mcps, finger_dips):
            # Calculate distances from wrist
            tip_wrist_dist = self.calculate_distance(landmarks[tip][1:], wrist[1:])
            pip_wrist_dist = self.calculate_distance(landmarks[pip][1:], wrist[1:])
            mcp_wrist_dist = self.calculate_distance(landmarks[mcp][1:], wrist[1:])
            
            # Calculate angles at joints
            pip_angle = self.calculate_angle(landmarks[mcp][1:], landmarks[pip][1:], landmarks[tip][1:])
            
            if is_back_of_hand:
                # For back view: Multiple factor check (MORE LENIENT)
                # Factor 1: Tip is further from wrist than PIP
                distance_check = tip_wrist_dist > pip_wrist_dist * 1.05  # Lowered from 1.08
                
                # Factor 2: Angle at PIP joint shows extension
                angle_check = pip_angle > 130  # Lowered from 140
                
                # Factor 3: Tip y-coordinate (visual check)
                y_check = landmarks[tip][2] < landmarks[mcp][2]
                
                # Finger is up if at least 2 of 3 checks pass
                checks_passed = sum([distance_check, angle_check, y_check])
                fingers.append(1 if checks_passed >= 2 else 0)
            else:
                # Standard palm view - improved (MORE LENIENT)
                distance_check = tip_wrist_dist > pip_wrist_dist * 1.05  # Lowered from 1.1
                angle_check = pip_angle > 130  # Lowered from 140
                y_check = landmarks[tip][2] < landmarks[pip][2]
                
                checks_passed = sum([distance_check, angle_check, y_check])
                fingers.append(1 if checks_passed >= 2 else 0)
        
        return fingers
    
    def classify_letter(self, landmarks, is_back_of_hand=False):
        """
        Classify ASL letter based on hand landmarks
        Optimized for back-of-hand view
        
        Args:
            landmarks: List of hand landmarks [[id, x, y], ...]
            is_back_of_hand: Whether viewing back of hand
            
        Returns:
            Tuple of (predicted letter, confidence score)
        """
        if len(landmarks) < 21:
            return "", 0.0
        
        fingers = self.fingers_up(landmarks, is_back_of_hand)
        
        if len(fingers) != 5:
            return "", 0.0
        
        # DEBUG: Print finger pattern for V/W troubleshooting
        if fingers in [[0, 1, 1, 0, 0], [0, 1, 1, 1, 0]]:
            print(f"🔍 DEBUG - Finger pattern: {fingers}")
        
        # Extract key points
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        index_mcp = landmarks[5]
        
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        middle_mcp = landmarks[9]
        
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]
        ring_mcp = landmarks[13]
        
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]
        pinky_mcp = landmarks[17]
        
        wrist = landmarks[0]
        
        # Calculate critical distances
        thumb_index_dist = self.calculate_distance(thumb_tip[1:], index_tip[1:])
        thumb_middle_dist = self.calculate_distance(thumb_tip[1:], middle_tip[1:])
        thumb_ring_dist = self.calculate_distance(thumb_tip[1:], ring_tip[1:])
        thumb_pinky_dist = self.calculate_distance(thumb_tip[1:], pinky_tip[1:])
        
        index_middle_dist = self.calculate_distance(index_tip[1:], middle_tip[1:])
        middle_ring_dist = self.calculate_distance(middle_tip[1:], ring_tip[1:])
        ring_pinky_dist = self.calculate_distance(ring_tip[1:], pinky_tip[1:])
        
        # Calculate palm width for normalization
        palm_width = self.calculate_distance(index_mcp[1:], pinky_mcp[1:])
        
        # Normalize distances by palm width for scale independence
        def norm_dist(dist):
            return dist / palm_width if palm_width > 0 else dist
        
        thumb_index_norm = norm_dist(thumb_index_dist)
        thumb_middle_norm = norm_dist(thumb_middle_dist)
        index_middle_norm = norm_dist(index_middle_dist)
        middle_ring_norm = norm_dist(middle_ring_dist)
        ring_pinky_norm = norm_dist(ring_pinky_dist)
        thumb_pinky_norm = norm_dist(thumb_pinky_dist)
        
        # Calculate angles for better precision
        index_angle = self.calculate_angle(index_mcp[1:], index_pip[1:], index_tip[1:])
        middle_angle = self.calculate_angle(middle_mcp[1:], middle_pip[1:], middle_tip[1:])
        ring_angle = self.calculate_angle(ring_mcp[1:], ring_pip[1:], ring_tip[1:])
        
        # ========== IMPROVED LETTER RECOGNITION - MORE LENIENT ==========
        # ========== CHECK V AND W FIRST - BEFORE B! ==========
        
        # W: Three fingers up (index, middle, ring) - CHECK FIRST!
        if fingers == [0, 1, 1, 1, 0]:
            # All three extended and separated
            if index_angle > 135 and middle_angle > 135 and ring_angle > 135:
                # Check finger spacing (RELAXED)
                if index_middle_norm > 0.2 and middle_ring_norm > 0.2:
                    return "W", 0.88
                else:
                    return "W", 0.80
        
        # V: Index and middle separated (peace sign) - CHECK SECOND BEFORE B!
        if fingers == [0, 1, 1, 0, 0]:
            # Separated V shape - distance between tips (VERY LENIENT)
            if index_middle_norm > 0.35 and index_angle > 140 and middle_angle > 140:
                return "V", 0.90
            # Less strict V detection
            elif index_middle_norm > 0.25 and index_angle > 135:
                return "V", 0.80
        
        # U: Index and middle together, pointing up - CHECK BEFORE B!
        if fingers == [0, 1, 1, 0, 0]:
            # Very close together and straight (RELAXED)
            if index_middle_norm < 0.25 and index_angle > 150 and middle_angle > 150:
                return "U", 0.87
            # Medium closeness
            elif index_middle_norm < 0.30 and index_angle > 145:
                return "U", 0.78
        
        # A: Fist with thumb on side
        if fingers == [1, 0, 0, 0, 0]:
            # Thumb extended, all fingers closed
            # Check thumb is not touching index (RELAXED)
            if thumb_index_norm > 0.4:  # Lowered from 0.5
                return "A", 0.92
        
        # B: All four fingers extended together, thumb tucked - NOW CHECKED AFTER V/W!
        if fingers == [0, 1, 1, 1, 1]:
            # Check fingers are close together (RELAXED)
            if index_middle_norm < 0.35 and middle_ring_norm < 0.35:  # Increased from 0.25
                return "B", 0.90
        
        # C: Curved hand shape (thumb and fingers form arc)
        if fingers == [1, 0, 0, 0, 0] or sum(fingers[1:]) <= 1:
            # Check if hand forms C curve (RELAXED)
            thumb_wrist_dist = self.calculate_distance(thumb_tip[1:], wrist[1:])
            index_wrist_dist = self.calculate_distance(index_tip[1:], wrist[1:])
            avg_dist = (thumb_wrist_dist + index_wrist_dist) / 2
            
            # Check curvature and gap (VERY RELAXED)
            if 0.25 < thumb_index_norm < 1.0 and abs(thumb_wrist_dist - index_wrist_dist) / avg_dist < 0.4:  # Was 0.3
                return "C", 0.78
        
        # D: Index up, thumb touches middle/ring, others closed
        if fingers == [1, 1, 0, 0, 0]:
            # Thumb should touch middle finger area (RELAXED)
            if thumb_middle_norm < 0.5 and index_angle > 140:  # Lowered from 150
                return "D", 0.85
        
        # E: Complete fist, all fingers closed
        if sum(fingers) == 0:
            # All fingers bent, check compactness (RELAXED)
            all_tips_close = (thumb_index_norm < 0.7 and  # Increased from 0.6
                             self.calculate_distance(index_tip[1:], middle_tip[1:]) < palm_width * 0.4)  # Increased from 0.3
            if all_tips_close:
                return "E", 0.88
        
        # F: OK sign - Index and thumb form circle, others up
        if fingers == [1, 0, 1, 1, 1]:
            # Thumb and index should be close (forming circle) (RELAXED)
            if thumb_index_norm < 0.4 and middle_angle > 140:  # Changed from 0.3 and 150
                return "F", 0.87
        
        # G: Index and thumb pointing sideways (like pointing gun)
        if fingers == [1, 1, 0, 0, 0]:
            # Check if thumb and index are extended but not touching (RELAXED)
            ti_angle = self.calculate_angle(thumb_tip[1:], wrist[1:], index_tip[1:])
            if 60 < ti_angle < 120 and thumb_index_norm > 0.7:  # Was 70-110 and 0.8
                return "G", 0.80
        
        # H: Index and middle extended horizontally, close together
        if fingers == [0, 1, 1, 0, 0]:
            # Fingers should be parallel and close (RELAXED)
            if index_middle_norm < 0.35 and abs(index_angle - middle_angle) < 30:  # Was 0.3 and 20
                return "H", 0.83
        
        # I: Only pinky extended (little finger up)
        if fingers == [0, 0, 0, 0, 1]:
            # Pinky clearly extended, others closed (RELAXED)
            pinky_angle = self.calculate_angle(pinky_mcp[1:], pinky_pip[1:], pinky_tip[1:])
            if pinky_angle > 140:  # Lowered from 150
                return "I", 0.92
        
        # K: Index and middle up, thumb between them
        if fingers == [1, 1, 1, 0, 0]:
            # Check thumb position relative to index and middle (RELAXED)
            thumb_y = thumb_tip[2]
            index_y = index_tip[2]
            middle_y = middle_tip[2]
            if abs(thumb_y - (index_y + middle_y)/2) < palm_width * 0.5:  # Increased from 0.4
                return "K", 0.78
        
        # L: Thumb and index at 90 degrees (L shape)
        if fingers == [1, 1, 0, 0, 0]:
            # Calculate angle between thumb and index (RELAXED)
            ti_angle = abs(thumb_tip[1] - index_tip[1]) / abs(thumb_tip[2] - index_tip[2] + 0.001)
            if ti_angle > 1.2 and index_angle > 140:  # Lowered from 1.5 and 150
                return "L", 0.85
        
        # M: Fist with thumb tucked under (3 knuckles showing)
        if fingers == [0, 0, 0, 0, 0]:
            # Thumb tucked under fingers (RELAXED)
            thumb_index_mcp_dist = self.calculate_distance(thumb_tip[1:], index_mcp[1:])
            if norm_dist(thumb_index_mcp_dist) < 0.5:  # Increased from 0.4
                return "M", 0.73
        
        # N: Similar to M but 2 knuckles (thumb between index and middle)
        if fingers == [0, 0, 0, 0, 0]:
            thumb_middle_mcp_dist = self.calculate_distance(thumb_tip[1:], middle_mcp[1:])
            if norm_dist(thumb_middle_mcp_dist) < 0.45:  # Increased from 0.35
                return "N", 0.71
        
        # O: Fingers and thumb form circle
        if fingers == [1, 0, 0, 0, 0] or sum(fingers[1:]) <= 1:
            # Check if tips form a circle (RELAXED)
            if thumb_index_norm < 0.35:  # Increased from 0.25
                return "O", 0.85
        
        # P: Index down, middle extended, forming inverted V
        if fingers == [1, 0, 1, 0, 0]:
            # Index bent down, middle pointing (RELAXED)
            if index_angle < 150 and middle_angle > 140:  # Changed from 140 and 150
                return "P", 0.80
        
        # Q: Similar to P but thumb pointing down more
        if fingers == [1, 0, 1, 0, 0]:
            thumb_down = thumb_tip[2] > thumb_mcp[2]
            if thumb_down and middle_angle > 140:  # Lowered from 150
                return "Q", 0.76
        
        # R: Index and middle crossed or very close
        if fingers == [0, 1, 1, 0, 0]:
            # Check crossing - tips should be very close (RELAXED)
            if index_middle_norm < 0.25 and abs(index_tip[1] - middle_tip[1]) < palm_width * 0.2:  # Was 0.2 and 0.15
                return "R", 0.78
        
        # S: Fist with thumb across front
        if fingers == [1, 0, 0, 0, 0]:
            # Thumb across fingers, not on side (RELAXED)
            thumb_center = (thumb_tip[1] > index_mcp[1] - palm_width * 0.2 and 
                          thumb_tip[1] < pinky_mcp[1] + palm_width * 0.2)
            if thumb_center and thumb_index_norm < 0.8:  # Increased from 0.7
                return "S", 0.73
        
        # T: Thumb between index and middle (fist)
        if fingers == [1, 0, 0, 0, 0]:
            # Thumb poking through closed fist (RELAXED)
            thumb_between = (index_mcp[1] < thumb_tip[1] < middle_mcp[1] or
                           middle_mcp[1] < thumb_tip[1] < index_mcp[1])
            if thumb_between and 0.3 < thumb_index_norm < 0.9:  # Changed from 0.4-0.8
                return "T", 0.73
        
        # NOTE: V, W, U are checked at the TOP of the function before B!
        
        # X: Index bent in hook shape
        if fingers == [0, 1, 0, 0, 0]:
            # Index bent/curved (RELAXED)
            if index_angle < 150:  # Increased from 140
                return "X", 0.80
        
        # Y: Thumb and pinky extended (hang loose/shaka)
        if fingers == [1, 0, 0, 0, 1]:
            # Wide spread between thumb and pinky (RELAXED)
            if thumb_pinky_norm > 1.1:  # Lowered from 1.3
                return "Y", 0.90
        
        # Additional fallback patterns for common issues
        
        # Detect V if fingers are slightly separated (even if U was tried)
        if fingers == [0, 1, 1, 0, 0] and index_middle_norm > 0.22:
            return "V", 0.75
        
        # Detect W if three fingers are up (even with relaxed angles)
        if fingers == [0, 1, 1, 1, 0]:
            return "W", 0.75
        
        # Detect B if four fingers are up
        if fingers == [0, 1, 1, 1, 1]:
            return "B", 0.75
        
        # Detect I if pinky is up
        if fingers == [0, 0, 0, 0, 1]:
            return "I", 0.75
        
        # Detect Y if thumb and pinky are up
        if fingers == [1, 0, 0, 0, 1]:
            return "Y", 0.75
        
        return "", 0.0
    
    def get_prediction(self, landmarks, is_back_of_hand=False, smoothing=True):
        """
        Get smoothed prediction with ENHANCED confidence scoring
        
        Args:
            landmarks: Hand landmarks
            is_back_of_hand: Whether viewing back of hand
            smoothing: Whether to apply temporal smoothing
            
        Returns:
            Tuple of (predicted letter, confidence)
        """
        letter, base_confidence = self.classify_letter(landmarks, is_back_of_hand)
        
        # Add to history
        self.letter_history.append(letter)
        
        if smoothing and len(self.letter_history) >= 3:
            # Require consistency across multiple frames
            recent = list(self.letter_history)[-5:]  # Last 5 frames
            
            # Count occurrences
            from collections import Counter
            letter_counts = Counter(recent)
            
            # Get most common letter
            if letter_counts:
                most_common_letter, count = letter_counts.most_common(1)[0]
                
                # Enhanced confidence calculation
                if most_common_letter != "" and count >= 3:
                    if most_common_letter == self.stable_letter:
                        self.stable_count += 1
                    else:
                        self.stable_letter = most_common_letter
                        self.stable_count = 1
                    
                    # Multi-factor confidence boost
                    # Factor 1: Temporal consistency (how many frames show same letter)
                    consistency_bonus = (count / 5.0) * 0.15  # Up to +15%
                    
                    # Factor 2: Stability over time (how long we've seen this letter)
                    stability_bonus = min(self.stable_count * 0.03, 0.15)  # Up to +15%
                    
                    # Factor 3: Base confidence quality
                    quality_multiplier = 1.0 if base_confidence > 0.85 else 0.8
                    
                    # Calculate final confidence
                    final_confidence = base_confidence + consistency_bonus + stability_bonus
                    final_confidence = min(final_confidence * quality_multiplier, 1.0)
                    
                    return self.stable_letter, final_confidence
                else:
                    # Not enough consistency, reduce confidence
                    return letter, base_confidence * 0.7
        
        return letter, base_confidence
