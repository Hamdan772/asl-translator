"""
ASL Letter Classifier
Recognizes ASL letters based on hand landmark geometry
Optimized for back-of-hand view
Enhanced with ML-inspired feature extraction
"""
import numpy as np
import math
from collections import deque
from feature_extraction import AdvancedFeatureExtractor, DataPreprocessor


class ASLClassifier:
    def __init__(self):
        """Initialize the ASL letter classifier with geometric rules and advanced features"""
        self.current_letter = ""
        self.letter_confidence = 0
        self.letter_history = deque(maxlen=10)  # Track last 10 predictions
        self.stable_letter = ""
        self.stable_count = 0
        
        # NEW: Advanced feature extraction
        self.feature_extractor = AdvancedFeatureExtractor()
        self.preprocessor = DataPreprocessor()
        self.landmark_history = deque(maxlen=5)  # For smoothing
        
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
    
    def calculate_finger_curvature(self, landmarks, finger_idx):
        """
        Calculate how curved a finger is (0=bent, 1=straight)
        
        Args:
            landmarks: Hand landmarks
            finger_idx: 0=thumb, 1=index, 2=middle, 3=ring, 4=pinky
        
        Returns:
            Curvature score (0.0 to 1.0)
        """
        if finger_idx == 0:  # Thumb
            joints = [2, 3, 4]  # MCP, IP, TIP
        else:  # Other fingers
            base = 1 + finger_idx * 4
            joints = [base, base+1, base+2, base+3]  # MCP, PIP, DIP, TIP
        
        if any(j >= len(landmarks) for j in joints):
            return 0.0
        
        # Calculate direct distance (straight line)
        direct = self.calculate_distance(landmarks[joints[0]][1:], landmarks[joints[-1]][1:])
        
        # Calculate sum of segments (actual path)
        segments = sum(
            self.calculate_distance(landmarks[joints[i]][1:], landmarks[joints[i+1]][1:])
            for i in range(len(joints) - 1)
        )
        
        # Straightness ratio (1.0 = perfectly straight)
        return direct / (segments + 0.001)
    
    def calculate_hand_orientation(self, landmarks):
        """
        Calculate hand rotation angle (helpful for some letters)
        
        Returns:
            Angle in degrees (0-360)
        """
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        
        dx = middle_mcp[1] - wrist[1]
        dy = middle_mcp[2] - wrist[2]
        
        angle = math.degrees(math.atan2(dy, dx))
        return (angle + 360) % 360  # Normalize to 0-360
    
    def get_finger_spread(self, landmarks):
        """
        Calculate distances between all adjacent fingertips
        Returns list of 4 distances: [thumb-index, index-middle, middle-ring, ring-pinky]
        """
        tips = [4, 8, 12, 16, 20]  # Thumb to pinky tips
        spreads = []
        
        for i in range(len(tips) - 1):
            dist = self.calculate_distance(landmarks[tips[i]][1:], landmarks[tips[i+1]][1:])
            spreads.append(dist)
        
        return spreads
    
    def get_advanced_confidence_boost(self, landmarks, letter, base_confidence):
        """
        Use advanced features to boost confidence for ambiguous letters
        Helps differentiate V/W/U, O/C, E/M/N, etc.
        """
        # Extract all features
        features = self.feature_extractor.extract_all_features(landmarks)
        
        if not features:
            return base_confidence
        
        confidence_adjustment = 0.0
        
        # Get key features
        dist_features = features.get('distances', {})
        angle_features = features.get('angles', {})
        finger_features = features.get('fingers', {})
        
        # Letter-specific confidence boosting
        if letter == "V":
            # V should have: 2 straight fingers, wide spread, high inter-finger angle
            if finger_features.get('index_straightness', 0) > 0.90 and \
               finger_features.get('middle_straightness', 0) > 0.90:
                confidence_adjustment += 0.05
            
            # Wide spread between index and middle
            if dist_features.get('spread_1', 0) > 0.25:
                confidence_adjustment += 0.03
            
            # High inter-finger angle (wide V)
            if angle_features.get('interfinger_angle_1', 0) > 25:
                confidence_adjustment += 0.02
        
        elif letter == "W":
            # W should have: 3 straight fingers, consistent spread
            straight_count = sum([
                finger_features.get('index_straightness', 0) > 0.90,
                finger_features.get('middle_straightness', 0) > 0.90,
                finger_features.get('ring_straightness', 0) > 0.90
            ])
            if straight_count == 3:
                confidence_adjustment += 0.05
            
            # Consistent spread between all three
            spread_1 = dist_features.get('spread_1', 0)
            spread_2 = dist_features.get('spread_2', 0)
            if spread_1 > 0.15 and spread_2 > 0.15 and abs(spread_1 - spread_2) < 0.10:
                confidence_adjustment += 0.03
        
        elif letter == "U":
            # U should have: 2 straight fingers, close together
            if finger_features.get('index_straightness', 0) > 0.90 and \
               finger_features.get('middle_straightness', 0) > 0.90:
                confidence_adjustment += 0.05
            
            # Very close spread
            if dist_features.get('spread_1', 0) < 0.15:
                confidence_adjustment += 0.03
        
        elif letter == "O":
            # O should have: all fingers bent, small circle
            bent_count = sum([
                finger_features.get('index_curvature', 0) > 0.25,
                finger_features.get('middle_curvature', 0) > 0.25,
                finger_features.get('ring_curvature', 0) > 0.25,
                finger_features.get('pinky_curvature', 0) > 0.25
            ])
            if bent_count >= 3:
                confidence_adjustment += 0.05
        
        elif letter == "C":
            # C should have: moderate curvature, wider gap than O
            moderate_curve_count = sum([
                0.15 < finger_features.get('index_curvature', 0) < 0.40,
                0.15 < finger_features.get('middle_curvature', 0) < 0.40
            ])
            if moderate_curve_count == 2:
                confidence_adjustment += 0.04
        
        elif letter == "B":
            # B should have: 4 straight fingers, close together
            straight_count = sum([
                finger_features.get('index_straightness', 0) > 0.88,
                finger_features.get('middle_straightness', 0) > 0.88,
                finger_features.get('ring_straightness', 0) > 0.88,
                finger_features.get('pinky_straightness', 0) > 0.88
            ])
            if straight_count == 4:
                confidence_adjustment += 0.05
            
            # All close together
            all_close = all([
                dist_features.get('spread_1', 0) < 0.20,
                dist_features.get('spread_2', 0) < 0.20,
                dist_features.get('spread_3', 0) < 0.20
            ])
            if all_close:
                confidence_adjustment += 0.03
        
        elif letter == "A":
            # A should have: all fingers bent (fist), thumb BESIDE (not touching)
            bent_count = sum([
                finger_features.get('index_curvature', 0) > 0.35,
                finger_features.get('middle_curvature', 0) > 0.35,
                finger_features.get('ring_curvature', 0) > 0.35,
                finger_features.get('pinky_curvature', 0) > 0.35
            ])
            if bent_count == 4:
                confidence_adjustment += 0.06  # Strong indicator
            
            # Thumb should be extended to side (large thumb-index distance)
            thumb_index_dist = dist_features.get('thumb_index_tip', 0)
            if thumb_index_dist > 0.38:
                confidence_adjustment += 0.04  # Thumb clearly out
        
        elif letter == "K":
            # K should have: index+middle straight in V, thumb TOUCHING middle knuckle
            if finger_features.get('index_straightness', 0) > 0.85 and \
               finger_features.get('middle_straightness', 0) > 0.85:
                confidence_adjustment += 0.05
            
            # V-shaped spread (index and middle separated)
            if dist_features.get('spread_1', 0) > 0.18:
                confidence_adjustment += 0.03
            
            # Thumb should be HIGH and close to middle (key K feature!)
            # This is the CRITICAL difference from A and V
            thumb_to_middle_mcp = dist_features.get('thumb_middle_mcp', 0)
            if thumb_to_middle_mcp and thumb_to_middle_mcp < 0.28:
                confidence_adjustment += 0.07  # MAJOR confidence boost for K

        
        # Apply adjustment
        return min(base_confidence + confidence_adjustment, 1.0)
    
    def fingers_up(self, landmarks, is_back_of_hand=False):
        """
        SIMPLE & PROVEN finger detection method
        Based on successful MediaPipe hand tracking projects
        
        Args:
            landmarks: List of landmarks [[id, x, y], ...]
            is_back_of_hand: Whether viewing back of hand
        
        Returns:
            List of 5 values (thumb to pinky): 1 if up, 0 if down
        """
        fingers = []
        
        if len(landmarks) < 21:
            return fingers
        
        # Landmark indices
        tip_ids = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky tips
        pip_ids = [2, 6, 10, 14, 18]  # PIP joints (use MCP for thumb)
        
        # THUMB: Simple horizontal distance check (PROVEN METHOD)
        # Thumb is "up" (extended) if tip is further from palm center than base
        if is_back_of_hand:
            # For back of hand: check X-axis distance from palm center
            thumb_tip_x = landmarks[4][1]  # x coordinate
            thumb_base_x = landmarks[2][1]  # thumb MCP x
            palm_center_x = landmarks[0][1]  # wrist x
            
            # Thumb extended if tip is further from palm center than base
            thumb_tip_dist = abs(thumb_tip_x - palm_center_x)
            thumb_base_dist = abs(thumb_base_x - palm_center_x)
            
            # SIMPLE: thumb extended if tip > base distance by 20%
            thumb_extended = thumb_tip_dist > thumb_base_dist * 1.2
        else:
            # Palm view: use Y-axis
            thumb_extended = landmarks[4][2] < landmarks[2][2]
        
        fingers.append(1 if thumb_extended else 0)
        
        # OTHER FOUR FINGERS - SIMPLE Y-COORDINATE CHECK (PROVEN METHOD)
        # This is how most successful MediaPipe projects do it
        for i in range(1, 5):  # index, middle, ring, pinky
            tip_idx = tip_ids[i]
            pip_idx = pip_ids[i]
            
            if is_back_of_hand:
                # SIMPLE: Finger is UP if tip Y < pip Y (tip is above pip joint)
                # Add small tolerance for bent vs straight
                tip_y = landmarks[tip_idx][2]
                pip_y = landmarks[pip_idx][2]
                
                # Finger is extended if tip is significantly above PIP joint
                finger_up = tip_y < pip_y - 10  # 10 pixel tolerance
            else:
                # Palm view: opposite logic
                finger_up = landmarks[tip_idx][2] > landmarks[pip_idx][2]
            
            fingers.append(1 if finger_up else 0)
        
        return fingers
    
    def classify_letter(self, landmarks, is_back_of_hand=False):
        """
        Classify ASL letter based on hand landmarks
        Optimized for back-of-hand view with ML-inspired features
        
        Args:
            landmarks: List of hand landmarks [[id, x, y], ...]
            is_back_of_hand: Whether viewing back of hand
            
        Returns:
            Tuple of (predicted letter, confidence score)
        """
        if len(landmarks) < 21:
            return "", 0.0
        
        # NEW: Apply preprocessing for better stability
        self.landmark_history.append(landmarks)
        if len(self.landmark_history) >= 3:
            # Apply Kalman filtering for smoother landmarks
            landmarks = self.preprocessor.apply_kalman_filter(
                landmarks, 
                list(self.landmark_history),
                alpha=0.8  # Weight current frame highly but smooth noise
            )
        
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
        
        # NEW: Calculate finger curvatures (0=bent, 1=straight)
        index_curvature = self.calculate_finger_curvature(landmarks, 1)
        middle_curvature = self.calculate_finger_curvature(landmarks, 2)
        ring_curvature = self.calculate_finger_curvature(landmarks, 3)
        pinky_curvature = self.calculate_finger_curvature(landmarks, 4)
        
        # NEW: Get finger spreads
        finger_spreads = self.get_finger_spread(landmarks)
        thumb_index_spread = norm_dist(finger_spreads[0]) if len(finger_spreads) > 0 else 0
        index_middle_spread = norm_dist(finger_spreads[1]) if len(finger_spreads) > 1 else 0
        middle_ring_spread = norm_dist(finger_spreads[2]) if len(finger_spreads) > 2 else 0
        ring_pinky_spread = norm_dist(finger_spreads[3]) if len(finger_spreads) > 3 else 0
        
        # ========== IMPROVED LETTER RECOGNITION WITH STRICT GEOMETRIC ANALYSIS ==========
        # ========== V AND W FIRST - PREVENT O CONFUSION ==========
        
                # W: Three fingers extended (index, middle, ring) - BALANCED
        if fingers == [0, 1, 1, 1, 0]:
            # All three fingers STRAIGHT
            all_straight = (
                index_curvature > 0.85 and
                middle_curvature > 0.85 and
                ring_curvature > 0.85 and
                index_angle > 145 and
                middle_angle > 145 and
                ring_angle > 145
            )
            
            # Fingers must be SEPARATED (not together like closed fist)
            well_separated = (
                index_middle_spread > 0.15 and  # BALANCED: Reasonable gaps
                middle_ring_spread > 0.15
            )
            
            if all_straight and well_separated:
                return "W", 0.93
            elif all_straight or well_separated:
                return "W", 0.85
            else:
                return "W", 0.72
        
        # V: Index and middle separated (peace sign) - BALANCED
        if fingers == [0, 1, 1, 0, 0]:
            # Both fingers must be STRAIGHT
            both_straight = (
                index_curvature > 0.85 and
                middle_curvature > 0.85 and
                index_angle > 150 and
                middle_angle > 150
            )
            
            # Fingers must be SEPARATED with clear V shape
            clear_separation = index_middle_spread > 0.22  # BALANCED: Reasonable V
            
            # NOT together like U
            not_together = index_middle_spread > 0.18
            
            if both_straight and clear_separation:
                return "V", 0.93
            elif both_straight and not_together:
                return "V", 0.85
            elif not_together:
                return "V", 0.72
        
        # U: Index and middle TOGETHER, pointing up - BALANCED
        if fingers == [0, 1, 1, 0, 0]:
            # Both fingers STRAIGHT
            both_straight = (
                index_curvature > 0.85 and
                middle_curvature > 0.85 and
                index_angle > 145 and
                middle_angle > 145
            )
            
            # Fingers CLOSE TOGETHER (not separated)
            very_close = index_middle_spread < 0.20  # BALANCED: Close together
            
            if both_straight and very_close:
                return "U", 0.95
            elif very_close:
                return "U", 0.82
        
        # ========== LETTERS WITH [1,0,0,0,0]: A, O, C, S, T ==========
        # CRITICAL: These 5 letters share same finger pattern!
        # Differentiate by thumb-index distance:
        # A: 0.00-0.35 (thumb BESIDE fist, touching)
        # O: 0.25-0.40 (small circle)
        # C: 0.40-0.90 (wide C curve)
        # S: 0.35-0.60 (thumb across front)
        # T: 0.25-0.60 (thumb between fingers)
        
        if fingers == [1, 0, 0, 0, 0]:
            # Check ORDER: A -> O -> C -> S -> T
            
            # A: VERY CLOSE (thumb touching/beside fist)
            if thumb_index_norm < 0.35:
                all_closed = (
                    index_curvature < 0.70 and
                    middle_curvature < 0.70 and
                    ring_curvature < 0.70 and
                    pinky_curvature < 0.70
                )
                if all_closed:
                    return "A", 0.95
                else:
                    return "A", 0.85
            
            # O: SMALL CIRCLE (0.25-0.40)
            elif 0.25 <= thumb_index_norm < 0.42:
                all_bent = (
                    index_curvature < 0.75 and
                    middle_curvature < 0.75 and
                    ring_curvature < 0.75
                )
                if all_bent:
                    return "O", 0.95
                else:
                    return "O", 0.82
        
        # B: All four fingers extended together, thumb tucked - BALANCED
        if fingers == [0, 1, 1, 1, 1]:
            # All four fingers STRAIGHT
            all_straight = (
                index_curvature > 0.85 and
                middle_curvature > 0.85 and
                ring_curvature > 0.85 and
                pinky_curvature > 0.85
            )
            
            # Fingers CLOSE TOGETHER (not separated)
            close_together = (
                index_middle_spread < 0.25 and  # BALANCED: Reasonably close
                middle_ring_spread < 0.25 and
                ring_pinky_spread < 0.25
            )
            
            if all_straight and close_together:
                return "B", 0.93
            elif close_together:
                return "B", 0.85
            elif all_straight:
                return "B", 0.75
        
            
            # C: WIDE CURVE (0.42-0.90)
            elif thumb_index_norm >= 0.42:
                curved = (
                    index_curvature < 0.80 and
                    middle_curvature < 0.80 and
                    index_curvature > 0.50
                )
                if curved:
                    return "C", 0.90
                else:
                    return "C", 0.80
        
        # ========== LETTERS WITH [0,0,0,0,0]: E, M, N ==========
        # CRITICAL: These 3 letters share same finger pattern!
        # Differentiate by thumb position:
        # E: thumb on side of fist (normal closed hand)
        # M: thumb tucked under 3 fingers
        # N: thumb tucked under 2 fingers
        
        # ========== LETTERS WITH [1,1,0,0,0]: D, G, L ==========
        # CRITICAL: These 3 letters share same finger pattern!
        # D: Thumb touches middle finger
        # G: Thumb and index pointing horizontally (like gun)
        # L: Thumb and index at 90° (L shape)
        
        if fingers == [1, 1, 0, 0, 0]:
            # Check angle between thumb and index
            ti_angle = self.calculate_angle(thumb_tip[1:], wrist[1:], index_tip[1:])
            
            # D: Thumb touching middle finger area (priority check)
            if thumb_middle_norm < 0.6 and index_angle > 115:
                return "D", 0.85
            elif thumb_middle_norm < 0.7:
                return "D", 0.78
            
            # G: Thumb and index pointing sideways (gun shape)
            # Must have wide angle AND good separation
            elif 55 < ti_angle < 130 and thumb_index_norm > 0.6:
                return "G", 0.82
            elif 50 < ti_angle < 135 and thumb_index_norm > 0.5:
                return "G", 0.72
            
            # L: 90° angle (L shape)
            # Calculate aspect ratio for L shape
            else:
                horizontal_dist = abs(thumb_tip[1] - index_tip[1])
                vertical_dist = abs(thumb_tip[2] - index_tip[2]) + 0.001
                aspect_ratio = horizontal_dist / vertical_dist
                
                if aspect_ratio > 1.0 and index_angle > 115:
                    return "L", 0.87
                elif aspect_ratio > 0.8 and index_angle > 120:
                    return "L", 0.78
                else:
                    # Fallback to generic detection
                    return "D", 0.65
        
        
        if fingers == [0, 0, 0, 0, 0]:
            # Check thumb position relative to finger knuckles
            thumb_to_index_mcp = self.calculate_distance(thumb_tip[1:], index_mcp[1:])
            thumb_to_middle_mcp = self.calculate_distance(thumb_tip[1:], middle_mcp[1:])
            thumb_to_ring_mcp = self.calculate_distance(thumb_tip[1:], ring_mcp[1:])
            
            thumb_index_mcp_norm = norm_dist(thumb_to_index_mcp)
            thumb_middle_mcp_norm = norm_dist(thumb_to_middle_mcp)
            thumb_ring_mcp_norm = norm_dist(thumb_to_ring_mcp)
            
            # CRITICAL FIX: Use CLOSEST knuckle to determine M vs N vs E
            # M: Thumb closest to index knuckle (tucked under 3 fingers)
            # N: Thumb closest to middle knuckle (tucked under 2 fingers)  
            # E: Thumb not tucked under any knuckles (on side)
            
            min_knuckle_dist = min(thumb_index_mcp_norm, thumb_middle_mcp_norm, thumb_ring_mcp_norm)
            
            # M: Thumb tucked near INDEX knuckle
            if thumb_index_mcp_norm == min_knuckle_dist and thumb_index_mcp_norm < 0.50:
                return "M", 0.78
            
            # N: Thumb tucked near MIDDLE knuckle
            elif thumb_middle_mcp_norm == min_knuckle_dist and thumb_middle_mcp_norm < 0.50:
                return "N", 0.76
            
            # E: Normal closed fist (thumb on side, not tucked)
            else:
                if thumb_index_norm < 0.8:
                    return "E", 0.88
                else:
                    return "E", 0.75
        
        # F: OK sign - Index and thumb form circle, others up
        if fingers == [1, 0, 1, 1, 1]:
            # Thumb and index should be close (forming circle) (VERY RELAXED)
            if thumb_index_norm < 0.5 and middle_angle > 115:  # Much more lenient
                return "F", 0.87
            elif thumb_index_norm < 0.6:
                return "F", 0.80
        
        # NOTE: G and L are now checked in consolidated [1,1,0,0,0] block above
        
        # ========== LETTERS WITH [0,1,1,0,0]: V, U, H, R ==========
        # V: Fingers separated (peace sign) - checked at TOP
        # U: Fingers together - checked at TOP  
        # H: Fingers horizontal and parallel
        # R: Fingers crossed (not implemented yet)
        
        # H: Index and middle extended horizontally, close together
        if fingers == [0, 1, 1, 0, 0]:
            # Fingers should be parallel and close (VERY RELAXED)
            if index_middle_norm < 0.80 and abs(index_angle - middle_angle) < 40:  # Much more lenient
                return "H", 0.85
            elif index_middle_norm < 0.80:
                return "H", 0.75
        
        # I: Only pinky extended (little finger up)
        if fingers == [0, 0, 0, 0, 1]:
            # Pinky clearly extended, others closed (VERY RELAXED)
            pinky_angle = self.calculate_angle(pinky_mcp[1:], pinky_pip[1:], pinky_tip[1:])
            if pinky_angle > 115:  # Much more lenient
                return "I", 0.92
            elif pinky_angle > 115:
                return "I", 0.85
        
        # K: Index and middle up in V-shape, thumb TOUCHING middle knuckle - BALANCED (keep good A/K differentiation)
        if fingers == [1, 1, 1, 0, 0]:
            # Index and middle must be STRAIGHT (like V)
            index_straight = index_curvature > 0.82
            middle_straight = middle_curvature > 0.82
            
            # They should be SEPARATED (V-shape, not together)
            v_spread = index_middle_spread > 0.15  # Reasonable spread for V
            
            # Thumb MUST be touching/near middle finger base (KEY DIFFERENCE FROM A!)
            thumb_to_middle_mcp = self.calculate_distance(thumb_tip[1:], middle_mcp[1:])
            thumb_touching_middle = norm_dist(thumb_to_middle_mcp) < 0.30  # Close to middle knuckle
            
            # Thumb should be relatively HIGH (not super low like A)
            thumb_y = thumb_tip[2]
            thumb_not_too_low = thumb_y > index_mcp[2] + palm_width * 0.25  # Not too low
            
            if index_straight and middle_straight and v_spread and thumb_touching_middle:
                return "K", 0.92  # High confidence
            elif index_straight and middle_straight and thumb_touching_middle:
                return "K", 0.85
            elif thumb_touching_middle:
                return "K", 0.75
        
        # NOTE: L is now checked in consolidated [1,1,0,0,0] block above (with D and G)
        
        # NOTE: O is checked earlier (before C) to prevent C from stealing O detections
        
        # ========== LETTERS WITH [1,0,1,0,0]: P, Q ==========
        # CRITICAL: These 2 letters share same finger pattern!
        # P: Index bent down, middle pointing (normal orientation)
        # Q: Similar to P but thumb pointing DOWN
        
        if fingers == [1, 0, 1, 0, 0]:
            # Check thumb orientation
            thumb_down = thumb_tip[2] > thumb_mcp[2]
            
            # Q: Thumb pointing DOWN (priority)
            if thumb_down and middle_angle > 115:
                return "Q", 0.78
            elif thumb_down:
                return "Q", 0.70
            
            # P: Normal orientation (index bent, middle up)
            elif index_angle < 160 and middle_angle > 115:
                return "P", 0.82
            elif middle_angle > 120:
                return "P", 0.72
            else:
                return "P", 0.65
        
        # ========== LETTERS WITH [0,1,1,0,0]: V, U, H, R ==========
        # NOTE: V and U are already checked above
        # H: Fingers horizontal and parallel
        # R: Fingers crossed
        
        # NOTE: V, W, U are checked at the TOP of the function before B!
        
        # X: Index bent in hook shape
        if fingers == [0, 1, 0, 0, 0]:
            # Index bent/curved (VERY RELAXED)
            if index_angle < 160:  # Much more lenient
                return "X", 0.82
            elif index_angle < 170:
                return "X", 0.73
        
        # Y: Thumb and pinky extended (hang loose/shaka)
        if fingers == [1, 0, 0, 0, 1]:
            # Wide spread between thumb and pinky (VERY RELAXED)
            if thumb_pinky_norm > 0.95:  # Much more lenient
                return "Y", 0.92
            elif thumb_pinky_norm > 0.80:
                return "Y", 0.83
        
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
        
        # No match found
        return "", 0.0
    
    def classify_letter_with_features(self, landmarks, is_back_of_hand=False):
        """
        Enhanced classification using both geometric rules AND advanced features
        Returns letter with boosted confidence
        """
        # Get base classification
        letter, base_confidence = self.classify_letter(landmarks, is_back_of_hand)
        
        if letter == "" or base_confidence == 0.0:
            return "", 0.0
        
        # Apply advanced feature-based confidence boost
        enhanced_confidence = self.get_advanced_confidence_boost(
            landmarks, letter, base_confidence
        )
        
        return letter, enhanced_confidence
    
    def get_prediction(self, landmarks, is_back_of_hand=False, smoothing=True):
        """
        Get smoothed prediction with STRICT multi-frame validation and advanced features
        
        Args:
            landmarks: Hand landmarks
            is_back_of_hand: Whether viewing back of hand
            smoothing: Whether to apply temporal smoothing
            
        Returns:
            Tuple of (predicted letter, confidence)
        """
        # Use enhanced classification with advanced features
        letter, base_confidence = self.classify_letter_with_features(landmarks, is_back_of_hand)
        
        # Add to history
        self.letter_history.append(letter)
        
        if smoothing and len(self.letter_history) >= 3:  # STRICT: Need at least 3 frames
            # Require consistency across multiple frames (STRICT)
            recent = list(self.letter_history)[-7:]  # Last 7 frames
            
            # Count occurrences
            from collections import Counter
            letter_counts = Counter(recent)
            
            # Get most common letter
            if letter_counts:
                most_common_letter, count = letter_counts.most_common(1)[0]
                
                # STRICT: Require at least 3 consistent frames for high confidence
                if most_common_letter != "" and count >= 3:  # STRICT: Need 3+ frames
                    if most_common_letter == self.stable_letter:
                        self.stable_count += 1
                    else:
                        self.stable_letter = most_common_letter
                        self.stable_count = 1
                    
                    # Multi-factor confidence calculation (STRICT)
                    # Factor 1: Temporal consistency (need high ratio)
                    consistency_ratio = count / len(recent)
                    consistency_bonus = consistency_ratio * 0.15  # Up to +15% (reasonable)
                    
                    # Factor 2: Stability over time (sustained detection)
                    stability_bonus = min(self.stable_count * 0.03, 0.15)  # Up to +15% (reasonable)
                    
                    # Factor 3: Base confidence quality (STRICT threshold)
                    if base_confidence < 0.70:
                        quality_multiplier = 0.85  # Penalty for low confidence
                    elif base_confidence < 0.85:
                        quality_multiplier = 0.95  # Small penalty
                    else:
                        quality_multiplier = 1.0  # Full confidence
                    
                    # Calculate final confidence (STRICT)
                    final_confidence = base_confidence + consistency_bonus + stability_bonus
                    final_confidence = min(final_confidence * quality_multiplier, 1.0)
                    
                    # STRICT: Only return if final confidence meets threshold
                    if final_confidence >= 0.65:  # STRICT: Minimum 65% confidence
                        return self.stable_letter, final_confidence
                    else:
                        return "", 0.0  # Not confident enough
                elif most_common_letter != "" and count >= 2:  # Medium confidence
                    # 2 frames = lower confidence
                    return most_common_letter, base_confidence * 0.75
                else:
                    # Not enough consistency
                    return "", 0.0
        
        # Not enough history yet
        return "", 0.0
