# 🤟 ASL Translator v2.0 - Optimized Edition

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.8-green.svg)](https://mediapipe.dev/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Real-time American Sign Language translator with ML training, photo capture, and enhanced visual feedback*

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Training](#-training-guide) • [Documentation](#-documentation)

</div>

---

## 🚀 What's New (October 2024)

### ✨ Latest Features

- 📸 **Training Photo Capture** - Automatically saves photos (with/without dots) during training
- 🎨 **Enhanced Visuals** - 121 colorful tracking dots, finger labels, and hand highlighting
- 📊 **Finger Status Panel** - Real-time finger detection (UP/DOWN) during training
- ⚡ **Performance Optimized** - 2x faster FPS (40-50 FPS), improved thumb detection
- 🗂️ **Better Organization** - Structured file layout with docs/ and scripts/ folders

---

## ⚠️ MODEL TRAINING REQUIRED

> **Note**: This repository does not include pre-trained models. Train with your own gestures for personalized accuracy.

**Status**: Ready for training  
**Training Data**: Empty - Start fresh!  
**Photos**: Automatically saved to `training_photos/` during training

📚 **See [docs/MODEL_STATUS.md](docs/MODEL_STATUS.md) for detailed instructions**

---

## 📋 Overview

ASL Translator is a real-time hand gesture recognition system with advanced visual feedback, ML training capabilities, and automatic photo documentation of training sessions.

### ✨ Core Features

#### Training & ML
- 🤖 **Easy Training Mode** - Press letter keys + ENTER to capture samples
- 📸 **Auto Photo Capture** - Saves training photos with dots AND clean versions
- 🎯 **Bulk Training** - Automatic outlier removal (z-score method)
- 🧠 **ML Classifier** - Neural network (128→64→32 neurons)
- 📊 **Prediction Debug** - See top 3 predictions with confidence percentages

#### Visual Enhancements
- 🎨 **121 Tracking Dots** - 21 green landmarks + 100 yellow intermediate dots
- 🏷️ **Finger Labels** - Each fingertip labeled (Thumb, Index, Middle, Ring, Pinky)
- 📊 **Finger Status Panel** - Real-time UP/DOWN detection for each finger
- 🟢 **Hand Highlighting** - Green bounding box around detected hand
- 💡 **Training Hints** - Expected finger counts for A, V, W

#### Performance
- ⚡ **Optimized FPS** - 40-50 FPS (2x improvement)
- 👍 **Improved Thumb Detection** - Angle-based algorithm (90% accuracy)
- 🚀 **Lite MediaPipe Model** - Faster processing without accuracy loss
- 📹 **Optimized Resolution** - 960x540 for smooth performance

#### Additional Features
- 🎓 **Practice Mode** - Interactive learning
- 📹 **Video Recording** - Save signing sessions
- 🔊 **Voice Output** - Text-to-speech
- 📝 **Custom Dictionary** - Save frequent words
- 📊 **Performance Analytics** - Track accuracy

---

## 📁 Project Structure

```
asl-translator/
├── main.py                 # Main entry point
├── requirements.txt        # Dependencies
├── training_data.json      # Training samples (JSON)
├── asl_model.pkl          # Trained model (generated)
├── asl_model_scaler.pkl   # ML scaler (generated)
│
├── src/                   # Source code
│   ├── asl_translator.py # Main application
│   ├── hand_detector.py  # Hand tracking & visualization
│   └── ml_trainer.py     # ML training & prediction
│
├── docs/                  # Documentation
│   ├── MODEL_STATUS.md   # Training status & guide
│   ├── EASY_TRAINING.md  # Quick training guide
│   ├── TRAINING_GUIDE.md # Comprehensive training
│   ├── ENHANCED_VISUALS.md # Visual features
│   ├── PERFORMANCE_OPTIMIZATIONS.md # Performance details
│   └── ... (more guides)
│
├── scripts/               # Utility scripts
│   ├── diagnose_training.py # Analyze training data
│   ├── QUICK_START_TRAINING.py # Training walkthrough
│   └── TEST_OPTIMIZATIONS.py # Test improvements
│
├── training_photos/       # Training photos (auto-generated)
│   ├── A/                # Letter A photos
│   ├── V/                # Letter V photos
│   └── W/                # Letter W photos
│
├── recordings/            # Video recordings (optional)
└── documentation/         # Additional docs
```

---

## 🔧 Installation

### Prerequisites

- Python 3.9 or higher
- Webcam
- macOS, Linux, or Windows

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/Hamdan772/asl-translator.git
cd asl-translator
```

2. **Create virtual environment** (recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python3 main.py
```

---

## 🚀 Quick Start

### First Time Setup

1. **Start the application**
```bash
python3 main.py
```

2. **Enter Training Mode**
   - Press `T` to activate training mode
   - You'll see the FINGER STATUS panel on the left

3. **Train Letter A** (closed fist)
   - Press `A`
   - Make a tight fist, thumb to the side
   - Verify FINGER STATUS shows: **Count: 0** (all fingers DOWN)
   - Press `ENTER` 20 times (slight variations each time)
   - Photos automatically saved to `training_photos/A/`

4. **Train Letter V** (peace sign ✌️)
   - Press `V`
   - Spread index + middle fingers WIDE
   - Verify FINGER STATUS shows: **Count: 2** (index + middle UP)
   - Press `ENTER` 20 times
   - Photos automatically saved to `training_photos/V/`

5. **Train Letter W** (three fingers)
   - Press `W`
   - Spread index + middle + ring fingers WIDE
   - Verify FINGER STATUS shows: **Count: 3**
   - Press `ENTER` 20 times
   - Photos automatically saved to `training_photos/W/`

6. **Bulk Train the Model**
   - Press `B` to train with outlier removal
   - Wait for training to complete (~10 seconds)
   - Check terminal for accuracy percentage

7. **Test Your Model**
   - Press `ESC` to exit training mode
   - Make A, V, or W gestures
   - Watch terminal for predictions: `🔍 Predictions: ✅A:89% V:8% W:3%`

---

## 📸 Training Photo Capture

### Automatic Photo Saving

When you press `ENTER` during training, **TWO photos** are automatically saved:

1. **With Dots** (`A_001_20241024_123456_dots.jpg`)
   - Shows all 121 tracking dots
   - Green landmarks + yellow intermediate dots
   - Finger labels visible
   - Useful for debugging hand tracking

2. **Clean Version** (`A_001_20241024_123456_clean.jpg`)
   - Original camera frame without any overlays
   - Pure hand gesture
   - Useful for documentation or analysis

### Photo Organization

```
training_photos/
├── A/
│   ├── A_001_20241024_123456_dots.jpg
│   ├── A_001_20241024_123456_clean.jpg
│   ├── A_002_20241024_123501_dots.jpg
│   └── A_002_20241024_123501_clean.jpg
├── V/
│   ├── V_001_20241024_123530_dots.jpg
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
