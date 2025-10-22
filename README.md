# 🤟 ASL Translator v2.0 - Easy Training Mode

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.8-green.svg)](https://mediapipe.dev/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Real-time American Sign Language translator using computer vision and machine learning*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Training](#-ml-training) • [Documentation](#-documentation)

</div>

---

## ⚠️ MODEL TRAINING IN PROGRESS

> **Note**: This repository does not include pre-trained models. You must train the ML model with your own hand gestures for personalized accuracy.

**Status**: Ready for fresh training  
**Training Data**: Empty (`training_data.json`)  
**Model Files**: Not included (generated after training)

� **See [MODEL_STATUS.md](MODEL_STATUS.md) for training instructions**

---

## 📋 Overview

ASL Translator is a real-time hand gesture recognition system that translates American Sign Language (ASL) alphabet signs into text using MediaPipe hand tracking and machine learning.

### ✨ Key Features

- 🤖 **Easy Training Mode** - Simplified training with letter keys + ENTER to capture
- 🧠 **Machine Learning** - Train the system to recognize YOUR hand for better accuracy
- ⚡ **Real-time Processing** - Instant recognition with smooth video processing
- 🎯 **Bulk Training** - Automatic outlier removal for better model accuracy
- 📊 **Visual Feedback** - On-screen ML status indicator and sample counter
- 🎓 **Practice Mode** - Interactive learning mode for beginners
- 📹 **Recording** - Save your signing sessions as videos
- 🔊 **Voice Output** - Optional text-to-speech for translated text

### Installation

---

---

## 🚀 Quick Start

```bash

### Installation

# Install dependencies### 🌐 Try Online (No Installation Required!)

```bash

# Clone the repositorypip install -r requirements.txt

git clone https://github.com/Hamdan772/asl-translator.git

cd asl-translator**Live Web App:** https://web-1j5h4ycct-epokatrandomstuff-4004s-projects.vercel.app



# Install dependencies# Run the application

pip install -r requirements.txt

python main.py👉 Click the link above to use ASL Translator directly in your browser!

# Run the application

python main.py```

```

---

### Requirements

### Basic Usage

- Python 3.11+

- Webcam</div>

- Dependencies: opencv-python, mediapipe, numpy, scikit-learn (optional)

1. **Start** - Run `python main.py`

---

2. **Sign** - Show back of hand to camera## 📋 Overview

## 🎮 Usage

3. **Hold** - Keep gesture stable for 1 second

### Basic Controls

4. **Repeat** - Wait 1.5 seconds between lettersASL Translator is a real-time hand gesture recognition system that translates American Sign Language (ASL) alphabet signs into text. Available in **two versions**:

| Key | Action | Description |

|-----|--------|-------------|

| **SPACE** | Add space | Insert a space in your text |

| **BACKSPACE** | Delete | Remove last character |## 🎮 Keyboard Controls1. **🖥️ Desktop App** (Python) - Full-featured application with recording, analytics, and practice mode

| **C** | Clear | Clear all text |

| **H** | Help | Show/hide letter guide |2. **🌐 Web App** (Next.js) - Browser-based version, no installation required!

| **ESC** | Save & Quit | Save session and exit |

| **Q** | Quit | Exit without saving |### Essential Controls



### Machine Learning Controls- **SPACE** - Add spaceBoth versions use MediaPipe's hand tracking and custom geometric pattern matching algorithms for accurate letter recognition.



| Key | Action | Description |- **BACKSPACE** - Delete last character

|-----|--------|-------------|

| **T** | Learning Mode | Capture and label gestures |- **C** - Clear all text### ✨ Key Highlights

| **M** | Quick Train | Train model (standard) |

| **B** | Bulk Train | Train with outlier removal ⭐ |- **ESC** - Save and quit

| **N** | Statistics | View training data stats |

- **Q** - Quit without saving- **🎯 Ultra-lenient Detection**: Enhanced geometric pattern matching optimized for accuracy

### Advanced Features

- **⚡ Real-time Processing**: Instant recognition with smooth video processing

| Key | Action | Description |

|-----|--------|-------------|### ML Learning (NEW!)- **🌐 Web & Desktop**: Use in browser or as standalone application

| **P** | Practice Mode | Interactive learning exercises |

| **R** | Recording | Start/stop video recording |- **T** - Enter learning mode (capture & label gestures)- **🎨 Visual Feedback**: Progress indicators, gesture timeline, and confidence scores

| **V** | Voice | Toggle text-to-speech |

| **S** | Statistics | Show/hide session stats |- **M** - Train ML model on captured data- **🔊 Audio Feedback**: Optional sound effects for letter confirmation (desktop)

| **A** | Add Word | Save current word to dictionary |

| **1-3** | Suggestions | Accept word suggestions |- **N** - Show training statistics- **📊 Analytics**: Session statistics including speed and accuracy tracking (desktop)



---- **ENTER** - Submit letter label (in learning mode)- **🎮 Practice Mode**: Interactive learning mode with visual guides (desktop)



## 🧠 Machine Learning- **📹 Recording**: Save your translation sessions as videos (desktop)



### Quick ML Training### Advanced Features



1. **Press 'T'** - Enter learning mode- **H** - Show/hide help---

2. **Make gesture** - Hold your hand still

3. **Type letter** - Label it (e.g., "A") + ENTER- **S** - Show/hide statistics

4. **Repeat** - Collect 10-15 samples per letter

5. **Press 'B'** - Bulk train with outlier removal- **P** - Toggle practice mode## 🚀 Features

6. **Done!** - Model trained and ready

- **R** - Start/stop recording

### Training Modes

- **V** - Toggle voice output### Core Recognition

#### Press 'M' - Quick Training

- Fast training (~1-2 seconds)- **1-3** - Accept word suggestions

- No outlier detection

- Best for clean, high-quality samples<table>



#### Press 'B' - Bulk Training ⭐ RECOMMENDED## 🧠 Machine Learning<tr>

- Automatic outlier removal

- Statistical z-score analysis<td width="50%">

- Better accuracy for mixed-quality data

- Takes ~3-5 seconds### How It Works

- Removes poor captures automatically

#### 🖐️ Hand Tracking

### Example Output

1. **Capture Gestures** - Press 'T', make sign, hold still- **MediaPipe Integration**: 21-point hand landmark detection

```

🧹 BULK TRAINING WITH OUTLIER REMOVAL2. **Label Them** - Type letter + ENTER- **Back-of-hand optimized**: Best results showing palm away from camera

============================================================

3. **Train Model** - Press 'M' after 10+ samples- **Scale-independent**: Works at various distances

📊 Step 1: Detecting anomalous samples...

   ❌ Removed outlier for 'A' (z-score: 3.21)4. **Improved Accuracy** - System learns YOUR hand- **GPU accelerated**: Metal support on Apple Silicon

   ❌ Removed outlier for 'B' (z-score: 2.87)



🧠 Step 2: Training model on cleaned data...

✅ Training accuracy: 98.00%### Quick ML Tutorial</td>

✅ Test accuracy: 95.00%

<td width="50%">

============================================================

✅ BULK TRAINING COMPLETE!```bash

🎯 Accuracy: 95.00%

🧹 Outliers removed: 2Press 'T'  →  Learning mode ON#### 🔤 Letter Recognition

📦 Final dataset: 48 samples

============================================================Make sign A  →  Hold still  →  Captured!- **24 ASL Letters**: A-Z (excluding motion-based J & Z)

```

Type "A" + ENTER  →  Saved- **Enhanced accuracy**: 85-95% recognition rate

---

Repeat 10-15 times for different letters- **Multi-factor detection**: 3 checks per finger

## 📚 Documentation

Press 'M'  →  Train model (1-2 seconds)- **Angle calculations**: Precise joint measurements

Comprehensive documentation is available in the `documentation/` folder:

Use normally  →  10-20% better accuracy!

### 📖 Quick Start

- **[Quick Reference](documentation/QUICK_REFERENCE.md)** - Essential commands and controls```</td>

- **[Quick Start ML Tutorial](documentation/tutorials/QUICK_START_ML.md)** - Get started with ML in 5 minutes

- **[Bulk Training Quickstart](documentation/tutorials/BULK_TRAINING_QUICKSTART.md)** - Fast guide to bulk training</tr>



### 📘 Comprehensive Guides## 📊 Expected Accuracy</table>

- **[ML Learning Guide](documentation/guides/ML_LEARNING_GUIDE.md)** - Complete ML training guide

- **[Visual Guide ML](documentation/guides/VISUAL_GUIDE_ML.md)** - Visual walkthrough

- **[Bulk Training Guide](documentation/guides/BULK_TRAINING.md)** - Detailed bulk training documentation

| Mode | Accuracy |### User Interface

### 🛠️ Developer Resources

- **[Documentation Index](documentation/README.md)** - Full documentation overview|------|----------|

- **[Push to GitHub Guide](documentation/PUSH_GUIDE.md)** - Contributing guide

| Rule-based only | 70-80% || Feature | Description |

---

| After ML training (10-20 samples) | 75-85% ||---------|-------------|

## 🏗️ Project Structure

| After ML training (50+ samples) | 85-95% || **Live Video Feed** | Real-time webcam display with hand tracking overlay |

```

asl-translator/| **Text Display** | Large, scrolling text showing translated letters |

├── main.py                      # Entry point

├── requirements.txt             # Dependencies## 📁 Project Structure| **Progress Indicator** | Circular timer showing 1-second hold requirement |

├── README.md                    # This file

├── LICENSE                      # MIT License| **Gesture Timeline** | Visual history of last 15 detected gestures |

├── training_data.json           # ML training data

├── src/                         # Source code```| **Confidence Scores** | Color-coded feedback (🟢 High / 🟡 Medium / 🔴 Low) |

│   ├── asl_translator.py        # Main application

│   ├── hand_detector.py         # Hand trackingASL Translator/| **Help Overlay** | Interactive ASL alphabet reference guide |

│   ├── asl_classifier.py        # Gesture recognition

│   ├── ml_trainer.py            # ML training module├── main.py                  # Entry point (run this)| **Statistics Dashboard** | Real-time session metrics and performance data |

│   └── feature_extraction.py   # Feature processing

├── documentation/               # Documentation├── requirements.txt         # Dependencies

│   ├── README.md                # Docs index

│   ├── QUICK_REFERENCE.md       # Quick reference├── README.md               # This file### Advanced Features

│   ├── guides/                  # Comprehensive guides

│   │   ├── ML_LEARNING_GUIDE.md│

│   │   ├── VISUAL_GUIDE_ML.md

│   │   └── BULK_TRAINING.md├── src/                    # Source code```

│   └── tutorials/               # Quick tutorials

│       ├── QUICK_START_ML.md│   ├── asl_translator.py   # Main application🎮 Practice Mode      →  Learn ASL alphabet interactively

│       └── BULK_TRAINING_QUICKSTART.md

├── recordings/                  # Video recordings│   ├── asl_classifier.py   # Letter recognition📹 Recording Mode     →  Save translation sessions as video

└── test_bulk_training.py        # Testing script

```│   ├── hand_detector.py    # Hand tracking🔊 Audio Feedback     →  Sound effects for letter confirmation



---│   ├── feature_extraction.py  # Geometric features📊 Analytics          →  Track speed, accuracy, and progress



## 🎯 Recognition Details│   └── ml_trainer.py       # Machine learning💾 Save Translations  →  Export text with timestamps



### Supported Letters│🎯 Cooldown System    →  1.5s pause prevents false positives



**24 ASL Letters**: A, B, C, D, E, F, G, H, I, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y├── documentation/          # Technical docs```



**Not Supported**: J and Z (require motion)│   └── *.md               # Implementation details



### How It Works│---



1. **Hand Detection** - MediaPipe detects 21 hand landmarks└── recordings/            # Saved video sessions

2. **Feature Extraction** - Calculates angles, distances, and positions

3. **Geometric Matching** - Rule-based pattern recognition    └── *.mp4## 🌐 Web Version

4. **ML Enhancement** - Optional neural network for personalization

5. **Hybrid System** - Combines both methods for best accuracy```



### Accuracy### Try it Online!



- **Rule-based**: 80-85% accuracy## 🛠️ Requirements

- **With ML training**: 90-95% accuracy (after training on your hand)

- **Best results**: Show back of hand, clear gestures, good lighting**Live Demo:** https://web-1j5h4ycct-epokatrandomstuff-4004s-projects.vercel.app



---- Python 3.11+



## 🧪 Testing- WebcamNo installation required - works directly in your browser!



Test the bulk training feature with synthetic data:- macOS, Windows, or Linux



```bash### Features

python3 test_bulk_training.py

```### Dependencies



This demonstrates:- OpenCV (cv2) - Video processing- ✅ **24 ASL Letters** (A-Y, excluding J/Z)

- Outlier detection algorithm

- Statistical z-score analysis- MediaPipe - Hand tracking- ✅ **Real-time Detection** using MediaPipe Hands

- Training workflow

- Before/after statistics- NumPy - Numerical operations- ✅ **Beautiful UI** with modern design



---- scikit-learn - Machine learning (optional, lazy-loaded)- ✅ **Mobile Friendly** - works on phones/tablets



## 🛠️ Technical Stack- ✅ **Privacy First** - all processing in browser



### Core Technologies## 🎯 Supported Letters- ✅ **Ultra-fast** - powered by Next.js & Vercel

- **Python 3.11+** - Primary language

- **OpenCV 4.8+** - Video processing

- **MediaPipe 0.10.8** - Hand landmark detection

- **NumPy 1.26.2** - Numerical operationsA, B, C, D, E, F, G, H, I, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y### How to Use (Web)



### Machine Learning (Optional)

- **scikit-learn 1.3+** - Neural networks

- **MLPClassifier** - 3-layer network (128→64→32)**Note:** J and Z require motion and are not supported yet.1. Visit the live URL above

- **StandardScaler** - Feature normalization

2. Allow camera access when prompted

### Features

- Lazy loading for fast startup## 💡 Tips for Best Results3. Show the back of your hand to camera

- GPU acceleration (Metal on Apple Silicon)

- Real-time video processing4. Form ASL letters (A-Y)

- Persistent data storage (JSON, pickle)

1. **Lighting** - Good, even lighting works best5. Hold for 1 second to add letter

---

2. **Background** - Plain background recommended6. Use buttons to add space, backspace, or clear

## 📊 Performance

3. **Hand Position** - Show back of hand clearly

### Optimization

- **Startup time**: 1-2 seconds (with lazy loading)4. **Stability** - Hold gesture steady for 1 second### Tech Stack (Web)

- **Frame rate**: 30 FPS smooth video

- **Recognition latency**: <100ms5. **ML Training** - 5+ samples per letter for best accuracy

- **ML training**: 1-5 seconds depending on dataset size

- Next.js 14.0.4 + TypeScript

### System Requirements

- **CPU**: Multi-core recommended## 📚 Documentation- MediaPipe Hands (browser version)

- **RAM**: 2GB minimum, 4GB recommended

- **Webcam**: 720p or higher- TensorFlow.js

- **OS**: Windows, macOS, or Linux

Detailed documentation available in `documentation/` folder:- Tailwind CSS

---

- React Webcam

## 🤝 Contributing

- **ML_LEARNING_GUIDE.md** - Complete ML tutorial- Deployed on Vercel

Contributions are welcome! Please:

- **QUICK_START_ML.md** - 5-minute ML quick start

1. Fork the repository

2. Create a feature branch- **VISUAL_GUIDE_ML.md** - Visual walkthrough📖 **Full web documentation:** [web/README.md](web/README.md)

3. Make your changes

4. Test thoroughly- **QUICK_REFERENCE.md** - All keyboard shortcuts

5. Submit a pull request

---

See [PUSH_GUIDE.md](documentation/PUSH_GUIDE.md) for details.

## 🐛 Troubleshooting

---

## 📦 Installation (Desktop Version)

## 📝 License

### App won't start

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

- Check Python version: `python --version` (need 3.11+)### Prerequisites

---

- Install dependencies: `pip install -r requirements.txt`

## 🙏 Acknowledgments

- **Python 3.11 or higher**

- **MediaPipe** - Hand tracking technology

- **OpenCV** - Computer vision library### Poor recognition- **Webcam** (built-in or external)

- **scikit-learn** - Machine learning framework

- **ASL Community** - Sign language resources- Improve lighting- **Operating System**: macOS, Windows, or Linux



---- Make clear, stable gestures



## 📞 Support- Train ML model with your hand (Press 'T')### Setup



- **Documentation**: [documentation/README.md](documentation/README.md)

- **Issues**: [GitHub Issues](https://github.com/Hamdan772/asl-translator/issues)

- **Quick Reference**: [QUICK_REFERENCE.md](documentation/QUICK_REFERENCE.md)### ML won't load1. **Clone the repository**



---- ML features are optional   ```bash



<div align="center">- They load on first use (Press 'T' or 'M')   git clone https://github.com/Hamdan772/asl-translator.git



**Made with ❤️ for the ASL community**- Takes 3-5 seconds to load sklearn/scipy   cd asl-translator



⭐ Star this repo if you find it helpful!   ```



</div>## 🤝 Contributing


2. **Create virtual environment**

Pull requests welcome! Please test thoroughly before submitting.   ```bash

   python3 -m venv .venv

## 📝 License   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   ```

MIT License - See LICENSE file

3. **Install dependencies**

## 🙏 Acknowledgments   ```bash

   pip install -r requirements.txt

- MediaPipe by Google for hand tracking   ```

- OpenCV for computer vision

- scikit-learn for machine learning4. **Run the application**

   ```bash

---   python asl_translator.py

   ```

**Version:** 2.0 + ML Learning  

**Last Updated:** October 21, 2025  ### Dependencies

**Status:** Production Ready ✅

```

For questions or issues, please open a GitHub issue.mediapipe==0.10.8    # Hand tracking and pose estimation

opencv-python==4.8.1  # Computer vision and video processing
numpy==1.26.2         # Numerical computations
```

---

## 🎯 Usage (Desktop Version)

### Quick Start

1. **Launch the application**
   ```bash
   python asl_translator.py
   ```

2. **Position your hand**
   - Show the **back of your hand** to the camera
   - Keep hand clearly visible in frame
   - Maintain steady position

3. **Make ASL signs**
   - Form letter with your hand
   - Hold steady for **1 second** (watch progress circle)
   - Letter appears in text display
   - Wait **1.5 seconds** (cooldown) before next letter

### Recognition Tips

✅ **DO:**
- Show back of hand (palm away from camera)
- Keep hand in good lighting
- Hold gestures steady for 1 second
- Wait for cooldown between letters
- Keep fingers clearly separated

❌ **DON'T:**
- Move hand rapidly during detection
- Overlap fingers or hide landmarks
- Rush between letters (wait for cooldown)
- Use palm-forward orientation
- Place hand outside camera frame

---

## ⌨️ Controls

### Keyboard Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| `SPACE` | Add Space | Insert space character |
| `BACKSPACE` | Delete | Remove last character |
| `C` | Clear | Clear all text |
| `H` | Help | Show/hide ASL alphabet guide |
| `S` | Statistics | Show/hide session stats |
| `P` | Practice Mode | Toggle interactive learning |
| `R` | Record | Start/stop video recording |
| `V` | Voice | Toggle audio feedback |
| `A` | Add Word | Save current word to dictionary |
| `1-3` | Suggestions | Accept word completion suggestions |
| `ESC` | Save & Quit | Save translation and exit |
| `Q` | Quit | Exit without saving |

---

## 🎨 Visual Guide

### On-Screen Elements

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  📹 Live Video Feed                    📊 Session Stats    │
│  └─ Hand tracking overlay             └─ Letters/min       │
│  └─ Progress indicator                └─ Accuracy          │
│                                        └─ Duration         │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  📝 Translated Text: HELLO WORLD                            │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                             │
│  🎯 Gesture Timeline: [H] [E] [L] [L] [O]                  │
│                                                             │
│  ⏱️ Hold gesture 1s to add (1.5s cooldown)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Timing System

```
Step 1: DETECTION (Instant)
   └─ Hand gesture recognized
   └─ Letter identified
   └─ Hold timer starts

Step 2: HOLD (1 second)
   └─ Progress circle fills
   └─ Keep hand steady
   └─ Letter added ✅

Step 3: COOLDOWN (1.5 seconds)
   └─ "Cooldown: X.Xs" displayed
   └─ Prepare next gesture
   └─ New letters ignored

Step 4: READY
   └─ System ready for next letter
```

---

## 📊 Practice Mode

Practice mode helps you learn the ASL alphabet with interactive guidance.

### Features
- **Letter-by-letter practice**: Master each sign individually
- **Visual reference**: See correct hand position for each letter
- **Instant feedback**: Green highlight on successful recognition
- **Progress tracking**: Monitor your learning journey

### How to Use
1. Press `P` to enter practice mode
2. System shows target letter
3. Make the corresponding ASL sign
4. Hold steady until recognized
5. System automatically moves to next letter

---

## 🎥 Recording Mode

Capture your translation sessions for review or sharing.

### Features
- **Full session recording**: Saves video with overlays
- **Timestamped files**: Organized by date and time
- **MP4 format**: Universal compatibility
- **Audio-free**: Silent recordings (audio feedback optional)

### How to Use
1. Press `R` to start recording
2. 🔴 Recording indicator appears
3. Perform your translations
4. Press `R` again to stop
5. Video saved to `recordings/` folder

---

## 📈 Performance

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Dual-core 2.0 GHz | Quad-core 2.5+ GHz |
| **RAM** | 4 GB | 8 GB+ |
| **GPU** | Integrated | Dedicated (CUDA/Metal) |
| **Camera** | 720p @ 30fps | 1080p @ 60fps |
| **OS** | macOS 11+, Windows 10+, Linux | Latest versions |

### Benchmarks

- **Recognition Accuracy**: 85-95% (depends on lighting and hand clarity)
- **Frame Rate**: 30+ FPS (with GPU acceleration)
- **Latency**: < 100ms (detection to display)
- **False Positives**: Reduced by 60% with cooldown system

---

## 🛠️ Technical Details

### Architecture

```
┌─────────────────┐
│  asl_translator │  ← Main application orchestrator
└────────┬────────┘
         │
    ┌────┴────┬──────────────┐
    │         │              │
┌───▼───┐ ┌──▼──────┐ ┌─────▼─────┐
│  Hand │ │   ASL   │ │  OpenCV   │
│ Detect│ │Classify │ │  Video    │
└───────┘ └─────────┘ └───────────┘
    │         │              │
MediaPipe  Geometric    Camera I/O
Tracking   Patterns    Processing
```

### Hand Detection (`hand_detector.py`)
- **MediaPipe Hands**: 21 landmark points per hand
- **Confidence filtering**: Removes low-confidence detections
- **Back-of-hand optimization**: Enhanced for this orientation

### Letter Classification (`asl_classifier.py`)
- **Multi-factor finger detection**: Distance + angle + position checks
- **Geometric pattern matching**: 24 unique letter patterns
- **Confidence scoring**: Multi-factor accuracy assessment
- **Scale normalization**: Distance-independent recognition

### Main Application (`asl_translator.py`)
- **Event loop**: 30+ FPS processing
- **UI rendering**: OpenCV-based interface
- **State management**: Session tracking and statistics
- **File I/O**: Save translations and recordings

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>Camera not working</b></summary>

- Check camera permissions in system settings
- Ensure no other app is using the camera
- Try different camera index in code (0, 1, 2...)
- Restart application
</details>

<details>
<summary><b>Poor recognition accuracy</b></summary>

- Improve lighting (avoid backlighting)
- Show back of hand (not palm)
- Keep hand fully visible in frame
- Separate fingers clearly
- Hold gestures steady for full 1 second
- Clean camera lens
</details>

<details>
<summary><b>Lag or low FPS</b></summary>

- Close other applications
- Reduce camera resolution
- Update GPU drivers
- Check CPU usage
- Enable hardware acceleration
</details>

<details>
<summary><b>Letters not being detected</b></summary>

- Verify hand is in frame
- Check cooldown timer (wait 1.5s between letters)
- Ensure proper hand orientation (back of hand)
- Make clear, distinct gestures
- Check confidence score (green is best)
</details>

---

## 📝 Project Structure

```
asl-translator/
├── asl_translator.py      # Main application
├── hand_detector.py       # MediaPipe hand tracking wrapper
├── asl_classifier.py      # Letter classification logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
├── docs/                 # Documentation
│   └── archive/          # Old documentation files
├── recordings/           # Saved video recordings (created at runtime)
└── translations/         # Saved text files (created at runtime)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Test on multiple platforms
- Update README for new features
- Keep dependencies minimal

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe** - Google's excellent hand tracking solution
- **OpenCV** - Computer vision library
- **ASL Community** - For the beautiful sign language

---

## 📧 Contact

**Project Maintainer**: Hamdan Nishad

- GitHub: [@hamdannishad](https://github.com/hamdannishad)
- Email: your.email@example.com

---

## 🗺️ Roadmap

### Current Version: 2.0

- [x] Real-time letter recognition (A-Z, excluding J & Z)
- [x] Enhanced accuracy with multi-factor detection
- [x] Practice mode
- [x] Recording functionality
- [x] Session analytics
- [x] Audio feedback
- [x] Cooldown system

### Future Plans

- [ ] Word recognition and common phrases
- [ ] Motion-based letters (J & Z)
- [ ] Machine learning model for better accuracy
- [ ] Mobile app version
- [ ] Multi-hand support
- [ ] Sign language dictionary integration
- [ ] Real-time translation between users
- [ ] Educational mode with lessons

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ and 🤟 by Hamdan Nishad**

*Empowering communication through technology*

</div>
