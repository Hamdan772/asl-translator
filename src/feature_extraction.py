"""
Advanced Feature Extraction for ASL Recognition
Based on research papers and ML best practices
"""
import numpy as np
import math
from typing import List, Tuple, Dict


class AdvancedFeatureExtractor:
    """
    Extract advanced geometric and statistical features from hand landmarks
    Inspired by:
    - Sign Language Recognition using CNNs (IEEE)
    - MediaPipe Hand Gesture Recognition (Google Research)
    - Real-time ASL Recognition Systems (ACM)
    """
    
    def __init__(self):
        """Initialize feature extractor with landmark indices"""
        # Finger landmark indices
        self.thumb_indices = [1, 2, 3, 4]
        self.index_indices = [5, 6, 7, 8]
        self.middle_indices = [9, 10, 11, 12]
        self.ring_indices = [13, 14, 15, 16]
        self.pinky_indices = [17, 18, 19, 20]
        self.finger_groups = [
            self.thumb_indices,
            self.index_indices,
            self.middle_indices,
            self.ring_indices,
            self.pinky_indices
        ]
    
    def extract_all_features(self, landmarks: List) -> Dict:
        """
        Extract comprehensive feature set
        
        Returns dict with:
        - geometric_features: distances, angles, ratios
        - statistical_features: mean, variance, entropy
        - topological_features: hand shape descriptors
        """
        if len(landmarks) < 21:
            return {}
        
        features = {}
        
        # 1. Geometric Features
        features['distances'] = self.extract_distance_features(landmarks)
        features['angles'] = self.extract_angle_features(landmarks)
        features['ratios'] = self.extract_ratio_features(landmarks)
        
        # 2. Statistical Features
        features['statistics'] = self.extract_statistical_features(landmarks)
        
        # 3. Topological Features
        features['topology'] = self.extract_topological_features(landmarks)
        
        # 4. Finger-specific Features
        features['fingers'] = self.extract_finger_features(landmarks)
        
        return features
    
    def extract_distance_features(self, landmarks: List) -> Dict:
        """
        Extract distance-based features
        - Inter-finger distances
        - Finger-to-palm distances
        - Normalized by palm width
        """
        wrist = landmarks[0]
        palm_width = self._calculate_distance(landmarks[5][1:], landmarks[17][1:])
        
        features = {}
        
        # 1. Fingertip-to-wrist distances (normalized)
        for i, (name, tip_idx) in enumerate([
            ('thumb', 4), ('index', 8), ('middle', 12), ('ring', 16), ('pinky', 20)
        ]):
            dist = self._calculate_distance(landmarks[tip_idx][1:], wrist[1:])
            features[f'{name}_wrist_dist'] = dist / palm_width
        
        # 2. Adjacent fingertip distances (normalized)
        tip_indices = [4, 8, 12, 16, 20]
        for i in range(len(tip_indices) - 1):
            dist = self._calculate_distance(
                landmarks[tip_indices[i]][1:],
                landmarks[tip_indices[i+1]][1:]
            )
            features[f'spread_{i}'] = dist / palm_width
        
        # 3. Finger length ratios (for hand shape)
        for i, (name, finger_indices) in enumerate([
            ('thumb', self.thumb_indices),
            ('index', self.index_indices),
            ('middle', self.middle_indices),
            ('ring', self.ring_indices),
            ('pinky', self.pinky_indices)
        ]):
            length = sum(
                self._calculate_distance(
                    landmarks[finger_indices[j]][1:],
                    landmarks[finger_indices[j+1]][1:]
                )
                for j in range(len(finger_indices) - 1)
            )
            features[f'{name}_length'] = length / palm_width
        
        return features
    
    def extract_angle_features(self, landmarks: List) -> Dict:
        """
        Extract angle-based features
        - Joint angles for each finger
        - Inter-finger angles
        - Palm plane angles
        """
        features = {}
        
        # 1. Finger joint angles
        finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
        for name, indices in zip(finger_names, self.finger_groups):
            if len(indices) >= 3:
                # Calculate angle at middle joint
                angle = self._calculate_angle(
                    landmarks[indices[0]][1:],
                    landmarks[indices[1]][1:],
                    landmarks[indices[2]][1:]
                )
                features[f'{name}_joint_angle'] = angle
                
                # Calculate angle at tip joint (if exists)
                if len(indices) >= 4:
                    angle_tip = self._calculate_angle(
                        landmarks[indices[1]][1:],
                        landmarks[indices[2]][1:],
                        landmarks[indices[3]][1:]
                    )
                    features[f'{name}_tip_angle'] = angle_tip
        
        # 2. Inter-finger angles (spread)
        tip_indices = [4, 8, 12, 16, 20]
        wrist = landmarks[0]
        for i in range(len(tip_indices) - 1):
            angle = self._calculate_angle(
                landmarks[tip_indices[i]][1:],
                wrist[1:],
                landmarks[tip_indices[i+1]][1:]
            )
            features[f'interfinger_angle_{i}'] = angle
        
        # 3. Hand orientation angle
        features['hand_orientation'] = self._calculate_hand_orientation(landmarks)
        
        return features
    
    def extract_ratio_features(self, landmarks: List) -> Dict:
        """
        Extract ratio-based features
        - Aspect ratios
        - Symmetry measures
        - Convexity measures
        """
        features = {}
        
        # 1. Bounding box aspect ratio
        x_coords = [lm[1] for lm in landmarks]
        y_coords = [lm[2] for lm in landmarks]
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        features['aspect_ratio'] = width / (height + 0.001)
        
        # 2. Hand compactness (area / perimeter^2)
        area = width * height
        perimeter = 2 * (width + height)
        features['compactness'] = area / (perimeter ** 2 + 0.001)
        
        # 3. Finger extension ratios
        wrist = landmarks[0]
        palm_center = landmarks[9]  # Middle finger MCP
        palm_dist = self._calculate_distance(wrist[1:], palm_center[1:])
        
        tip_indices = [4, 8, 12, 16, 20]
        for i, tip_idx in enumerate(tip_indices):
            tip_dist = self._calculate_distance(wrist[1:], landmarks[tip_idx][1:])
            features[f'extension_ratio_{i}'] = tip_dist / (palm_dist + 0.001)
        
        return features
    
    def extract_statistical_features(self, landmarks: List) -> Dict:
        """
        Extract statistical features
        - Mean, variance, skewness
        - Distribution characteristics
        """
        features = {}
        
        # Extract coordinates
        x_coords = np.array([lm[1] for lm in landmarks])
        y_coords = np.array([lm[2] for lm in landmarks])
        
        # 1. Position statistics
        features['x_mean'] = np.mean(x_coords)
        features['x_std'] = np.std(x_coords)
        features['x_min'] = np.min(x_coords)
        features['x_max'] = np.max(x_coords)
        
        features['y_mean'] = np.mean(y_coords)
        features['y_std'] = np.std(y_coords)
        features['y_min'] = np.min(y_coords)
        features['y_max'] = np.max(y_coords)
        
        # 2. Distribution moments
        features['x_skewness'] = self._calculate_skewness(x_coords)
        features['y_skewness'] = self._calculate_skewness(y_coords)
        
        # 3. Spread metrics
        features['coordinate_variance'] = np.var(x_coords) + np.var(y_coords)
        
        return features
    
    def extract_topological_features(self, landmarks: List) -> Dict:
        """
        Extract topological features
        - Hand shape descriptors
        - Convex hull properties
        - Finger arrangement patterns
        """
        features = {}
        
        # 1. Fingertip configuration
        tip_indices = [4, 8, 12, 16, 20]
        tips = [landmarks[i] for i in tip_indices]
        
        # Calculate convex hull area (simplified)
        features['tip_spread'] = self._calculate_spread_area(tips)
        
        # 2. Palm openness (distance from center to edges)
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        palm_center = [(wrist[1] + middle_mcp[1]) / 2, (wrist[2] + middle_mcp[2]) / 2]
        
        distances = []
        for tip_idx in tip_indices:
            dist = self._calculate_distance(palm_center, landmarks[tip_idx][1:])
            distances.append(dist)
        
        features['palm_openness'] = np.mean(distances)
        features['palm_openness_std'] = np.std(distances)
        
        # 3. Finger alignment (are fingers parallel or spread?)
        alignment_score = 0
        for i in range(len(tip_indices) - 1):
            # Calculate angle between adjacent fingers relative to palm
            angle = self._calculate_angle(
                landmarks[tip_indices[i]][1:],
                palm_center,
                landmarks[tip_indices[i+1]][1:]
            )
            alignment_score += abs(180 - angle)  # Deviation from straight
        
        features['finger_alignment'] = alignment_score / (len(tip_indices) - 1)
        
        return features
    
    def extract_finger_features(self, landmarks: List) -> Dict:
        """
        Extract per-finger features
        - Curvature
        - Extension
        - Direction
        """
        features = {}
        
        finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
        
        for name, indices in zip(finger_names, self.finger_groups):
            # 1. Finger curvature
            curvature = self._calculate_finger_curvature(landmarks, indices)
            features[f'{name}_curvature'] = curvature
            
            # 2. Finger direction vector
            if len(indices) >= 2:
                base = landmarks[indices[0]]
                tip = landmarks[indices[-1]]
                dx = tip[1] - base[1]
                dy = tip[2] - base[2]
                angle = math.atan2(dy, dx)
                features[f'{name}_direction'] = angle
            
            # 3. Finger straightness score
            straightness = self._calculate_straightness(landmarks, indices)
            features[f'{name}_straightness'] = straightness
        
        return features
    
    # Helper methods
    
    def _calculate_distance(self, p1, p2):
        """Euclidean distance"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def _calculate_angle(self, p1, p2, p3):
        """Angle at p2 formed by p1-p2-p3 in degrees"""
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
    
    def _calculate_hand_orientation(self, landmarks):
        """Calculate hand rotation angle"""
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        
        dx = middle_mcp[1] - wrist[1]
        dy = middle_mcp[2] - wrist[2]
        
        angle = math.degrees(math.atan2(dy, dx))
        return (angle + 360) % 360
    
    def _calculate_skewness(self, data):
        """Calculate skewness of distribution"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 3)
    
    def _calculate_spread_area(self, points):
        """Calculate approximate area covered by points"""
        x_coords = [p[1] for p in points]
        y_coords = [p[2] for p in points]
        
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        
        return width * height
    
    def _calculate_finger_curvature(self, landmarks, indices):
        """Calculate finger curvature (0=straight, 1=bent)"""
        if len(indices) < 2:
            return 0
        
        # Direct distance
        direct = self._calculate_distance(
            landmarks[indices[0]][1:],
            landmarks[indices[-1]][1:]
        )
        
        # Sum of segments
        segment_sum = sum(
            self._calculate_distance(
                landmarks[indices[i]][1:],
                landmarks[indices[i+1]][1:]
            )
            for i in range(len(indices) - 1)
        )
        
        # Straightness ratio (invert for curvature)
        if segment_sum == 0:
            return 0
        straightness = direct / segment_sum
        return 1 - straightness
    
    def _calculate_straightness(self, landmarks, indices):
        """Calculate how straight a finger is (0=bent, 1=straight)"""
        if len(indices) < 2:
            return 0
        
        # Direct distance
        direct = self._calculate_distance(
            landmarks[indices[0]][1:],
            landmarks[indices[-1]][1:]
        )
        
        # Sum of segments
        segment_sum = sum(
            self._calculate_distance(
                landmarks[indices[i]][1:],
                landmarks[indices[i+1]][1:]
            )
            for i in range(len(indices) - 1)
        )
        
        if segment_sum == 0:
            return 0
        
        return direct / segment_sum


