# 🤟 ASL Translator - Advanced Real-Time Sign Language Recognition

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.8-green.svg)](https://mediapipe.dev/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Real-time American Sign Language translator with machine learning, photo capture, and multi-modal recognition*

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Keybinds](#-keybinds-reference) • [Training](#-training-guide) • [Documentation](#-documentation)

</div>

---

## ⚠️ MODEL TRAINING REQUIRED

> **Note**: This repository does not include pre-trained models. You must train your own model with your hand gestures for personalized accuracy.

**Status**: 🟢 Ready for training  
**Training Data**: Empty - Start fresh!  
**Photos**: Automatically saved to `training_photos/` during training

📚 **See [TRAINING_GUIDE.md](TRAINING_GUIDE.md) for detailed instructions**

---

## ✨ Features

### 🎯 Core Recognition System
- **Real-time hand tracking** with 21 landmark points (MediaPipe)
- **Multi-modal recognition** combining 4 intelligence layers:
  - 🖐️ **Finger state detection** - Detects which fingers are UP/DOWN
  - 🧠 **Neural network** - 396 features (landmarks + finger states + geometry + HOG)
  - 📏 **Geometric analysis** - Finger spacing, distances, and ratios
  - 📸 **Visual features** - HOG image analysis from photos
- **Rule-based corrections** - Auto-fixes V vs W confusion
- **Confidence scoring** - Ambiguity detection with stability bonus
- **Adaptive learning** - Train custom gestures

### 🎓 Training System
- **Interactive training mode** - Press T to enter, select letter, capture samples
- **Photo capture** - Automatically saves cropped hand images during training
- **Finger state recording** - Captures which fingers are extended
- **Geometric features** - Records finger positions and angles
- **Bulk training** - Removes outliers for better accuracy (Press B)
- **Debug mode** - Detailed logging for troubleshooting (Press D)

### 📊 Visual Features
- **121 visual markers** - 21 green landmarks + 100 yellow connections
- **Finger status panel** - Real-time UP/DOWN indicator for each finger
- **Confidence indicators** - Shows prediction certainty
- **Hand stability detection** - Green indicator when hand is stable
- **Session statistics** - Tracks letters, accuracy, speed

---

## 🚀 Installation

### Prerequisites

```bash
Python 3.9 or higher
Webcam/Camera
```

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Hamdan772/asl-translator.git
cd asl-translator
```

2. **Install dependencies**
```bash
pip install opencv-python mediapipe numpy scikit-learn
```

3. **Run the application**
```bash
python3 src/asl_translator.py
```

---

## 🎮 Keybinds Reference

### 📝 Core Controls (Always Active)

| Key | Action | Description |
|-----|--------|-------------|
| **SPACE** | Add space | Inserts a space character |
| **BACKSPACE** | Delete last character | Removes the most recent character |
| **C** | Clear all text | Wipes the entire translation buffer |
| **H** | Toggle help guide | Shows/hides the help overlay |
| **S** | Toggle statistics | Shows/hides session stats |
| **Q** | Quit without saving | Exits immediately |
| **ESC** | Save and quit | Saves text to file and exits |

### 🎓 Training Controls

| Key | Action | Description |
|-----|--------|-------------|
| **T** | Toggle training mode | Enters/exits learning mode |
| **A-Z** | Select letter to train | Choose which letter to capture (in training mode) |
| **ENTER** | Capture training sample | Saves current hand gesture with photo |
| **M** | Train ML model (standard) | Trains neural network with all samples |
| **B** | Bulk train (advanced) | Trains model after removing outlier samples |
| **N** | Show ML statistics | Displays training data distribution |
| **D** | Toggle debug mode | Enables/disables detailed logging |

### 🎯 Training Mode Workflow

```
1. Press T          → Enter training mode
2. Press V          → Select letter V
3. Make V gesture   → Hold hand steady
4. Press ENTER      → Capture sample (repeat 15-20 times)
5. Press W          → Switch to letter W
6. Make W gesture   → Capture 15-20 samples
7. Press M          → Train the model
8. Press T          → Exit training mode
9. Test gestures!   → Model recognizes V and W
```

### 💡 Quick Tips

- **Training Mode**: Stay in training mode when switching between letters (just press different letter keys)
- **Debug Mode**: Press D to see detailed photo capture logs
- **Stability**: Wait for green "stable" indicator before pressing ENTER
- **Variations**: Capture samples from different angles for better accuracy
- **Quantity**: 15-20 samples per letter recommended

---

## 📚 Training Guide

### Step 1: Enter Training Mode
```
Press T → See "🎓 LEARNING MODE ACTIVATED"
```

### Step 2: Train Your First Letter
```
1. Press V (for victory sign)
2. Make the V gesture with your hand
3. Hold steady until "stable" indicator appears
4. Press ENTER to capture
5. Repeat 15-20 times with slight variations
```

### Step 3: Train More Letters
```
1. Press W (without exiting training mode)
2. Make the W gesture
3. Press ENTER 15-20 times
4. Continue with other letters (A, B, C, etc.)
```

### Step 4: Train the Model
```
Press M → Wait for training completion
Watch for: "✅ Training accuracy: XX%"
```

### Step 5: Test Recognition
```
1. Press T to exit training mode
2. Show your trained gestures
3. Watch real-time detection!
```

### 📸 Photo Capture
During training, the system automatically:
- Captures cropped hand images
- Saves to `training_photos/[LETTER]/`
- Records finger states (which fingers are UP/DOWN)
- Stores geometric features (spacing, angles)

---

## 🧠 How It Works

### Multi-Layer Intelligence System

```
┌─────────────────────────────────────┐
│ Layer 1: Finger State Detection    │
│ • Detects which fingers are UP      │
│ • 4-method voting for thumb         │
│ • Angle + distance for others       │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ Layer 2: Neural Network (396)      │
│ • 63 landmark coordinates           │
│ • 5 finger state binaries           │
│ • 4 geometric measurements          │
│ • 324 HOG image features            │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ Layer 3: Rule-Based Correction     │
│ • Validates finger count            │
│ • Auto-corrects V ↔ W confusion    │
│ • Shows correction messages         │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ Layer 4: Confidence Scoring        │
│ • Ambiguity detection               │
│ • Stability bonus (+5%)             │
│ • Threshold: 70% minimum            │
└─────────────────────────────────────┘
```

### Neural Network Architecture
```
Input: 396 features
  ↓
Hidden Layer 1: 256 neurons (ReLU)
  ↓
Hidden Layer 2: 128 neurons (ReLU)
  ↓
Hidden Layer 3: 64 neurons (ReLU)
  ↓
Hidden Layer 4: 32 neurons (ReLU)
  ↓
Output: Softmax (A-Z classification)
```

---

## 📁 Project Structure

```
asl-translator/
├── src/
│   ├── asl_translator.py      # Main application (1466 lines)
│   ├── hand_detector.py       # Hand tracking & finger detection (623 lines)
│   ├── ml_trainer.py          # ML training & prediction (668 lines)
│   └── finger_matcher.py      # Advanced pattern matching (249 lines)
├── training_photos/           # Auto-saved hand images (created during training)
├── training_data.json         # Training samples with finger states
├── TRAINING_GUIDE.md         # Detailed training instructions
├── RELEASE_NOTES.md          # Release documentation
└── README.md                 # This file
```

---

## 🐛 Troubleshooting

### Photos Not Saving?
1. Enable debug mode (press **D**)
2. Check console for error messages
3. Verify camera permissions
4. Ensure `training_photos/` directory exists

### V and W Confused?
1. Train 20+ samples for each letter
2. Make clear finger separation
3. Check FINGER STATUS panel shows correct count
   - **V** = 2 fingers (Index + Middle)
   - **W** = 3 fingers (Index + Middle + Ring)

### Low Recognition Confidence?
1. Hold hand more stable
2. Improve lighting conditions
3. Keep hand centered in frame
4. Train more sample variations
5. Press **N** to check training statistics

### Camera Not Working?
1. Close other apps using the camera
2. Check system camera permissions
3. Restart the application
4. Try a different USB port (external webcam)

---

## 🎯 Tips for Best Accuracy

1. **Lighting**: Use bright, even lighting
2. **Background**: Plain background reduces noise
3. **Distance**: Keep hand at consistent distance from camera
4. **Stability**: Hold hand still when capturing (wait for green indicator)
5. **Variation**: Train samples from different angles and positions
6. **Quantity**: 15-20 samples minimum per letter
7. **Quality**: Make clear, distinct gestures
8. **Consistency**: Use same hand and orientation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Areas for Contribution
- Pre-trained model for A-Z letters
- Additional ASL signs and words
- Improved detection algorithms
- Dynamic gesture recognition (moving signs)
- Multi-hand support
- Performance optimizations
- Better UI/UX

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **MediaPipe** - Google's hand tracking solution
- **OpenCV** - Computer vision library  
- **scikit-learn** - Machine learning toolkit
- ASL community for gesture references

---

## 📧 Contact

**Hamdan** - [@Hamdan772](https://github.com/Hamdan772)

**Project Link**: [https://github.com/Hamdan772/asl-translator](https://github.com/Hamdan772/asl-translator)

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

### 🐛 Report bugs in the [Issues](https://github.com/Hamdan772/asl-translator/issues) section

### 💡 Suggest features via [Pull Requests](https://github.com/Hamdan772/asl-translator/pulls)

---

**Made with ❤️ for the ASL community**

</div>
