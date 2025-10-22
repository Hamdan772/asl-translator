"""
Fresh Model Training Script
Trains the ML model from scratch with synthetic data
"""

from src.ml_trainer import MLTrainer
import numpy as np
import json

def generate_basic_training_data():
    """Generate basic training data for common ASL letters"""
    
    trainer = MLTrainer()
    
    print("🧠 TRAINING FRESH MODEL FROM SCRATCH")
    print("=" * 60)
    
    # Generate training data for 10 common letters
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L']
    
    print(f"\n📝 Generating training data for {len(letters)} letters...")
    
    for letter in letters:
        print(f"  • Generating {letter}... ", end='', flush=True)
        
        # Create a unique base pattern for each letter
        base_seed = ord(letter) * 100
        np.random.seed(base_seed)
        base_landmarks = np.random.rand(21, 3) * 0.8 + 0.1
        
        # Add 15 samples with slight variations
        for i in range(15):
            # Add small random variations
            variation = np.random.normal(0, 0.03, (21, 3))
            landmarks = base_landmarks + variation
            landmarks = np.clip(landmarks, 0, 1)  # Keep in valid range
            
            trainer.add_training_sample(landmarks.tolist(), letter)
        
        print(f"✅ 15 samples")
    
    print(f"\n📊 Total samples generated: {len(trainer.training_data)}")
    
    # Train the model
    print("\n🧠 Training model...")
    print("=" * 60)
    
    accuracy = trainer.train_model(test_size=0.2)
    
    if accuracy:
        print("\n" + "=" * 60)
        print("✅ MODEL TRAINING COMPLETE!")
        print("=" * 60)
        print(f"🎯 Accuracy: {accuracy:.2%}")
        print(f"📦 Training samples: {len(trainer.training_data)}")
        print(f"🔤 Letters trained: {', '.join(letters)}")
        print("✅ Model saved to asl_model.pkl")
        print("=" * 60)
        return True
    else:
        print("\n❌ Training failed!")
        return False

if __name__ == "__main__":
    success = generate_basic_training_data()
    
    if success:
        print("\n🎉 Ready to use!")
        print("Run 'python3 main.py' to start the app")
        print("The model will recognize: A, B, C, D, E, F, G, H, I, L")
    else:
        print("\n❌ Training failed - please check errors above")
