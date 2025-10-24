# 🤟 ASL Translator - Advanced Real-Time Sign Language Recognition# 🤟 ASL Translator v2.0 - Optimized Edition



![Python](https://img.shields.io/badge/python-3.9+-blue.svg)<div align="center">

![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)

![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.8-orange.svg)[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)

![License](https://img.shields.io/badge/license-MIT-blue.svg)[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.8-green.svg)](https://mediapipe.dev/)

[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org/)

An intelligent American Sign Language (ASL) translator that uses **computer vision**, **machine learning**, and **multi-modal recognition** to convert hand gestures into text in real-time.[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)



## ✨ Features*Real-time American Sign Language translator with ML training, photo capture, and enhanced visual feedback*



### 🎯 Core Recognition System[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Training](#-training-guide) • [Documentation](#-documentation)

- **Real-time hand tracking** with 21 landmark points

- **Multi-modal recognition** combining 4 intelligence layers:</div>

  - 🖐️ Finger state detection (which fingers are UP/DOWN)

  - 🧠 Neural network prediction (396 features)---

  - 📏 Geometric analysis (finger spacing, distances)

  - 📸 Visual features (HOG image analysis)## 🚀 What's New (October 2024)

- **Rule-based corrections** to prevent common confusions (e.g., V vs W)

- **Confidence scoring** with ambiguity detection### ✨ Latest Features

- **Adaptive learning** through custom training

- 📸 **Training Photo Capture** - Automatically saves photos (with/without dots) during training

### 🎓 Training System- 🎨 **Enhanced Visuals** - 121 colorful tracking dots, finger labels, and hand highlighting

- **Interactive training mode** - train any ASL letter- 📊 **Finger Status Panel** - Real-time finger detection (UP/DOWN) during training

- **Photo capture** - automatically saves hand images during training- ⚡ **Performance Optimized** - 2x faster FPS (40-50 FPS), improved thumb detection

- **Finger state recording** - captures which fingers are extended- 🗂️ **Better Organization** - Structured file layout with docs/ and scripts/ folders

- **Geometric features** - records finger positions and angles

- **Bulk training** - removes outliers for better accuracy---

- **Debug mode** - detailed logging for troubleshooting

## ⚠️ MODEL TRAINING REQUIRED

### 📊 Advanced Features

- **121 visual markers** - 21 green landmarks + 100 yellow connections> **Note**: This repository does not include pre-trained models. Train with your own gestures for personalized accuracy.

- **Finger status panel** - real-time UP/DOWN indicator for each finger

- **Confidence indicators** - shows prediction certainty**Status**: Ready for training  

- **Hand stability detection** - ensures accurate captures**Training Data**: Empty - Start fresh!  

- **Session statistics** - tracks letters, accuracy, speed**Photos**: Automatically saved to `training_photos/` during training



## 🚀 Getting Started📚 **See [docs/MODEL_STATUS.md](docs/MODEL_STATUS.md) for detailed instructions**



### Prerequisites---



```bash## 📋 Overview

Python 3.9 or higher

Webcam/CameraASL Translator is a real-time hand gesture recognition system with advanced visual feedback, ML training capabilities, and automatic photo documentation of training sessions.

```

### ✨ Core Features

### Installation

#### Training & ML

1. **Clone the repository**- 🤖 **Easy Training Mode** - Press letter keys + ENTER to capture samples

```bash- 📸 **Auto Photo Capture** - Saves training photos with dots AND clean versions

git clone https://github.com/Hamdan772/asl-translator.git- 🎯 **Bulk Training** - Automatic outlier removal (z-score method)

cd asl-translator- 🧠 **ML Classifier** - Neural network (128→64→32 neurons)

```- 📊 **Prediction Debug** - See top 3 predictions with confidence percentages



2. **Install dependencies**#### Visual Enhancements

```bash- 🎨 **121 Tracking Dots** - 21 green landmarks + 100 yellow intermediate dots

pip install opencv-python mediapipe numpy scikit-learn- 🏷️ **Finger Labels** - Each fingertip labeled (Thumb, Index, Middle, Ring, Pinky)

```- 📊 **Finger Status Panel** - Real-time UP/DOWN detection for each finger

- 🟢 **Hand Highlighting** - Green bounding box around detected hand

3. **Run the application**- 💡 **Training Hints** - Expected finger counts for A, V, W

```bash

python3 src/asl_translator.py#### Performance

```- ⚡ **Optimized FPS** - 40-50 FPS (2x improvement)

- 👍 **Improved Thumb Detection** - Angle-based algorithm (90% accuracy)

## 🎮 Controls- 🚀 **Lite MediaPipe Model** - Faster processing without accuracy loss

- 📹 **Optimized Resolution** - 960x540 for smooth performance

### Core Controls

| Key | Action |#### Additional Features

|-----|--------|- 🎓 **Practice Mode** - Interactive learning

| **SPACE** | Add space to text |- 📹 **Video Recording** - Save signing sessions

| **BACKSPACE** | Delete last character |- 🔊 **Voice Output** - Text-to-speech

| **C** | Clear all text |- 📝 **Custom Dictionary** - Save frequent words

| **H** | Show/hide help guide |- 📊 **Performance Analytics** - Track accuracy

| **S** | Show/hide statistics |

---

### Training Controls

| Key | Action |## 📁 Project Structure

|-----|--------|

| **T** | Enter/exit TRAINING MODE |```

| **A-Z** | Select letter to train (in training mode) |asl-translator/

| **ENTER** | Capture training sample |├── main.py                 # Main entry point

| **M** | Train ML model (standard) |├── requirements.txt        # Dependencies

| **B** | BULK TRAIN (removes outliers) |├── training_data.json      # Training samples (JSON)

| **N** | Show ML statistics |├── asl_model.pkl          # Trained model (generated)

| **D** | Toggle DEBUG mode |├── asl_model_scaler.pkl   # ML scaler (generated)

│

### Exit├── src/                   # Source code

| Key | Action |│   ├── asl_translator.py # Main application

|-----|--------|│   ├── hand_detector.py  # Hand tracking & visualization

| **ESC** | Save and quit |│   └── ml_trainer.py     # ML training & prediction

| **Q** | Quit without saving |│

├── docs/                  # Documentation

## 📚 Training Guide│   ├── MODEL_STATUS.md   # Training status & guide

│   ├── EASY_TRAINING.md  # Quick training guide

### Step 1: Enter Training Mode│   ├── TRAINING_GUIDE.md # Comprehensive training

```│   ├── ENHANCED_VISUALS.md # Visual features

Press T → See "🎓 LEARNING MODE ACTIVATED"│   ├── PERFORMANCE_OPTIMIZATIONS.md # Performance details

```│   └── ... (more guides)

│

### Step 2: Train Letters├── scripts/               # Utility scripts

```│   ├── diagnose_training.py # Analyze training data

1. Press a letter key (e.g., V)│   ├── QUICK_START_TRAINING.py # Training walkthrough

2. Make the ASL sign│   └── TEST_OPTIMIZATIONS.py # Test improvements

3. Hold hand steady│

4. Press ENTER to capture (repeat 15-20 times)├── training_photos/       # Training photos (auto-generated)

5. Vary angle/position slightly for each sample│   ├── A/                # Letter A photos

```│   ├── V/                # Letter V photos

│   └── W/                # Letter W photos

### Step 3: Train Model│

```├── recordings/            # Video recordings (optional)

Press M → Wait for training to complete└── documentation/         # Additional docs

``````



### Step 4: Test Recognition---

```

Press T to exit training mode## 🔧 Installation

Show gestures → Watch for real-time detection

```### Prerequisites



## 🧠 How It Works- Python 3.9 or higher

- Webcam

### Multi-Layer Intelligence- macOS, Linux, or Windows



#### Layer 1: Finger State Detection### Setup Steps

- Detects which fingers are UP or DOWN

- Uses 4-method voting for thumb detection1. **Clone the repository**

- Accurate finger counting for V vs W distinction```bash

git clone https://github.com/Hamdan772/asl-translator.git

#### Layer 2: Neural Network (396 Features)cd asl-translator

``````

63 Landmark Features    (21 points × 3 coordinates)

+  5 Finger States      (binary UP/DOWN for each finger)2. **Create virtual environment** (recommended)

+  4 Geometric Features (finger spacing, distances, ratios)```bash

+ 324 HOG Image Features (visual hand shape analysis)python3 -m venv .venv

────────────────────────source .venv/bin/activate  # On Windows: .venv\Scripts\activate

= 396 Total Features```

```

3. **Install dependencies**

**Architecture**: 4-layer deep network (256→128→64→32 neurons)```bash

pip install -r requirements.txt

#### Layer 3: Rule-Based Correction```

- Validates finger count matches expected pattern

- Auto-corrects V↔W confusion based on actual finger count4. **Run the application**

- Shows correction messages for transparency```bash

python3 main.py

#### Layer 4: Confidence Scoring```

- Reduces confidence if top 2 predictions are close

- Boosts confidence for stable hand---

- Only accepts predictions above 70% threshold

## 🚀 Quick Start

## 📁 Project Structure

### First Time Setup

```

asl-translator/1. **Start the application**

├── src/```bash

│   ├── asl_translator.py      # Main applicationpython3 main.py

│   ├── hand_detector.py       # Hand tracking & finger detection```

│   ├── ml_trainer.py          # ML model training & prediction

│   └── finger_matcher.py      # Advanced pattern matching2. **Enter Training Mode**

├── training_photos/           # Captured hand images (auto-created)   - Press `T` to activate training mode

├── training_data.json         # Training samples (auto-created)   - You'll see the FINGER STATUS panel on the left

├── TRAINING_GUIDE.md         # Detailed training instructions

└── README.md                 # This file3. **Train Letter A** (closed fist)

```   - Press `A`

   - Make a tight fist, thumb to the side

## 📈 Model Status   - Verify FINGER STATUS shows: **Count: 0** (all fingers DOWN)

   - Press `ENTER` 20 times (slight variations each time)

### ⚠️ UNTRAINED MODEL   - Photos automatically saved to `training_photos/A/`



This repository contains the complete recognition system but **NO TRAINED MODEL**.4. **Train Letter V** (peace sign ✌️)

   - Press `V`

You must train your own model:   - Spread index + middle fingers WIDE

1. Run the application   - Verify FINGER STATUS shows: **Count: 2** (index + middle UP)

2. Enter training mode (press **T**)   - Press `ENTER` 20 times

3. Train at least 3-5 letters with 15-20 samples each   - Photos automatically saved to `training_photos/V/`

4. Press **M** to train the model

5. Test recognition!5. **Train Letter W** (three fingers)

   - Press `W`

### 🔜 Coming Soon   - Spread index + middle + ring fingers WIDE

Pre-trained model for common ASL letters (A-Z)   - Verify FINGER STATUS shows: **Count: 3**

   - Press `ENTER` 20 times

## 🎯 Tips for Best Accuracy   - Photos automatically saved to `training_photos/W/`



1. **Lighting**: Use good, even lighting6. **Bulk Train the Model**

2. **Background**: Plain background reduces noise   - Press `B` to train with outlier removal

3. **Distance**: Keep hand at consistent distance   - Wait for training to complete (~10 seconds)

4. **Stability**: Hold hand still when capturing   - Check terminal for accuracy percentage

5. **Variation**: Train with different angles/positions

6. **Quantity**: More samples = better accuracy (15-20 minimum)7. **Test Your Model**

   - Press `ESC` to exit training mode

## 🐛 Troubleshooting   - Make A, V, or W gestures

   - Watch terminal for predictions: `🔍 Predictions: ✅A:89% V:8% W:3%`

See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for detailed troubleshooting steps.

---

Quick fixes:

- **Photos not saving?** Enable debug mode (press **D**)## 📸 Training Photo Capture

- **V and W confused?** Train 20+ samples each with clear finger separation

- **Low confidence?** Hold hand more stable, ensure good lighting### Automatic Photo Saving

- **Camera issues?** Close other apps using camera, check permissions

When you press `ENTER` during training, **TWO photos** are automatically saved:

## 🤝 Contributing

1. **With Dots** (`A_001_20241024_123456_dots.jpg`)

Contributions are welcome! Please feel free to submit a Pull Request.   - Shows all 121 tracking dots

   - Green landmarks + yellow intermediate dots

## 📝 License   - Finger labels visible

   - Useful for debugging hand tracking

This project is licensed under the MIT License.

2. **Clean Version** (`A_001_20241024_123456_clean.jpg`)

## 🙏 Acknowledgments   - Original camera frame without any overlays

   - Pure hand gesture

- **MediaPipe** - Google's hand tracking solution   - Useful for documentation or analysis

- **OpenCV** - Computer vision library

- **scikit-learn** - Machine learning toolkit### Photo Organization



## 📧 Contact```

training_photos/

**Hamdan** - [@Hamdan772](https://github.com/Hamdan772)├── A/

│   ├── A_001_20241024_123456_dots.jpg

Project Link: [https://github.com/Hamdan772/asl-translator](https://github.com/Hamdan772/asl-translator)│   ├── A_001_20241024_123456_clean.jpg

│   ├── A_002_20241024_123501_dots.jpg

---│   └── A_002_20241024_123501_clean.jpg

├── V/

⭐ **Star this repo** if you find it helpful!│   ├── V_001_20241024_123530_dots.jpg

│   └── V_001_20241024_123530_clean.jpg
└── W/
    ├── W_001_20241024_123600_dots.jpg
    └── W_001_20241024_123600_clean.jpg
```

---

## 🎮 Controls

### Main Controls
- `T` - Enter/exit training mode
- `M` - Train ML model (basic)
- `B` - Bulk train with outlier removal (recommended)
- `N` - Show ML statistics
- `SPACE` - Add space to text
- `BACKSPACE` - Delete last character
- `C` - Clear all text
- `ESC` - Save and quit
- `Q` - Quit without saving

### Training Mode
- `A-Z` - Select letter to train
- `ENTER` - Capture current gesture (saves photos automatically)
- `ESC` - Exit training mode

### Advanced Features
- `H` - Show/hide help guide
- `S` - Show/hide statistics
- `4` - Toggle practice mode
- `5` - Start/stop recording
- `6` - Toggle voice output
- `7` - Add word to dictionary
- `1-3` - Accept word suggestions

---

## 📊 Visual Features Explained

### FINGER STATUS Panel

During training mode, you'll see this panel on the left:

```
┌─────────────────────────┐
│   FINGER STATUS         │
├─────────────────────────┤
│ Thumb:  DOWN  👇        │  ← Gray = curled
│ Index:  UP    👆        │  ← Green = extended
│ Middle: UP    👆        │
│ Ring:   DOWN  👇        │
│ Pinky:  DOWN  👇        │
│                         │
│ Count: 2                │  ← Total fingers UP
└─────────────────────────┘
```

**Use this to verify hand positions BEFORE capturing!**

### 121 Tracking Dots

- **21 Green Dots** (5px) - Main hand landmarks
- **100 Yellow Dots** (3px) - Intermediate tracking points
- **Cyan Lines** (3px) - Connections between landmarks
- **Purple Labels** - Finger names on fingertips

### Hand Highlighting

- **Green Box** - Auto-detected hand region
- **Semi-transparent overlay** - Better dot visibility

---

## 🎯 Training Guide

### Best Practices

1. **Good Lighting** - Face a light source
2. **Clear Background** - Easier hand detection
3. **Hand Stability** - Wait for "STABLE" indicator
4. **Variety** - Slightly rotate hand between captures (±10°)
5. **Verification** - Check FINGER STATUS before pressing ENTER
6. **Quantity** - 20+ samples per letter recommended

### Common Mistakes to Avoid

❌ **Letter A**: Fingers partially up (should be 0)  
❌ **Letter V**: Only 1 finger or ring finger up (should be 2: index + middle)  
❌ **Letter W**: All 4 fingers up (should be 3: index + middle + ring)  
❌ **Capturing while "MOVING"** (wait for "STABLE")  
❌ **Fingers close together** (SPREAD them wide for V and W)

### Using Diagnostic Tools

**Analyze your training data:**
```bash
python3 scripts/diagnose_training.py
```

This will show:
- Finger extension statistics per letter
- Problematic samples
- Recommendations for improvement

---

## 📚 Documentation

### Comprehensive Guides

- **[EASY_TRAINING.md](docs/EASY_TRAINING.md)** - Quick start training guide
- **[TRAINING_GUIDE.md](docs/TRAINING_GUIDE.md)** - Detailed training instructions
- **[ENHANCED_VISUALS.md](docs/ENHANCED_VISUALS.md)** - Visual features documentation
- **[PERFORMANCE_OPTIMIZATIONS.md](docs/PERFORMANCE_OPTIMIZATIONS.md)** - Performance details
- **[TRAINING_TIPS_AVW.md](docs/TRAINING_TIPS_AVW.md)** - A/V/W specific tips
- **[VISUAL_GUIDE_AVW.md](docs/VISUAL_GUIDE_AVW.md)** - ASCII art hand positions

### Utility Scripts

- **[diagnose_training.py](scripts/diagnose_training.py)** - Analyze training data quality
- **[QUICK_START_TRAINING.py](scripts/QUICK_START_TRAINING.py)** - Interactive training guide
- **[TEST_OPTIMIZATIONS.py](scripts/TEST_OPTIMIZATIONS.py)** - Test performance improvements

---

## 🔧 Technical Details

### ML Architecture

- **Model**: Multi-layer Perceptron (MLP)
- **Layers**: 128 → 64 → 32 neurons
- **Activation**: ReLU
- **Solver**: Adam optimizer
- **Features**: 63 (21 landmarks × 3 coordinates)
- **Normalization**: StandardScaler

### Performance Metrics

| Metric | Value |
|--------|-------|
| FPS | 40-50 |
| Processing Time | ~25ms per frame |
| Thumb Accuracy | ~90% |
| Resolution | 960×540 (optimized) |
| Model Complexity | Lite (MediaPipe) |

### Dependencies

- **OpenCV** 4.8+ - Video processing
- **MediaPipe** 0.10.8 - Hand tracking (21 landmarks)
- **scikit-learn** 1.3+ - ML classifier
- **NumPy** 1.26+ - Numerical operations

---

## 🐛 Troubleshooting

### Low FPS (<30)
- Close other applications
- Improve lighting (camera works harder in dim light)
- Ensure GPU acceleration is available

### Thumb Detection Issues
- Make exaggerated thumb movements
- Ensure good lighting on hand
- Keep hand centered in green box

### Model Always Predicts Same Letter
- Check training data distribution: `python3 scripts/diagnose_training.py`
- Verify finger positions using FINGER STATUS panel
- Delete `training_data.json` and retrain carefully
- View saved photos in `training_photos/` to verify hand positions

### Photos Not Saving
- Check disk space
- Ensure write permissions in project directory
- Check terminal for error messages

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe** team for the hand tracking solution
- **OpenCV** community for computer vision tools
- **scikit-learn** for machine learning algorithms

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Open an issue on GitHub
- 📚 Check the [docs/](docs/) folder for guides
- 🔧 Run diagnostic scripts in [scripts/](scripts/) folder

---

<div align="center">

**Made with ❤️ for the ASL community**

⭐ Star this repo if you find it useful!

</div>
