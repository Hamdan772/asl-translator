"""
Finger Pattern Matcher for ASL Recognition
Combines finger states, landmark positions, and photo similarity
"""

import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional

class FingerMatcher:
    """
    Advanced finger pattern matcher that uses:
    1. Finger states (which fingers are UP/DOWN)
    2. Landmark geometry (finger positions, angles, distances)
    3. Photo similarity (HOG features, template matching)
    """
    
    def __init__(self):
        self.patterns = {}  # Store finger patterns for each letter
        
    def add_pattern(self, letter: str, finger_states: Dict[str, bool], 
                   landmarks: List, photo_path: Optional[str] = None):
        """
        Add a finger pattern for a letter
        
        Args:
            letter: The ASL letter
            finger_states: Dict with thumb, index, middle, ring, pinky states
            landmarks: Hand landmark positions
            photo_path: Path to training photo (optional)
        """
        if letter not in self.patterns:
            self.patterns[letter] = []
        
        # Calculate geometric features
        geometric_features = self._extract_geometric_features(landmarks)
        
        # Load photo if available
        photo_features = None
        if photo_path:
            photo_features = self._load_photo_features(photo_path)
        
        pattern = {
            'finger_states': finger_states.copy(),
            'finger_count': sum(1 for v in finger_states.values() if v),
            'geometric_features': geometric_features,
            'photo_features': photo_features,
            'landmarks': landmarks.copy()
        }
        
        self.patterns[letter].append(pattern)
    
    def _extract_geometric_features(self, landmarks) -> Dict:
        """Extract geometric features from landmarks"""
        try:
            # Get key points
            wrist = np.array([landmarks[0][1], landmarks[0][2]])
            thumb_tip = np.array([landmarks[4][1], landmarks[4][2]])
            index_tip = np.array([landmarks[8][1], landmarks[8][2]])
            middle_tip = np.array([landmarks[12][1], landmarks[12][2]])
            ring_tip = np.array([landmarks[16][1], landmarks[16][2]])
            pinky_tip = np.array([landmarks[20][1], landmarks[20][2]])
            
            # Calculate distances
            features = {
                'index_middle_dist': np.linalg.norm(index_tip - middle_tip),
                'middle_ring_dist': np.linalg.norm(middle_tip - ring_tip),
                'ring_pinky_dist': np.linalg.norm(ring_tip - pinky_tip),
                'thumb_index_dist': np.linalg.norm(thumb_tip - index_tip),
                'hand_span': np.linalg.norm(index_tip - pinky_tip),
                'palm_to_index': np.linalg.norm(wrist - index_tip),
                'palm_to_middle': np.linalg.norm(wrist - middle_tip),
                'palm_to_ring': np.linalg.norm(wrist - ring_tip),
            }
            
            return features
        except:
            return {}
    
    def _load_photo_features(self, photo_path: str) -> Optional[np.ndarray]:
        """Load and extract features from photo"""
        try:
            img = cv2.imread(photo_path)
            if img is None:
                return None
            
            # Resize to standard size
            img_resized = cv2.resize(img, (64, 64))
            gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
            
            # Extract HOG features
            win_size = (64, 64)
            block_size = (16, 16)
            block_stride = (8, 8)
            cell_size = (8, 8)
            nbins = 9
            
            hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
            features = hog.compute(gray)
            
            return features.flatten()
        except:
            return None
    
    def match(self, finger_states: Dict[str, bool], landmarks: List, 
             current_image: Optional[np.ndarray] = None) -> Tuple[Optional[str], float, Dict]:
        """
        Match current finger pattern against stored patterns
        
        Returns:
            (best_letter, confidence, debug_info)
        """
        if not self.patterns:
            return None, 0.0, {}
        
        current_finger_count = sum(1 for v in finger_states.values() if v)
        current_geometric = self._extract_geometric_features(landmarks)
        current_photo_features = None
        
        if current_image is not None:
            try:
                img_resized = cv2.resize(current_image, (64, 64))
                gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
                
                win_size = (64, 64)
                block_size = (16, 16)
                block_stride = (8, 8)
                cell_size = (8, 8)
                nbins = 9
                
                hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
                current_photo_features = hog.compute(gray).flatten()
            except:
                pass
        
        # Score each letter
        scores = {}
        for letter, patterns in self.patterns.items():
            max_score = 0.0
            
            for pattern in patterns:
                score = 0.0
                weights_sum = 0.0
                
                # 1. Finger state matching (40% weight)
                finger_match_score = self._match_finger_states(finger_states, pattern['finger_states'])
                score += finger_match_score * 0.4
                weights_sum += 0.4
                
                # 2. Finger count exact match (20% weight)
                if current_finger_count == pattern['finger_count']:
                    score += 1.0 * 0.2
                weights_sum += 0.2
                
                # 3. Geometric similarity (20% weight)
                geo_score = self._match_geometric_features(current_geometric, pattern['geometric_features'])
                score += geo_score * 0.2
                weights_sum += 0.2
                
                # 4. Photo similarity (20% weight) - only if both have photos
                if current_photo_features is not None and pattern['photo_features'] is not None:
                    photo_score = self._match_photo_features(current_photo_features, pattern['photo_features'])
                    score += photo_score * 0.2
                    weights_sum += 0.2
                
                # Normalize by actual weights used
                if weights_sum > 0:
                    score = score / weights_sum
                
                max_score = max(max_score, score)
            
            scores[letter] = max_score
        
        # Get best match
        if not scores:
            return None, 0.0, {}
        
        best_letter = max(scores, key=scores.get)
        confidence = scores[best_letter]
        
        debug_info = {
            'all_scores': scores,
            'finger_count': current_finger_count,
            'finger_states': finger_states
        }
        
        return best_letter, confidence, debug_info
    
    def _match_finger_states(self, states1: Dict, states2: Dict) -> float:
        """Calculate similarity between two finger state dicts"""
        total_fingers = 5
        matching = 0
        
        for finger in ['thumb', 'index', 'middle', 'ring', 'pinky']:
            if states1.get(finger, False) == states2.get(finger, False):
                matching += 1
        
        return matching / total_fingers
    
    def _match_geometric_features(self, features1: Dict, features2: Dict) -> float:
        """Calculate similarity between geometric features"""
        if not features1 or not features2:
            return 0.5  # Neutral score if missing
        
        # Compare normalized distances
        keys = set(features1.keys()) & set(features2.keys())
        if not keys:
            return 0.5
        
        similarities = []
        for key in keys:
            val1 = features1[key]
            val2 = features2[key]
            
            # Normalized difference (smaller is better)
            max_val = max(val1, val2, 0.001)
            diff = abs(val1 - val2) / max_val
            similarity = 1.0 - min(diff, 1.0)
            similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.5
    
    def _match_photo_features(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """Calculate similarity between HOG features"""
        try:
            # Cosine similarity
            dot_product = np.dot(features1, features2)
            norm1 = np.linalg.norm(features1)
            norm2 = np.linalg.norm(features2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.5
            
            cosine_sim = dot_product / (norm1 * norm2)
            # Convert from [-1, 1] to [0, 1]
            return (cosine_sim + 1.0) / 2.0
        except:
            return 0.5
    
    def get_statistics(self) -> Dict:
        """Get statistics about stored patterns"""
        stats = {}
        for letter, patterns in self.patterns.items():
            stats[letter] = {
                'count': len(patterns),
                'with_photos': sum(1 for p in patterns if p['photo_features'] is not None)
            }
        return stats