class DataPreprocessor:
    """
    Data preprocessing techniques from ML research
    - Normalization
    - Augmentation
    - Noise reduction
    """
    
    @staticmethod
    def normalize_landmarks(landmarks: List, method='minmax') -> List:
        """
        Normalize landmark coordinates
        
        Methods:
        - 'minmax': Scale to [0, 1] range
        - 'zscore': Zero mean, unit variance
        - 'palm': Normalize by palm size (scale-invariant)
        """
        if len(landmarks) < 21:
            return landmarks
        
        normalized = [lm.copy() for lm in landmarks]
        
        if method == 'minmax':
            x_coords = [lm[1] for lm in landmarks]
            y_coords = [lm[2] for lm in landmarks]
            
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            x_range = x_max - x_min if x_max != x_min else 1
            y_range = y_max - y_min if y_max != y_min else 1
            
            for i in range(len(normalized)):
                normalized[i][1] = (landmarks[i][1] - x_min) / x_range
                normalized[i][2] = (landmarks[i][2] - y_min) / y_range
        
        elif method == 'palm':
            wrist = landmarks[0]
            palm_width = math.sqrt(
                (landmarks[5][1] - landmarks[17][1])**2 +
                (landmarks[5][2] - landmarks[17][2])**2
            )
            
            if palm_width == 0:
                return normalized
            
            for i in range(len(normalized)):
                normalized[i][1] = (landmarks[i][1] - wrist[1]) / palm_width
                normalized[i][2] = (landmarks[i][2] - wrist[2]) / palm_width
        
        return normalized
    
    @staticmethod
    def apply_kalman_filter(current: List, history: List, alpha=0.7) -> List:
        """
        Apply Kalman-like filtering for smoothing
        alpha: Weight for current observation (0-1)
        """
        if len(history) == 0:
            return current
        
        filtered = []
        prev = history[-1]
        
        for i in range(len(current)):
            filtered_point = [
                current[i][0],  # ID stays same
                alpha * current[i][1] + (1 - alpha) * prev[i][1],  # Filtered X
                alpha * current[i][2] + (1 - alpha) * prev[i][2]   # Filtered Y
            ]
            filtered.append(filtered_point)
        
        return filtered
    
    @staticmethod
    def remove_outliers(landmarks: List, history: List, threshold=0.2) -> List:
        """
        Remove outlier landmarks using median filtering
        threshold: Maximum allowed deviation from median
        """
        if len(history) < 3:
            return landmarks
        
        cleaned = landmarks.copy()
        
        for i in range(len(landmarks)):
            # Get history for this landmark
            hist_x = [h[i][1] for h in history[-5:]]
            hist_y = [h[i][2] for h in history[-5:]]
            
            # Calculate median
            median_x = np.median(hist_x)
            median_y = np.median(hist_y)
            
            # Calculate deviation
            dev_x = abs(landmarks[i][1] - median_x)
            dev_y = abs(landmarks[i][2] - median_y)
            
            # If outlier, replace with median
            if dev_x > threshold * (max(hist_x) - min(hist_x)):
                cleaned[i][1] = median_x
            if dev_y > threshold * (max(hist_y) - min(hist_y)):
                cleaned[i][2] = median_y
        
        return cleaned
