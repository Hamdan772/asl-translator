#!/usr/bin/env python3
"""
Training Data Diagnostic Tool
Analyzes your training data to find problematic samples
"""

import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from collections import defaultdict

def analyze_finger_states(landmarks):
    """Analyze which fingers are extended"""
    # Convert flat list to points
    points = []
    for i in range(0, len(landmarks), 3):
        points.append([landmarks[i], landmarks[i+1], landmarks[i+2]])
    points = np.array(points)
    
    # Finger tip indices: [thumb, index, middle, ring, pinky]
    tip_indices = [4, 8, 12, 16, 20]
    # Finger base indices (knuckles)
    base_indices = [2, 5, 9, 13, 17]
    
    finger_states = {}
    finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
    
    for i, (tip_idx, base_idx, name) in enumerate(zip(tip_indices, base_indices, finger_names)):
        tip = points[tip_idx]
        base = points[base_idx]
        wrist = points[0]
        
        # Distance from tip to wrist vs base to wrist
        tip_dist = np.linalg.norm(tip[:2] - wrist[:2])  # Use only x,y
        base_dist = np.linalg.norm(base[:2] - wrist[:2])
        
        # If tip is significantly farther from wrist than base, finger is extended
        extension_ratio = tip_dist / (base_dist + 0.001)
        finger_states[name] = extension_ratio > 1.2  # True if extended
    
    return finger_states

def main():
    print("=" * 60)
    print("🔍 ASL TRAINING DATA DIAGNOSTIC TOOL")
    print("=" * 60)
    print()
    
    # Load training data
    try:
        with open('training_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ training_data.json not found!")
        return
    
    if not data:
        print("❌ No training data found!")
        return
    
    print(f"📊 Loaded {len(data)} samples\n")
    
    # Group by letter
    by_letter = defaultdict(list)
    for sample in data:
        by_letter[sample['label']].append(sample['landmarks'])
    
    # Expected finger states for A, V, W
    expected_patterns = {
        'A': {
            'description': 'Closed fist (all fingers down)',
            'expected': {'thumb': False, 'index': False, 'middle': False, 'ring': False, 'pinky': False}
        },
        'V': {
            'description': 'Index + Middle fingers UP, others down',
            'expected': {'thumb': False, 'index': True, 'middle': True, 'ring': False, 'pinky': False}
        },
        'W': {
            'description': 'Index + Middle + Ring fingers UP, others down',
            'expected': {'thumb': False, 'index': True, 'middle': True, 'ring': True, 'pinky': False}
        }
    }
    
    # Analyze each letter
    for letter in sorted(by_letter.keys()):
        samples = by_letter[letter]
        print(f"\n{'=' * 60}")
        print(f"📋 Letter: {letter} ({len(samples)} samples)")
        
        if letter in expected_patterns:
            print(f"✅ Expected: {expected_patterns[letter]['description']}")
        
        print(f"{'=' * 60}")
        
        # Analyze finger states for each sample
        finger_counts = defaultdict(int)
        problematic_samples = []
        
        for idx, landmarks in enumerate(samples):
            states = analyze_finger_states(landmarks)
            
            # Count finger states
            for finger, is_up in states.items():
                if is_up:
                    finger_counts[finger] += 1
            
            # Check if it matches expected pattern
            if letter in expected_patterns:
                expected = expected_patterns[letter]['expected']
                matches = all(states[f] == expected[f] for f in expected.keys())
                
                if not matches:
                    # Find differences
                    diffs = []
                    for finger in expected.keys():
                        if states[finger] != expected[finger]:
                            state = "UP" if states[finger] else "DOWN"
                            expected_state = "UP" if expected[finger] else "DOWN"
                            diffs.append(f"{finger}: {state} (expected {expected_state})")
                    
                    problematic_samples.append((idx + 1, diffs))
        
        # Print finger statistics
        print(f"\n📊 Finger Extension Statistics:")
        total = len(samples)
        for finger in ['thumb', 'index', 'middle', 'ring', 'pinky']:
            count = finger_counts[finger]
            pct = (count / total) * 100
            emoji = "👆" if pct > 50 else "👇"
            print(f"   {emoji} {finger.capitalize():8s}: {count:3d}/{total} ({pct:5.1f}%) extended")
        
        # Report problematic samples
        if letter in expected_patterns and problematic_samples:
            print(f"\n⚠️  Found {len(problematic_samples)} PROBLEMATIC samples:")
            for sample_num, diffs in problematic_samples[:10]:  # Show first 10
                print(f"   Sample #{sample_num}: {', '.join(diffs)}")
            if len(problematic_samples) > 10:
                print(f"   ... and {len(problematic_samples) - 10} more")
            
            print(f"\n💡 TIP: Delete training_data.json and retrain {letter} more carefully!")
    
    print(f"\n{'=' * 60}")
    print("🎯 RECOMMENDATIONS:")
    print("=" * 60)
    
    # Check if A, V, W all exist
    if 'A' in by_letter and 'V' in by_letter and 'W' in by_letter:
        # Get average finger states
        def get_avg_fingers(letter):
            samples = by_letter[letter]
            totals = defaultdict(int)
            for landmarks in samples:
                states = analyze_finger_states(landmarks)
                for finger, is_up in states.items():
                    if is_up:
                        totals[finger] += 1
            return {f: (totals[f] / len(samples)) for f in ['thumb', 'index', 'middle', 'ring', 'pinky']}
        
        a_fingers = get_avg_fingers('A')
        v_fingers = get_avg_fingers('V')
        w_fingers = get_avg_fingers('W')
        
        # Check for proper differentiation
        issues = []
        
        # A should have all fingers down
        if any(pct > 0.3 for pct in a_fingers.values()):
            issues.append("❌ Letter A: Some fingers appear UP in many samples (should all be DOWN)")
        
        # V should have index+middle up, ring down
        if v_fingers['index'] < 0.7 or v_fingers['middle'] < 0.7:
            issues.append("❌ Letter V: Index/Middle fingers not consistently UP")
        if v_fingers['ring'] > 0.3:
            issues.append("❌ Letter V: Ring finger appears UP (should be DOWN)")
        
        # W should have index+middle+ring up
        if w_fingers['index'] < 0.7 or w_fingers['middle'] < 0.7 or w_fingers['ring'] < 0.7:
            issues.append("❌ Letter W: Index/Middle/Ring fingers not consistently UP")
        
        # W and V should be clearly different (ring finger)
        if abs(v_fingers['ring'] - w_fingers['ring']) < 0.4:
            issues.append("⚠️  V and W are TOO SIMILAR: Ring finger state not clearly different")
        
        if issues:
            print("\n🚨 PROBLEMS FOUND:\n")
            for issue in issues:
                print(f"   {issue}")
            print("\n💡 SOLUTION:")
            print("   1. Delete training_data.json")
            print("   2. Retrain with CLEAR hand positions:")
            print("      • A: Make a TIGHT fist, ALL fingers curled")
            print("      • V: ONLY index + middle UP (✌️ peace sign)")
            print("      • W: index + middle + ring UP (👌 but 3 fingers)")
            print("   3. Use bulk training (press B) after capturing samples")
        else:
            print("\n✅ Your training data looks GOOD!")
            print("   The issue might be:")
            print("   • Not enough samples (try 30-40 per letter)")
            print("   • Camera angle or lighting")
            print("   • Hand position varying too much")
    
    print()

if __name__ == '__main__':
    main()
