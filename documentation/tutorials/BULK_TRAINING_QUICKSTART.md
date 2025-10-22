# Quick Reference: Bulk Training Feature

## What's New?
Added **Press 'B'** for bulk training with automatic outlier removal!

## Key Bindings

| Key | Action | Description |
|-----|--------|-------------|
| **T** | Learning Mode | Capture gestures and label them |
| **M** | Quick Train | Train model (no outlier removal) |
| **B** | Bulk Train | Train model + remove anomalies ✨ **NEW** |
| **N** | Statistics | View training data stats |

## When to Use What?

### Press 'M' (Quick Training)
- ✅ When you have **clean, high-quality** samples
- ✅ When you want **faster** training
- ✅ When dataset is **small** and verified
- ⚡ Speed: ~1-2 seconds

### Press 'B' (Bulk Training) ✨ **RECOMMENDED**
- ✅ When you have **mixed quality** samples
- ✅ When some gestures were **captured poorly**
- ✅ When training for the **first time**
- ✅ When you want **maximum accuracy**
- 🐢 Speed: ~3-5 seconds (worth it!)

## Example Workflow

```bash
1. python main.py           # Start the app
2. Press 'T'                # Enter learning mode
3. Make gesture → Type 'A'  # Capture and label
4. Repeat 10-15 times       # Collect samples
5. Press 'B'                # Bulk train with outlier removal ✨
6. Test the model!          # Make gestures, see predictions
```

## What Happens When You Press 'B'?

```
🧹 Step 1: Outlier Detection
   ❌ Removed outlier for 'A' (z-score: 3.21)
   ❌ Removed outlier for 'B' (z-score: 2.87)
   ✅ 2 anomalies detected

🧠 Step 2: Model Training
   🧠 Training on cleaned data...
   ✅ 95% accuracy achieved!

🎉 Result:
   📦 48 clean samples
   🎯 95% accuracy
   🚀 ML enabled!
```

## Technical Details

### Outlier Detection Method
- **Algorithm**: Z-score statistical analysis
- **Threshold**: 2.5 standard deviations
- **Features**: Analyzes all 63 hand landmarks
- **Min samples**: Needs 5+ samples per letter

### What Gets Removed?
- ❌ Gestures captured while hand was moving
- ❌ Poor hand positioning
- ❌ Occluded or partial hand views
- ❌ Lighting issues
- ❌ Accidental captures

### What Gets Kept?
- ✅ Stable, clear gestures
- ✅ Consistent hand positioning
- ✅ Representative samples
- ✅ High-quality data

## Benefits

| Benefit | Description |
|---------|-------------|
| 🎯 **Higher Accuracy** | Removes bad data → better predictions |
| 🧹 **Automatic Cleaning** | No manual review needed |
| 📊 **Transparency** | See exactly what was removed |
| ⚡ **One-Click** | Training + cleaning in one step |
| 🔧 **Smart Thresholds** | Works well out of the box |

## Tips for Best Results

1. **Collect 15-20 samples per letter**
   - More data = better outlier detection
   
2. **Hold gestures still**
   - Stable captures = fewer outliers
   
3. **Use consistent lighting**
   - Reduces noise in data
   
4. **Check statistics** (Press 'N')
   - See what got removed
   - Add more samples if needed

5. **Retrain periodically** (Press 'B')
   - As you add more samples
   - After fixing problem gestures

## Troubleshooting

### "Need at least 10 samples for bulk training"
**Solution**: Press 'T' and collect more gesture samples

### "Skipping 'X': only 3 samples (need 5+)"
**Solution**: Add 2+ more samples for that letter (samples are kept, just not analyzed)

### Accuracy still low after bulk training
**Solution**: 
- Collect 20+ samples per letter
- Ensure gestures are clear and distinct
- Check you're showing **back of hand** to camera

## Testing

Run the test script to see bulk training in action:
```bash
python3 test_bulk_training.py
```

This generates synthetic data with outliers and demonstrates the feature.

## Learn More

- [BULK_TRAINING.md](documentation/BULK_TRAINING.md) - Detailed guide
- [ML_TRAINING.md](documentation/ML_TRAINING.md) - ML training overview
- [LEARNING_MODE.md](documentation/LEARNING_MODE.md) - How to capture gestures

## Summary

**Press 'B' for bulk training** = Better accuracy through automatic outlier removal! 🎉

It's the recommended way to train your model, especially when starting out or when you have lots of data.
