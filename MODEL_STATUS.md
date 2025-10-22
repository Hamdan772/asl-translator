# 🤖 ML Model Status

## ⚠️ Model Training In Progress

The machine learning model for this ASL Translator is currently being trained with real hand gesture data.

### Current Status
- **Training Data**: Being collected
- **Model File**: Not yet available
- **Estimated Completion**: In progress

### How to Train the Model

1. **Run the application**:
   ```bash
   python3 main.py
   ```

2. **Enter Training Mode** (Press `T`):
   - The app will guide you through capturing hand gestures

3. **Capture Training Data**:
   - Press any letter key (A-Z) to select what gesture to train
   - Make the ASL sign and hold steady
   - Press ENTER repeatedly (15-20 times per letter)
   - Train at least 2 different letters

4. **Train the Model**:
   - Press `B` for Bulk Training (recommended - removes outliers)
   - OR Press `M` for standard training

5. **Start Recognizing**:
   - Once trained, the model will automatically recognize your ASL gestures!

### Requirements
- Minimum 2 different letters with 10+ samples each
- Recommended: 5-10 letters with 15-20 samples each for best accuracy

### Files
- `training_data.json` - Captured hand landmark data
- `asl_model.pkl` - Trained ML model (generated after training)
- `asl_model_scaler.pkl` - Feature scaler (generated after training)

---

*Note: Pre-trained models are not included. You must train the model with your own hand gestures for personalized accuracy.*
