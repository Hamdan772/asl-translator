# 🎓 ASL Translator Training Guide

## The Problem
The synthetic training data created random patterns that don't represent real ASL hand positions. This is why everything was being detected as 'B' - the model learned meaningless patterns.

## The Solution
Train the model with **real hand gesture data** captured from your webcam.

## 📝 How to Train the Model

### Step 1: Start the App
```bash
python3 main.py
```

### Step 2: Enter Learning Mode
- Press **T** to enter LEARNING MODE
- You'll see a prompt asking you to type a letter

### Step 3: Capture Training Data
For each letter you want to recognize:

1. **Type the letter** (e.g., 'A') and press ENTER
2. **Make the ASL hand sign** for that letter
3. **Press ENTER** to capture the gesture (hold the sign steady!)
4. **Repeat 10-20 times** for the same letter
   - Vary your hand position slightly (different angles, distances)
   - Keep the core gesture the same
   - More samples = better accuracy

### Step 4: Train Multiple Letters
- Press **T** again to capture more letters
- Repeat for each letter: A, B, C, D, E, F, G, H, I, L, etc.
- Aim for **at least 10 letters** with 15+ samples each

### Step 5: Train the Model
Once you have enough samples:
- Press **B** for BULK TRAINING (recommended - removes outliers)
- OR Press **M** for standard training
- Wait for training to complete
- Check the accuracy score

### Step 6: Test Your Model
- Make different ASL signs
- The app will predict which letter you're showing
- If accuracy is low, capture more samples and retrain

## 📊 Check Your Progress
- Press **N** to show ML statistics
- See how many samples you have per letter
- Aim for balanced data (similar counts per letter)

## 💡 Tips for Best Results

1. **Consistent Lighting**: Train in good lighting
2. **Clear Background**: Avoid busy backgrounds
3. **Full Hand Visible**: Make sure all fingers are in frame
4. **Steady Gestures**: Hold each sign stable when capturing
5. **Variety**: Capture from slightly different angles/distances
6. **More Samples**: 15-20 samples per letter is ideal
7. **Balanced Training**: Train similar amounts for each letter

## 🎯 Recommended Training Set
Start with these common letters:
- **A, B, C, D, E, F, G, H, I, L, O, U, V, W, Y**

Each letter: 15-20 samples = 225-300 total samples

## ⚠️ Common Issues

**"Everything shows as one letter"**
- You need more variety in training data
- Capture from different angles
- Add more letters to the training set

**"Low accuracy"**
- Capture more samples (aim for 20+ per letter)
- Make sure gestures are distinct
- Use BULK TRAINING (Press B) to remove outliers

**"Model not detecting anything"**
- Press M or B to train the model first
- Make sure you have at least 2 letters with 10+ samples each

## 🔄 Retraining
If you're not happy with results:
1. Delete training data: `rm training_data.json asl_model.pkl asl_model_scaler.pkl`
2. Start fresh with the training process
3. Focus on capturing high-quality samples
