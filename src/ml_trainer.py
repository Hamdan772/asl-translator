"""
Machine Learning Trainer for ASL Gestures
Trains a neural network on captured hand landmark data
Optimized for fast loading and crash prevention
"""

import json
import os
from datetime import datetime
from typing import Optional, Tuple, Dict, List

# Import only when needed to speed up loading
import numpy as np

class MLTrainer:
    """ML trainer with lazy sklearn import for faster startup"""
    
    def __init__(self, data_file="training_data.json", model_file="asl_model.pkl"):
        """Initialize the ML trainer with minimal overhead"""
        self.data_file = data_file
        self.model_file = model_file
        self.scaler_file = model_file.replace('.pkl', '_scaler.pkl')
        
        self.model = None
        self.scaler = None
        self.training_data = []
        
        # Lazy import flags
        self._sklearn_loaded = False
        self._MLPClassifier = None
        self._StandardScaler = None
        self._train_test_split = None
        
        # Load existing data (fast - no sklearn needed)
        self.load_training_data()
        
        # Only load model if it exists (deferred sklearn import)
        if os.path.exists(self.model_file):
            try:
                self.load_model()
            except Exception as e:
                print(f"⚠️  Could not load model: {e}")
    
    def _ensure_sklearn_loaded(self) -> bool:
        """Lazy load sklearn only when needed"""
        if self._sklearn_loaded:
            return True
        
        try:
            from sklearn.neural_network import MLPClassifier
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import StandardScaler
            import pickle
            
            self._MLPClassifier = MLPClassifier
            self._StandardScaler = StandardScaler
            self._train_test_split = train_test_split
            self._pickle = pickle
            self._sklearn_loaded = True
            
            # Initialize scaler now
            if self.scaler is None:
                self.scaler = StandardScaler()
            
            return True
        except ImportError as e:
            print(f"❌ sklearn not available: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading sklearn: {e}")
            return False
    
    def load_training_data(self):
        """Load existing training data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.training_data = json.load(f)
                print(f"✅ Loaded {len(self.training_data)} training samples")
            except Exception as e:
                print(f"⚠️  Could not load training data: {e}")
                self.training_data = []
        else:
            self.training_data = []
    
    def save_training_data(self):
        """Save training data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.training_data, f, indent=2)
            print(f"✅ Saved {len(self.training_data)} training samples")
        except Exception as e:
            print(f"❌ Could not save training data: {e}")
    
    def add_training_sample(self, landmarks, label):
        """
        Add a new training sample
        
        Args:
            landmarks: List of 21 hand landmarks (x, y, z for each)
            label: Letter label (A-Z)
        """
        # Flatten landmarks to 1D array (21 points × 3 coords = 63 features)
        flattened = []
        for point in landmarks:
            flattened.extend([point[0], point[1], point[2]])
        
        sample = {
            'landmarks': flattened,
            'label': label.upper(),
            'timestamp': datetime.now().isoformat()
        }
        
        self.training_data.append(sample)
        print(f"✅ Added training sample for '{label}' (total: {len(self.training_data)})")
        
        # Auto-save
        self.save_training_data()
        
        return True
    
    def get_statistics(self):
        """Get training statistics"""
        if not self.training_data:
            return {}
        
        stats = {}
        for sample in self.training_data:
            label = sample['label']
            stats[label] = stats.get(label, 0) + 1
        
        return stats
    
    def train_model(self, test_size=0.2) -> Optional[float]:
        """
        Train the ML model on collected data
        
        Returns:
            accuracy: Model accuracy on test set, or None if insufficient data
        """
        # Ensure sklearn is loaded
        if not self._ensure_sklearn_loaded():
            print("❌ Cannot train: sklearn not available")
            return None
        
        if len(self.training_data) < 10:
            print("❌ Need at least 10 samples to train model")
            return None
        
        # Check if we have at least 2 different labels
        labels = set(s['label'] for s in self.training_data)
        if len(labels) < 2:
            print("❌ Need samples from at least 2 different letters")
            return None
        
        try:
            print(f"🧠 Training model on {len(self.training_data)} samples...")
            
            # Prepare data
            X = np.array([s['landmarks'] for s in self.training_data])
            y = np.array([s['label'] for s in self.training_data])
            
            # Split into train/test
            X_train, X_test, y_train, y_test = self._train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y if len(labels) > 1 else None
            )
            
            # Scale features
            if self.scaler is None:
                self.scaler = self._StandardScaler()
            self.scaler.fit(X_train)
            X_train_scaled = self.scaler.transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train neural network
            self.model = self._MLPClassifier(
                hidden_layer_sizes=(128, 64, 32),
                activation='relu',
                solver='adam',
                max_iter=500,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            )
            
            self.model.fit(X_train_scaled, y_train)
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return None
        
        # Evaluate
        train_accuracy = self.model.score(X_train_scaled, y_train)
        test_accuracy = self.model.score(X_test_scaled, y_test)
        
        print(f"✅ Training accuracy: {train_accuracy:.2%}")
        print(f"✅ Test accuracy: {test_accuracy:.2%}")
        
        # Save model
        self.save_model()
        
        return test_accuracy
    
    def save_model(self):
        """Save trained model to disk"""
        if self.model is None:
            print("⚠️  No model to save")
            return
        
        if not self._ensure_sklearn_loaded():
            print("❌ Cannot save: sklearn not available")
            return
        
        try:
            with open(self.model_file, 'wb') as f:
                self._pickle.dump(self.model, f)
            with open(self.scaler_file, 'wb') as f:
                self._pickle.dump(self.scaler, f)
            print(f"✅ Model saved to {self.model_file}")
        except Exception as e:
            print(f"❌ Could not save model: {e}")
    
    def load_model(self):
        """Load trained model from disk"""
        if not (os.path.exists(self.model_file) and os.path.exists(self.scaler_file)):
            return False
        
        if not self._ensure_sklearn_loaded():
            print("⚠️  Cannot load model: sklearn not available")
            return False
        
        try:
            with open(self.model_file, 'rb') as f:
                self.model = self._pickle.load(f)
            with open(self.scaler_file, 'rb') as f:
                self.scaler = self._pickle.load(f)
            print(f"✅ Model loaded from {self.model_file}")
            return True
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")
            self.model = None
            return False
    
    def predict(self, landmarks):
        """
        Predict letter from landmarks using trained model
        
        Args:
            landmarks: List of 21 hand landmarks (x, y, z for each)
            
        Returns:
            (letter, confidence) or (None, 0) if no model
        """
        if self.model is None:
            return None, 0.0
        
        try:
            # Flatten landmarks
            flattened = []
            for point in landmarks:
                flattened.extend([point[0], point[1], point[2]])
            
            X = np.array([flattened])
            X_scaled = self.scaler.transform(X)
            
            # Get prediction and probability
            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]
            confidence = max(probabilities)
            
            return prediction, confidence
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None, 0.0
    
    def clear_data(self):
        """Clear all training data"""
        self.training_data = []
        self.save_training_data()
        print("✅ All training data cleared")
    
    def remove_samples(self, label):
        """Remove all samples for a specific label"""
        before = len(self.training_data)
        self.training_data = [s for s in self.training_data if s['label'] != label.upper()]
        after = len(self.training_data)
        removed = before - after
        self.save_training_data()
        print(f"✅ Removed {removed} samples for '{label}'")
        return removed
    
    def detect_and_remove_outliers(self, threshold=2.5, min_samples_per_label=5) -> Dict[str, int]:
        """
        Detect and remove anomalous samples using statistical methods
        
        Uses z-score based outlier detection within each label group.
        Samples that are statistically far from the mean are removed.
        
        Args:
            threshold: Z-score threshold (default 2.5 = ~99% confidence)
            min_samples_per_label: Minimum samples needed per label to perform outlier detection
            
        Returns:w
            Dict mapping labels to number of outliers removed
        """
        if len(self.training_data) < 10:
            print("⚠️  Need at least 10 samples for outlier detection")
            return {}
        
        # Group samples by label
        label_groups = {}
        for sample in self.training_data:
            label = sample['label']
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(sample)
        
        outliers_removed = {}
        samples_to_keep = []
        
        for label, samples in label_groups.items():
            if len(samples) < min_samples_per_label:
                # Not enough samples to detect outliers reliably
                samples_to_keep.extend(samples)
                print(f"⚠️  Skipping '{label}': only {len(samples)} samples (need {min_samples_per_label}+)")
                continue
            
            # Extract landmark arrays
            X = np.array([s['landmarks'] for s in samples])
            
            # Calculate mean and std for each feature
            mean = np.mean(X, axis=0)
            std = np.std(X, axis=0)
            
            # Avoid division by zero
            std = np.where(std == 0, 1, std)
            
            # Calculate z-scores for each sample
            z_scores = np.abs((X - mean) / std)
            
            # A sample is an outlier if ANY feature has z-score > threshold
            # More lenient: use average z-score across top 10 features
            max_z_scores = np.sort(z_scores, axis=1)[:, -10:]  # Top 10 most deviant features
            avg_top_z = np.mean(max_z_scores, axis=1)
            
            # Mark outliers
            is_outlier = avg_top_z > threshold
            
            outlier_count = np.sum(is_outlier)
            outliers_removed[label] = outlier_count
            
            # Keep non-outliers
            for i, sample in enumerate(samples):
                if not is_outlier[i]:
                    samples_to_keep.append(sample)
                else:
                    print(f"   ❌ Removed outlier for '{label}' (z-score: {avg_top_z[i]:.2f})")
        
        # Update training data
        before = len(self.training_data)
        self.training_data = samples_to_keep
        after = len(self.training_data)
        
        if before != after:
            self.save_training_data()
            print(f"\n✅ Removed {before - after} total outliers from {len(outliers_removed)} labels")
        
        return outliers_removed
    
    def bulk_train_with_outlier_removal(self, outlier_threshold=2.5, test_size=0.2) -> Optional[Tuple[float, Dict[str, int]]]:
        """
        Train model with automatic outlier removal
        
        This will:
        1. Detect and remove statistical outliers
        2. Train the model on cleaned data
        3. Report accuracy and outliers removed
        
        Args:
            outlier_threshold: Z-score threshold for outlier detection
            test_size: Fraction of data for testing
            
        Returns:
            (accuracy, outliers_dict) or (None, {}) if training failed
        """
        print("\n" + "=" * 60)
        print("🧹 BULK TRAINING WITH OUTLIER REMOVAL")
        print("=" * 60)
        
        if len(self.training_data) < 10:
            print("❌ Need at least 10 samples to train")
            return None, {}
        
        # Check if we have at least 2 different labels
        labels = set(s['label'] for s in self.training_data)
        if len(labels) < 2:
            print("❌ Need samples from at least 2 different letters")
            print(f"💡 Currently have: {', '.join(sorted(labels))}")
            return None, {}
        
        # Step 1: Remove outliers
        print("\n📊 Step 1: Detecting anomalous samples...")
        outliers = self.detect_and_remove_outliers(threshold=outlier_threshold)
        
        if outliers:
            print("\n📋 Outliers removed per letter:")
            for label, count in sorted(outliers.items()):
                if count > 0:
                    print(f"   {label}: {count} outliers removed")
        else:
            print("   ✅ No outliers detected - data looks clean!")
        
        # Step 2: Train model
        print("\n🧠 Step 2: Training model on cleaned data...")
        accuracy = self.train_model(test_size=test_size)
        
        if accuracy:
            print("\n" + "=" * 60)
            print(f"✅ BULK TRAINING COMPLETE!")
            print(f"🎯 Accuracy: {accuracy:.2%}")
            print(f"🧹 Outliers removed: {sum(outliers.values())}")
            print(f"📦 Final dataset: {len(self.training_data)} samples")
            print("=" * 60)
        
        return accuracy, outliers


if __name__ == "__main__":
    # Test the trainer
    trainer = MLTrainer()
    
    print("\n📊 Current statistics:")
    stats = trainer.get_statistics()
    for letter, count in sorted(stats.items()):
        print(f"  {letter}: {count} samples")
    
    print(f"\n📦 Total samples: {len(trainer.training_data)}")
    
    if len(trainer.training_data) >= 10:
        print("\n🧠 Training model...")
        accuracy = trainer.train_model()
        if accuracy:
            print(f"✅ Model trained with {accuracy:.2%} accuracy!")
