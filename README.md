<div align="center">

# 🤟 ASL Sign Language Recognition

### Real-time American Sign Language alphabet recognition powered by AI

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-00A67E?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.6-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<img src="docs/SLR.png" alt="ASL Recognition Demo" width="600">

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Training](#-training)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- **Real-time Recognition** — Instant ASL alphabet detection
- **Both Hands Support** — Works with left or right hand
- **High Accuracy** — 99.98% validation accuracy
- **24 Letters** — A-Y (excluding J & Z)

</td>
<td width="50%">

### 🚀 Advanced Features
- **🔊 Text-to-Speech** — Hold 3 sec to hear the letter
- **📷 Multi-Camera** — Switch cameras on the fly
- **📝 Data Logging** — Collect your own training data
- **⚡ TFLite Optimized** — Fast inference

</td>
</tr>
</table>

---

## 🎬 Demo

<div align="center">

| Prediction Mode | How It Works |
|:---:|:---:|
| <img src="docs/result.png" width="300"> | <img src="docs/hand-landmarks.png" width="300"> |
| *Real-time letter recognition* | *21 hand landmarks detected* |

</div>

### Supported Signs

The model recognizes **24 ASL alphabet letters**:

```
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ A │ B │ C │ D │ E │ F │ G │ H │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ I │ K │ L │ M │ N │ O │ P │ Q │
├───┼───┼───┼───┼───┼───┼───┼───┤
│ R │ S │ T │ U │ V │ W │ X │ Y │
└───┴───┴───┴───┴───┴───┴───┴───┘
```

> 💡 **Note:** J and Z require motion gestures and are not supported.

---

## 🛠 Installation

### Prerequisites

- 🐍 Python 3.8 or higher
- 📷 Webcam
- 💻 macOS / Windows / Linux

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Hamdan772/asl-translator.git
cd asl-translator

# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

---

## 🎮 Usage

### Launch the Application

```bash
python app.py
```

### ⌨️ Keyboard Controls

| Key | Action | Description |
|:---:|--------|-------------|
| <kbd>N</kbd> | **Prediction Mode** | Default mode - recognizes signs |
| <kbd>K</kbd> | **Logging Mode** | Record training data |
| <kbd>C</kbd> | **Switch Camera** | Cycle through available cameras |
| <kbd>0-9</kbd> | **Select Class** | Choose sign class (logging mode) |
| <kbd>ESC</kbd> | **Exit** | Close the application |

### 🔊 Text-to-Speech Feature

> **macOS users:** Hold any sign steady for **3 seconds** and hear it spoken aloud!

The app uses the native `say` command for natural speech synthesis.

---

## 🧠 How It Works

<div align="center">

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Camera    │ ──▶ │  MediaPipe  │ ──▶ │  TFLite     │ ──▶ │   Output    │
│   Input     │     │  21 Points  │     │   Model     │     │   Letter    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

</div>

1. **📷 Capture** — Webcam captures video frames
2. **✋ Detect** — MediaPipe extracts 21 hand landmarks (x, y coordinates)
3. **🔄 Process** — Landmarks are normalized and flattened to 42 features
4. **🤖 Classify** — TensorFlow Lite model predicts the letter
5. **🔊 Speak** — Optional TTS after 3-second hold

---

## 📁 Project Structure

```
asl-translator/
│
├── 📄 app.py                    # Entry point
├── 📄 train.py                  # Model training script
├── 📄 requirements.txt          # Dependencies
│
├── 📁 slr/
│   ├── 📄 main.py               # Main application logic
│   │
│   ├── 📁 model/
│   │   ├── 📄 classifier.py     # TFLite inference wrapper
│   │   ├── 🧠 slr_model.tflite  # Trained model (optimized)
│   │   ├── 🧠 slr_model.hdf5    # Trained model (Keras)
│   │   ├── 📊 keypoint.csv      # Training data (~48K samples)
│   │   └── 🏷️ label.csv         # Class labels (24 letters)
│   │
│   └── 📁 utils/
│       ├── 📄 landmarks.py      # MediaPipe hand detection
│       ├── 📄 pre_process.py    # Data preprocessing
│       ├── 📄 draw_debug.py     # Visualization helpers
│       └── 📄 logging.py        # Data collection utilities
│
├── 📁 docs/                     # Documentation images
└── 📁 resources/                # UI assets
```

---

## 🏋️ Training

### Train Your Own Model

<details>
<summary><b>📝 Step 1: Collect Data</b></summary>

1. Run the app: `python app.py`
2. Press <kbd>K</kbd> to enter logging mode
3. Press number keys to select the sign class
4. Perform the sign to record samples
5. Data saves to `slr/model/keypoint.csv`

</details>

<details>
<summary><b>🚀 Step 2: Train Model</b></summary>

```bash
python train.py
```

Training includes:
- Automatic train/validation split
- Class weight balancing
- Early stopping & learning rate reduction
- Model checkpoint saving

</details>

<details>
<summary><b>📊 Step 3: Results</b></summary>

The trained model achieves:
- **Validation Accuracy:** 99.98%
- **Validation Loss:** 0.0013

Models saved:
- `slr/model/slr_model.hdf5` — Keras format
- `slr/model/slr_model.tflite` — Optimized for inference

</details>

### Model Architecture

```
Input (42) → Dense(128) → BatchNorm → Dropout(0.3)
          → Dense(64)  → BatchNorm → Dropout(0.3)
          → Dense(32)  → BatchNorm
          → Dense(24)  → Softmax
```

| Layer | Output Shape | Parameters |
|-------|-------------|------------|
| Input | (42,) | — |
| Dense | (128,) | 5,504 |
| BatchNorm | (128,) | 512 |
| Dense | (64,) | 8,256 |
| BatchNorm | (64,) | 256 |
| Dense | (32,) | 2,080 |
| BatchNorm | (32,) | 128 |
| Dense | (24,) | 792 |
| **Total** | — | **~17.5K** |

---

## 🔧 Technologies

<div align="center">

| Technology | Purpose |
|:---:|---|
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40"> | **Python** — Core language |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg" width="40"> | **TensorFlow** — Model training |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" width="40"> | **OpenCV** — Image processing |
| 🖐️ | **MediaPipe** — Hand detection |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" width="40"> | **NumPy** — Data manipulation |

</div>

---

## 📋 Requirements

```txt
tensorflow==2.13.1
mediapipe==0.10.21
opencv-python==4.6.0.66
numpy==1.24.3
pandas==2.0.1
scikit-learn==1.2.2
matplotlib==3.7.1
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🌟 Star this repo if you found it helpful!

Made with ❤️ by [Hamdan](https://github.com/Hamdan772)

<img src="docs/hand-landmarks.png" width="150">

*Bridging communication through technology*

</div>
