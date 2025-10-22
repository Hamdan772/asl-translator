# Bulk Training with Outlier Removal

## Overview
The bulk training feature automatically detects and removes anomalous training samples before training the ML model. This ensures higher model accuracy by filtering out poor-quality data.

## How It Works

### 1. Statistical Outlier Detection
- Uses **z-score** analysis to identify samples that are statistically far from the mean
- Analyzes all 63 hand landmark features (21 points × 3 coordinates)
- Default threshold: **2.5 standard deviations** (~99% confidence interval)
- Only processes labels with **5+ samples** to ensure reliability

### 2. Smart Filtering
- Calculates the top 10 most deviant features for each sample
- Averages their z-scores for a balanced outlier metric
- Removes samples where the average top z-score exceeds the threshold
- Reports which samples were removed and why

### 3. Automatic Training
- After removing outliers, immediately trains the model
- Uses cleaned dataset for better accuracy
- Saves the trained model automatically

## Usage

### Press 'B' Key
1. **Start the app**: `python main.py`
2. **Collect training data**: Press 'T' to enter learning mode
3. **Capture gestures**: Make signs and label them (10-15 per letter recommended)
4. **Bulk train**: Press 'B' to remove outliers and train

### Example Output
```
============================================================
🧹 BULK TRAINING WITH OUTLIER REMOVAL
============================================================

📊 Step 1: Detecting anomalous samples...
   ❌ Removed outlier for 'A' (z-score: 3.21)
   ❌ Removed outlier for 'B' (z-score: 2.87)
   ⚠️  Skipping 'C': only 3 samples (need 5+)

📋 Outliers removed per letter:
   A: 1 outliers removed
   B: 1 outliers removed

✅ Removed 2 total outliers from 2 labels

🧠 Step 2: Training model on cleaned data...
🧠 Training model on 48 samples...
✅ Training accuracy: 98.00%
✅ Test accuracy: 95.00%
✅ Model saved to asl_model.pkl

============================================================
✅ BULK TRAINING COMPLETE!
🎯 Accuracy: 95.00%
🧹 Outliers removed: 2
📦 Final dataset: 48 samples
============================================================

🎉 BULK TRAINING SUCCESS!
   📊 Before: 50 samples
   🧹 Removed: 2 anomalous samples
   📦 After: 48 clean samples
   🎯 Model accuracy: 95.00%
   🚀 ML predictions enabled!
```

## When to Use Bulk Training

### ✅ Use Bulk Training (Press 'B') When:
- You have **10+ samples** from **multiple letters**
- Some gestures were captured with poor hand positioning
- Training data includes mistakes or unclear signs
- You want maximum accuracy with automatic data cleaning
- You're training for the first time with lots of data

### ⚡ Use Regular Training (Press 'M') When:
- You have **high-quality**, carefully captured gestures
- Dataset is small and you know all samples are good
- Want faster training without outlier analysis
- Adding just a few new samples to existing model

## Technical Details

### Z-Score Method
- **Formula**: `z = (x - μ) / σ`
  - `x` = sample value
  - `μ` = mean of all samples for that letter
  - `σ` = standard deviation

- **Threshold**: 2.5 (default)
  - Samples beyond 2.5σ are considered outliers
  - Captures ~99% of normal distribution
  - Removes extreme anomalies

### Feature Analysis
- Analyzes all 63 features per sample
- Identifies top 10 most deviant features
- Averages their z-scores for robust detection
- Prevents false positives from single noisy features

### Minimum Sample Requirements
- **10 total samples**: Minimum for training
- **5 samples per label**: Minimum for outlier detection
- **2 different labels**: Minimum for model training
- Labels with fewer samples are skipped (not removed)

## Benefits

### 🎯 Higher Accuracy
- Removes bad training data automatically
- Model learns from clean, representative samples
- Reduces overfitting to anomalies

### 🧹 Data Quality
- Identifies samples captured with poor positioning
- Removes gestures that were moving during capture
- Filters out hand occlusions or weird angles

### ⚡ Automated Workflow
- One-click training with data cleaning
- No manual sample review needed
- Smart threshold works for most cases

### 📊 Transparency
- Reports which samples were removed
- Shows z-scores for removed outliers
- Displays before/after statistics

## Comparison: Press 'M' vs Press 'B'

| Feature | Press 'M' (Regular) | Press 'B' (Bulk) |
|---------|---------------------|------------------|
| **Speed** | ⚡ Fast (~1-2s) | 🐢 Slower (~3-5s) |
| **Outlier Detection** | ❌ None | ✅ Automatic |
| **Data Cleaning** | ❌ None | ✅ Yes |
| **Best For** | Clean data | Mixed quality data |
| **Recommended** | Experienced users | Beginners |
| **Sample Requirement** | 10+ samples | 10+ samples |

## Tips for Best Results

### 📸 Capture Quality Gestures
- Hold hand **completely still** during capture
- Use consistent **lighting** and **background**
- Keep hand at **same distance** from camera
- Make **clear, distinct** gestures

### 📊 Collect Enough Data
- **15-20 samples per letter** = Good
- **30-50 samples per letter** = Better
- **50+ samples per letter** = Best
- More data = more accurate outlier detection

### 🔁 Iterative Training
1. Collect initial batch (10-15 per letter)
2. Press 'B' to bulk train
3. Test the model with real gestures
4. Add more samples for problem letters
5. Press 'B' again to retrain

### 🎯 Check Statistics
- Press 'N' to view sample counts
- Ensure balanced data across letters
- Add more samples to underrepresented letters
- Press 'B' periodically as you add data

## Troubleshooting

### "Need at least 10 samples for bulk training"
- Collect more gesture samples using Learning Mode (Press 'T')
- You need at least 10 total samples from 2+ different letters

### "Skipping 'X': only 3 samples (need 5+)"
- That letter has too few samples for reliable outlier detection
- Samples are kept (not removed), just not analyzed
- Add 2+ more samples for that letter

### "No outliers detected - data looks clean!"
- Your training data is high quality! 🎉
- Model will still train on the existing data
- This is the ideal outcome

### Outliers Removed But Accuracy Still Low
- Collect more samples (aim for 20+ per letter)
- Ensure gestures are distinct and clear
- Check that you're showing the **back of hand** to camera
- Try different hand positions and angles

## Advanced: Customizing Threshold

### Modify in Code (src/ml_trainer.py)
```python
# More aggressive outlier removal (removes more)
outliers = self.detect_and_remove_outliers(threshold=2.0)

# More lenient (removes less)
outliers = self.detect_and_remove_outliers(threshold=3.0)
```

### Threshold Guidelines
- **2.0**: Aggressive (removes ~95% confidence)
- **2.5**: Standard (removes ~99% confidence) ✅ **DEFAULT**
- **3.0**: Lenient (removes ~99.7% confidence)
- **3.5+**: Very lenient (only extreme outliers)

## See Also
- [ML_TRAINING.md](ML_TRAINING.md) - Complete ML training guide
- [LEARNING_MODE.md](LEARNING_MODE.md) - How to capture gestures
- [USER_GUIDE.md](USER_GUIDE.md) - General usage instructions
