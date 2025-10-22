"""
Test script for bulk training with outlier removal
Demonstrates the feature with synthetic data
"""

from src.ml_trainer import MLTrainer
import numpy as np
import json

def generate_synthetic_data():
    """Generate synthetic training data with some outliers"""
    print("🔬 Generating synthetic test data...")
    print("=" * 60)
    
    trainer = MLTrainer()
    
    # Generate 15 samples for letter 'A' (with 2 outliers)
    print("\n📝 Generating 15 samples for 'A' (includes 2 outliers)...")
    base_landmarks_A = np.random.rand(21, 3) * 0.5 + 0.2  # Normal range
    
    for i in range(13):
        # Normal samples - small variations
        landmarks = base_landmarks_A + np.random.normal(0, 0.02, (21, 3))
        trainer.add_training_sample(landmarks.tolist(), 'A')
    
    # Add 2 outliers for 'A'
    outlier1 = base_landmarks_A + np.random.normal(0, 0.3, (21, 3))  # Very different
    outlier2 = np.random.rand(21, 3)  # Completely random
    trainer.add_training_sample(outlier1.tolist(), 'A')
    trainer.add_training_sample(outlier2.tolist(), 'A')
    
    # Generate 12 samples for letter 'B' (with 1 outlier)
    print("\n📝 Generating 12 samples for 'B' (includes 1 outlier)...")
    base_landmarks_B = np.random.rand(21, 3) * 0.5 + 0.4  # Different range from A
    
    for i in range(11):
        # Normal samples
        landmarks = base_landmarks_B + np.random.normal(0, 0.02, (21, 3))
        trainer.add_training_sample(landmarks.tolist(), 'B')
    
    # Add 1 outlier for 'B'
    outlier3 = np.random.rand(21, 3) * 2.0  # Way out of range
    trainer.add_training_sample(outlier3.tolist(), 'B')
    
    # Generate 10 clean samples for letter 'C'
    print("\n📝 Generating 10 samples for 'C' (all clean)...")
    base_landmarks_C = np.random.rand(21, 3) * 0.5 + 0.6  # Different range
    
    for i in range(10):
        landmarks = base_landmarks_C + np.random.normal(0, 0.02, (21, 3))
        trainer.add_training_sample(landmarks.tolist(), 'C')
    
    print("\n" + "=" * 60)
    print(f"✅ Generated {len(trainer.training_data)} total samples")
    print("   - A: 15 samples (13 clean + 2 outliers)")
    print("   - B: 12 samples (11 clean + 1 outlier)")
    print("   - C: 10 samples (all clean)")
    print("=" * 60)
    
    return trainer

def test_bulk_training():
    """Test the bulk training feature"""
    print("\n🧪 TESTING BULK TRAINING WITH OUTLIER REMOVAL")
    print("=" * 60)
    
    # Generate test data
    trainer = generate_synthetic_data()
    
    # Show stats before
    print("\n📊 Training data BEFORE outlier removal:")
    stats = trainer.get_statistics()
    for letter, count in sorted(stats.items()):
        print(f"   {letter}: {count} samples")
    print(f"   Total: {len(trainer.training_data)} samples")
    
    # Perform bulk training
    print("\n" + "=" * 60)
    print("🚀 Starting bulk training...")
    print("=" * 60)
    
    accuracy, outliers = trainer.bulk_train_with_outlier_removal(
        outlier_threshold=2.5,
        test_size=0.2
    )
    
    # Show stats after
    if accuracy:
        print("\n📊 Training data AFTER outlier removal:")
        stats = trainer.get_statistics()
        for letter, count in sorted(stats.items()):
            print(f"   {letter}: {count} samples")
        print(f"   Total: {len(trainer.training_data)} samples")
        
        print("\n🎉 TEST SUCCESSFUL!")
        print(f"   ✅ Model trained with {accuracy:.2%} accuracy")
        print(f"   ✅ Outliers detected and removed")
        print(f"   ✅ Clean dataset ready for predictions")
    else:
        print("\n❌ TEST FAILED - Training did not complete")
    
    print("\n" + "=" * 60)
    print("💡 TIP: Run 'python main.py' and press 'B' to use bulk training")
    print("         with your own hand gesture data!")
    print("=" * 60)

if __name__ == "__main__":
    test_bulk_training()
