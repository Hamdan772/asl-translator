"""
ASL Translator - Main Application
Translates hand signs to text in real-time using webcam
Enhanced version with back-of-hand support and improved UI
Optimized for fast startup and crash prevention
"""
import cv2
import time
import numpy as np
import os
import sys
from collections import deque
from datetime import datetime
from typing import Optional, Tuple

try:
    from hand_detector import HandDetector
    from asl_classifier import ASLClassifier
except ImportError:
    print("❌ Error: Could not import required modules")
    print("Make sure you're running from the correct directory")
    sys.exit(1)

# Lazy import ML trainer (slow to load due to sklearn/scipy)
MLTrainer = None


class ASLTranslator:
    def __init__(self):
        """Initialize the ASL Translator with ENHANCED features"""
        try:
            self.detector = HandDetector(max_hands=1, detection_con=0.8)
            self.classifier = ASLClassifier()
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            raise
        
        # Text display variables
        self.current_text = ""
        self.last_letter = ""
        self.letter_start_time = 0
        self.hold_time = 1.0  # Hold for 1 second before inserting
        self.last_confidence = 0
        self.last_letter_added_time = 0  # Track when last letter was added
        self.letter_cooldown = 1.5  # 1.5 second pause between letters
        
        # History tracking
        self.letter_history = deque(maxlen=10)
        self.gesture_timeline = deque(maxlen=20)
        self.last_wave_detected = 0
        self.wave_cooldown = 5.0  # Cooldown between wave greetings
        
        # Statistics
        self.session_start = time.time()
        self.letters_added = 0
        self.total_gestures_detected = 0
        self.show_stats = False
        
        # Audio feedback (system beep)
        self.audio_enabled = True
        
        # GAMIFICATION FEATURES DISABLED (but initialized to prevent errors)
        self.practice_mode = False  # Disabled
        self.recording = False  # Disabled
        self.video_writer = None  # Disabled
        self.recording_start_time = 0  # Disabled
        self.custom_words = []  # Disabled
        self.voice_enabled = False  # Disabled
        
        # UI settings
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_thickness = 2
        
        # Animation variables
        self.letter_flash_time = 0
        self.flash_duration = 0.5
        self.show_help = False
        
        # Color scheme (BGR format)
        self.color_primary = (50, 205, 50)      # Lime green
        self.color_secondary = (0, 165, 255)    # Orange
        self.color_text = (255, 255, 255)       # White
        self.color_bg = (40, 40, 40)            # Dark gray
        self.color_progress = (0, 255, 0)       # Green
        self.color_warning = (0, 200, 255)      # Yellow-orange
        self.color_accent = (255, 100, 255)     # Pink
        
        # Word suggestions
        self.common_words = [
            "HELLO", "THANKS", "PLEASE", "YES", "NO", "HELP", "SORRY",
            "GOOD", "BAD", "FRIEND", "FAMILY", "LOVE", "WORK", "HOME",
            "MORNING", "NIGHT", "DAY", "TIME", "WANT", "NEED", "LIKE",
            "THANK", "YOU", "ME", "WE", "THEY", "CAN", "WILL", "WOULD"
        ]
        
        # ========== NEW ADVANCED FEATURES ==========
        
        # Multiplayer Mode (two hands)
        self.multiplayer_enabled = False
        self.player1_text = ""
        self.player2_text = ""
        
        # Performance Analytics
        self.analytics = {
            'letter_accuracy': {},  # Per-letter accuracy tracking
            'speed_history': [],     # Speed over time
            'session_history': [],   # Historical sessions
            'mistake_count': 0,
            'correction_count': 0,
            'avg_confidence': []
        }
        
        # ========== MACHINE LEARNING FEATURES ==========
        # Initialize ML trainer for adaptive learning (lazy loaded)
        self.ml_trainer = None
        self.ml_trainer_loaded = False
        
        # Learning Mode (RE-ENABLED for real training)
        self.learning_mode = False
        self.direct_letter_mode = False  # Press T to enable A-Z keys directly
        self.current_training_letter = None  # Which letter we're currently training
        self.training_count = {}  # Count samples per letter
        self.learning_stage = 'capture'  # 'capture' or 'label'
        self.captured_landmarks = None
        self.learning_prompt = ""
        self.ml_confidence_threshold = 0.70  # Use ML if confidence > 70%
        self.ml_enabled = False  # ML needs to be trained first
        
        # Number-to-Letter mapping for training (Keys 3-9, 0)
        # Key 1 = Toggle training mode, Key 2 = Train model
        self.number_to_letters = {
            3: ['A', 'K', 'U'],   # Key 3: cycles through A, K, U
            4: ['B', 'L', 'V'],   # Key 4: cycles through B, L, V
            5: ['C', 'M', 'W'],   # Key 5: cycles through C, M, W
            6: ['D', 'N', 'X'],   # Key 6: cycles through D, N, X
            7: ['E', 'O', 'Y'],   # Key 7: cycles through E, O, Y
            8: ['F', 'P', 'Z'],   # Key 8: cycles through F, P, Z
            9: ['G', 'Q'],        # Key 9: cycles through G, Q
            0: ['H', 'R', 'I', 'S', 'J', 'T'],  # Key 0: cycles through H, R, I, S, J, T
        }
        self.current_number_index = {}  # Track which letter in the cycle for each number
        
        # Debug mode (can be toggled with 'D' key)
        self.debug_mode = False
    

    def load_ml_trainer(self):
        """Lazy load ML trainer (takes time due to sklearn/scipy imports)"""
        if self.ml_trainer_loaded:
            return True
        
        try:
            print("🔄 Loading ML trainer (this may take a few seconds)...")
            global MLTrainer
            from ml_trainer import MLTrainer
            self.ml_trainer = MLTrainer()
            self.ml_trainer_loaded = True
            self.ml_enabled = self.ml_trainer.model is not None
            print("✅ ML trainer loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to load ML trainer: {e}")
            return False
    
    def play_sound(self, sound_type='letter'):
        """Play system sound for feedback"""
        if not self.audio_enabled:
            return
        
        try:
            # Use macOS system sounds
            if sound_type == 'letter':
                os.system('afplay /System/Library/Sounds/Tink.aiff &')
            elif sound_type == 'wave':
                os.system('afplay /System/Library/Sounds/Glass.aiff &')
            elif sound_type == 'thumbs_up':
                os.system('afplay /System/Library/Sounds/Hero.aiff &')
            elif sound_type == 'thumbs_down':
                os.system('afplay /System/Library/Sounds/Basso.aiff &')
        except:
            # Silently fail if sounds don't work
            pass
        
    def get_word_suggestions(self):
        """Get word suggestions based on current partial text"""
        if not self.current_text:
            return []
        
        # Get last word being typed
        words = self.current_text.split()
        if not words:
            return []
        
        partial = words[-1].upper()
        if len(partial) < 2:
            return []
        
        # Find matching words
        suggestions = [w for w in self.common_words if w.startswith(partial)]
        return suggestions[:3]  # Return top 3
    
    def draw_help_overlay(self, img):
        """Draw help overlay with ASL letter reference"""
        h, w, c = img.shape
        
        # Semi-transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (50, 50), (w - 50, h - 50), self.color_bg, -1)
        img_out = cv2.addWeighted(overlay, 0.9, img, 0.1, 0)
        
        # Title
        cv2.putText(img_out, "ASL LETTER GUIDE (Back of Hand View)", (80, 100), 
                   cv2.FONT_HERSHEY_DUPLEX, 1, self.color_primary, 2, cv2.LINE_AA)
        
        # Instructions in columns - ALL 24 SUPPORTED LETTERS
        letters = [
            ("A", "Fist, thumb on side"),
            ("B", "All 4 fingers up, together"),
            ("C", "Curved hand shape"),
            ("D", "Index up, thumb touches"),
            ("E", "Complete fist, all closed"),
            ("F", "Thumb+index circle, others up"),
            ("G", "Thumb+index sideways (gun)"),
            ("H", "Index+middle horizontal"),
            ("I", "Pinky up only"),
            ("K", "Index+middle+thumb up"),
            ("L", "Thumb+index L shape"),
            ("M", "Thumb under 3 fingers"),
            ("N", "Thumb under 2 fingers"),
            ("O", "Fingers form circle"),
            ("P", "Index down, middle out"),
            ("Q", "Thumb+middle down"),
            ("R", "Index+middle crossed"),
            ("S", "Fist, thumb across front"),
            ("T", "Thumb between fingers"),
            ("U", "Index+middle together, up"),
            ("V", "Index+middle apart (peace)"),
            ("W", "Three fingers up, apart"),
            ("X", "Index bent in hook"),
            ("Y", "Thumb+pinky out (shaka)"),
        ]
        
        x_offset = 80
        y_offset = 150
        col_width = 360
        row_height = 42
        
        for i, (letter, desc) in enumerate(letters):
            col = i // 8  # 8 rows per column for better fit
            row = i % 8
            x = x_offset + col * col_width
            y = y_offset + row * row_height
            
            # Letter
            cv2.putText(img_out, letter, (x, y), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, self.color_accent, 2, cv2.LINE_AA)
            
            # Description
            cv2.putText(img_out, f"- {desc}", (x + 40, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
        
        # Footer with note about missing letters
        cv2.putText(img_out, "Note: J and Z require motion (not supported)", (w // 2 - 250, h - 170), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 1, cv2.LINE_AA)
        
        # Number key mapping guide
        cv2.putText(img_out, "TRAINING: Press 1 to enter training | Press 2 to train model", (80, h - 130), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_primary, 1, cv2.LINE_AA)
        cv2.putText(img_out, "Letters: 3=A/K/U 4=B/L/V 5=C/M/W 6=D/N/X 7=E/O/Y 8=F/P/Z 9=G/Q 0=H/R/I/S/J/T", (80, h - 105), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.color_text, 1, cv2.LINE_AA)
        
        cv2.putText(img_out, "Press 'H' to close help", (w // 2 - 150, h - 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.color_warning, 2, cv2.LINE_AA)
        
        return img_out
    
    def draw_ui_overlay(self, img, detected_letter, confidence, is_back_of_hand):
        """Draw enhanced UI overlay with better visuals"""
        h, w, c = img.shape
        
        # Create semi-transparent overlay for header
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), self.color_bg, -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # ML Status Indicator (top-left corner)
        ml_status = "🤖 ML: ON" if self.ml_enabled else "⚠️  ML: OFF"
        ml_color = (0, 255, 0) if self.ml_enabled else (0, 165, 255)
        cv2.putText(img, ml_status, (20, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, ml_color, 2, cv2.LINE_AA)
        
        # Display translated text with better formatting
        text_display = self.current_text if self.current_text else "Start signing..."
        if len(text_display) > 50:
            text_display = "..." + text_display[-47:]
        
        cv2.putText(img, text_display, (20, 50), 
                   self.font, 1.2, self.color_text, 2, cv2.LINE_AA)
        
        # Info panel - right side
        info_x = w - 320
        info_y = 100
        
        # Semi-transparent info box
        overlay = img.copy()
        cv2.rectangle(overlay, (info_x - 10, info_y - 10), 
                     (w - 10, info_y + 200), self.color_bg, -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Hand orientation indicator
        hand_status = "BACK" if is_back_of_hand else "PALM"
        hand_color = self.color_primary if is_back_of_hand else self.color_warning
        cv2.putText(img, f"View: {hand_status}", (info_x, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, hand_color, 2, cv2.LINE_AA)
        
        # Detected letter with flash effect
        if detected_letter:
            current_time = time.time()
            if detected_letter != self.last_letter:
                self.letter_flash_time = current_time
            
            # Flash effect
            flash_progress = (current_time - self.letter_flash_time) / self.flash_duration
            if flash_progress < 1.0:
                flash_alpha = int(255 * (1 - flash_progress))
                letter_color = (0, flash_alpha, 255)
            else:
                letter_color = self.color_primary
            
            cv2.putText(img, f"Letter: {detected_letter}", (info_x, info_y + 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, letter_color, 2, cv2.LINE_AA)
            
            # Confidence bar
            cv2.putText(img, "Confidence:", (info_x, info_y + 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
            
            bar_width = 200
            bar_height = 15
            bar_x = info_x
            bar_y = info_y + 80
            
            # Background bar
            cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), 
                         (100, 100, 100), 2)
            
            # Confidence fill
            fill_width = int(bar_width * confidence)
            conf_color = self.color_primary if confidence > 0.60 else self.color_warning
            cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), 
                         conf_color, -1)
            
            # Confidence percentage
            cv2.putText(img, f"{int(confidence * 100)}%", (bar_x + bar_width + 10, bar_y + 12), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "No hand detected", (info_x, info_y + 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1, cv2.LINE_AA)
        
        # Instructions
        instructions = [
            "Hold gesture 1s to add (1.5s cooldown)",
            "SPACE: space | BACKSPACE: delete",
            "C: clear | H: help | Q: quit"
        ]
        
        inst_y = h - 90
        for i, inst in enumerate(instructions):
            cv2.putText(img, inst, (20, inst_y + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
        
        return img
    
    def draw_gesture_timeline(self, img):
        """Draw timeline of recent gestures"""
        h, w, c = img.shape
        
        # Timeline box
        box_height = 60
        box_y = h - box_height - 140
        
        overlay = img.copy()
        cv2.rectangle(overlay, (20, box_y), (w - 20, box_y + box_height), 
                     self.color_bg, -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Title
        cv2.putText(img, "Recent Gestures:", (30, box_y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
        
        # Draw timeline items
        if self.gesture_timeline:
            x_start = 200
            spacing = 40
            for i, (letter, conf) in enumerate(list(self.gesture_timeline)[-15:]):
                x = x_start + i * spacing
                
                # Color based on confidence
                if conf > 0.8:
                    color = self.color_primary
                elif conf > 0.6:
                    color = self.color_warning
                else:
                    color = (128, 128, 128)
                
                cv2.putText(img, letter, (x, box_y + 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
        
        return img
    
    def show_wave_greeting(self, img):
        """Show animated 'HELLO!' greeting when wave is detected"""
        h, w, c = img.shape
        
        # Large centered text with animation
        greeting = "HELLO!"
        
        # Calculate text size for centering
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 2.5
        thickness = 4
        
        text_size = cv2.getTextSize(greeting, font, font_scale, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = (h + text_size[1]) // 2
        
        # Draw background box
        padding = 40
        cv2.rectangle(img, 
                     (text_x - padding, text_y - text_size[1] - padding),
                     (text_x + text_size[0] + padding, text_y + padding),
                     self.color_bg, -1)
        
        # Draw border
        cv2.rectangle(img, 
                     (text_x - padding, text_y - text_size[1] - padding),
                     (text_x + text_size[0] + padding, text_y + padding),
                     self.color_primary, 4)
        
        # Draw text with glow effect
        # Shadow
        cv2.putText(img, greeting, (text_x + 3, text_y + 3), 
                   font, font_scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
        
        # Main text
        cv2.putText(img, greeting, (text_x, text_y), 
                   font, font_scale, self.color_primary, thickness, cv2.LINE_AA)
        
        # Add wave emojis on sides
        emoji_font_scale = 3.0
        cv2.putText(img, "!", (text_x - 80, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, emoji_font_scale, self.color_warning, 3, cv2.LINE_AA)
        cv2.putText(img, "!", (text_x + text_size[0] + 50, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, emoji_font_scale, self.color_warning, 3, cv2.LINE_AA)
        
        return img
    
    def draw_word_suggestions(self, img):
        """Draw word suggestions"""
        suggestions = self.get_word_suggestions()
        if not suggestions:
            return img
        
        h, w, c = img.shape
        x = 20
        y = 100
        
        cv2.putText(img, "Suggestions:", (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
        
        for i, word in enumerate(suggestions):
            cv2.putText(img, f"{i+1}. {word}", (x, y + 30 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_accent, 1, cv2.LINE_AA)
        
        return img
    
    def save_to_file(self):
        """Save translated text to a file"""
        if not self.current_text.strip():
            print("⚠️  No text to save!")
            return
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"asl_translation_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("ASL Translation\n")
                f.write("=" * 50 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Letters: {self.letters_added}\n")
                f.write(f"Session Duration: {self.get_session_duration()}\n")
                f.write("=" * 50 + "\n\n")
                f.write(self.current_text)
            
            print(f"💾 Saved to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return None
    
    def get_session_duration(self):
        """Get formatted session duration"""
        duration = time.time() - self.session_start
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return f"{minutes}m {seconds}s"
    
    def get_letters_per_minute(self):
        """Calculate letters per minute"""
        duration = (time.time() - self.session_start) / 60  # minutes
        if duration < 0.1:
            return 0
        return self.letters_added / duration
    
    def draw_stats_overlay(self, img):
        """Draw statistics overlay"""
        h, w, c = img.shape
        
        # Semi-transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (50, 50), (w - 50, h - 50), self.color_bg, -1)
        img_out = cv2.addWeighted(overlay, 0.9, img, 0.1, 0)
        
        # Title
        cv2.putText(img_out, "SESSION STATISTICS", (w // 2 - 200, 120), 
                   cv2.FONT_HERSHEY_DUPLEX, 1.2, self.color_primary, 2, cv2.LINE_AA)
        
        # Stats
        stats = [
            f"Session Duration: {self.get_session_duration()}",
            f"Letters Added: {self.letters_added}",
            f"Total Gestures Detected: {self.total_gestures_detected}",
            f"Letters Per Minute: {self.get_letters_per_minute():.1f}",
            f"Current Text Length: {len(self.current_text)} characters",
            f"Words: {len(self.current_text.split())}",
            "",
            "Press 'S' to close statistics"
        ]
        
        y_offset = 200
        for stat in stats:
            cv2.putText(img_out, stat, (150, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.color_text, 2, cv2.LINE_AA)
            y_offset += 50
        
        return img_out
        """Draw enhanced UI overlay with better visuals"""
        h, w, c = img.shape
        
        # Create semi-transparent overlay for header
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), self.color_bg, -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Display translated text with better formatting
        text_display = self.current_text if self.current_text else "Start signing..."
        if len(text_display) > 50:
            text_display = "..." + text_display[-47:]
        
        cv2.putText(img, text_display, (20, 50), 
                   self.font, 1.2, self.color_text, 2, cv2.LINE_AA)
        
        # Info panel - right side
        info_x = w - 320
        info_y = 100
        
        # Semi-transparent info box
        overlay = img.copy()
        cv2.rectangle(overlay, (info_x - 10, info_y - 10), 
                     (w - 10, info_y + 200), self.color_bg, -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Hand orientation indicator
        hand_status = "BACK" if is_back_of_hand else "PALM"
        hand_color = self.color_primary if is_back_of_hand else self.color_warning
        cv2.putText(img, f"View: {hand_status}", (info_x, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, hand_color, 2, cv2.LINE_AA)
        
        # Detected letter with flash effect
        if detected_letter:
            current_time = time.time()
            if detected_letter != self.last_letter:
                self.letter_flash_time = current_time
            
            # Flash effect
            flash_progress = (current_time - self.letter_flash_time) / self.flash_duration
            if flash_progress < 1.0:
                flash_alpha = int(255 * (1 - flash_progress))
                letter_color = (0, flash_alpha, 255)
            else:
                letter_color = self.color_primary
            
            cv2.putText(img, f"Letter: {detected_letter}", (info_x, info_y + 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, letter_color, 2, cv2.LINE_AA)
            
            # Confidence bar
            cv2.putText(img, "Confidence:", (info_x, info_y + 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
            
            bar_width = 200
            bar_height = 15
            bar_x = info_x
            bar_y = info_y + 80
            
            # Background bar
            cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), 
                         (100, 100, 100), 2)
            
            # Confidence fill
            fill_width = int(bar_width * confidence)
            conf_color = self.color_primary if confidence > 0.60 else self.color_warning
            cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), 
                         conf_color, -1)
            
            # Confidence percentage
            cv2.putText(img, f"{int(confidence * 100)}%", (bar_x + bar_width + 10, bar_y + 12), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "No hand detected", (info_x, info_y + 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1, cv2.LINE_AA)
        
        # Instructions
        instructions = [
            "Hold gesture 1s to add (1.5s cooldown)",
            "SPACE: space | BACKSPACE: delete",
            "C: clear | H: help | Q: quit"
        ]
        
        inst_y = h - 90
        for i, inst in enumerate(instructions):
            cv2.putText(img, inst, (20, inst_y + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_text, 1, cv2.LINE_AA)
        
        return img
    
    def draw_progress_indicator(self, img, time_held, hold_time):
        """Draw a circular progress indicator"""
        h, w, c = img.shape
        center_x, center_y = w // 2, h - 80
        radius = 40
        
        # Calculate progress
        progress = min(time_held / hold_time, 1.0)
        angle = int(360 * progress)
        
        # Draw background circle
        cv2.circle(img, (center_x, center_y), radius, (100, 100, 100), 3)
        
        # Draw progress arc
        if progress > 0:
            # Create arc
            axes = (radius, radius)
            start_angle = -90
            end_angle = start_angle + angle
            
            color = self.color_progress if progress < 1.0 else (0, 255, 255)
            cv2.ellipse(img, (center_x, center_y), axes, 0, 
                       start_angle, end_angle, color, 6)
        
        # Draw percentage text
        cv2.putText(img, f"{int(progress * 100)}%", (center_x - 30, center_y + 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.color_text, 2, cv2.LINE_AA)
        
        return img
    
    def start_recording(self, frame_width, frame_height):
        """Start video recording"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"asl_recording_{timestamp}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))
        self.recording = True
        self.recording_start_time = time.time()
        print(f"🎥 Recording started: {filename}")
    
    def stop_recording(self):
        """Stop video recording"""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        self.recording = False
        duration = time.time() - self.recording_start_time
        print(f"🎥 Recording stopped (Duration: {duration:.1f}s)")
    
    def draw_practice_mode(self, img):
        """Draw practice mode interface"""
        if not self.practice_mode:
            return img
        
        h, w, c = img.shape
        
        # Draw semi-transparent overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (w//2 - 300, 50), (w//2 + 300, 250), (40, 40, 40), -1)
        img = cv2.addWeighted(overlay, 0.8, img, 0.2, 0)
        
        # Title
        cv2.putText(img, "PRACTICE MODE", (w//2 - 200, 100), 
                   cv2.FONT_HERSHEY_DUPLEX, 1.2, self.color_primary, 2, cv2.LINE_AA)
        
        # Target letter
        cv2.putText(img, f"Make this sign: {self.target_letter}", (w//2 - 180, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, self.color_text, 2, cv2.LINE_AA)
        
        # Score
        accuracy = (self.practice_score / self.practice_attempts * 100) if self.practice_attempts > 0 else 0
        cv2.putText(img, f"Score: {self.practice_score}/{self.practice_attempts} ({accuracy:.0f}%)", 
                   (w//2 - 150, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.color_accent, 2, cv2.LINE_AA)
        
        # Instructions
        cv2.putText(img, "Press P to exit practice mode", (w//2 - 180, 230), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_text, 1, cv2.LINE_AA)
        
        return img
    
    def check_practice_letter(self, detected_letter):
        """Check if detected letter matches target in practice mode"""
        if detected_letter == self.target_letter:
            self.practice_score += 1
            self.practice_attempts += 1
            self.play_sound('letter')  # Changed from thumbs_up to generic letter sound
            print(f"✅ Correct! Score: {self.practice_score}/{self.practice_attempts}")
            # Move to next letter
            self.practice_index = (self.practice_index + 1) % len(self.practice_letters)
            self.target_letter = self.practice_letters[self.practice_index]
            return True
        return False
    
    def speak_text(self, text):
        """Speak the text using macOS text-to-speech"""
        if not self.voice_enabled or not text:
            return
        
        try:
            # Use macOS 'say' command
            os.system(f'say "{text}" &')
        except:
            pass
    
    def add_custom_word(self, word):
        """Add a word to custom dictionary"""
        word = word.strip().upper()
        if word and word not in self.custom_words:
            self.custom_words.append(word)
            try:
                    with open('custom_words.txt', 'a') as f:
                        f.write(word + '\n')
                    print(f"📝 Added '{word}' to custom dictionary")
            except:
                pass
    
    def process_learning_label(self):
        """Process user input for labeling captured gesture"""
        if not self.captured_landmarks:
            return False
        
        try:
            # Get input from user (non-blocking would be better, but this works)
            print("\n" + "=" * 60)
            print("🧠 LEARNING MODE - Label Capture")
            print("=" * 60)
            label = input("Enter the letter (A-Z) this gesture represents: ").strip().upper()
            
            if len(label) == 1 and label.isalpha():
                # Add to training data
                success = self.ml_trainer.add_training_sample(self.captured_landmarks, label)
                if success:
                    print(f"✅ Training sample added for '{label}'!")
                    print(f"📦 Total samples: {len(self.ml_trainer.training_data)}")
                    
                    # Show stats
                    stats = self.ml_trainer.get_statistics()
                    print(f"📊 Samples for '{label}': {stats.get(label, 0)}")
                    
                    # Suggest training if enough data
                    if len(self.ml_trainer.training_data) >= 10:
                        print("\n💡 TIP: You have enough data! Press 'M' to train the model")
                    
                    print("=" * 60)
                    
                    # Reset for next capture
                    self.captured_landmarks = None
                    self.learning_stage = 'capture'
                    return True
                else:
                    print("❌ Failed to add training sample")
                    return False
            else:
                print("❌ Invalid input. Please enter a single letter (A-Z)")
                return False
                
        except Exception as e:
            print(f"❌ Error processing label: {e}")
            return False
    
    def run(self):
        """Main loop for the ASL translator with OPTIMIZED performance"""
        # Initialize webcam with OPTIMIZED settings for better FPS
        cap = cv2.VideoCapture(0)
        cap.set(3, 960)   # Width: Reduced from 1280 for better FPS
        cap.set(4, 540)   # Height: Reduced from 720 for better FPS
        cap.set(cv2.CAP_PROP_FPS, 60)  # Request 60 FPS
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer lag
        
        # Get actual resolution
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        print("=" * 60)
        print("🚀 ASL Translator v2.0 - SIMPLIFIED EDITION")
        print("=" * 60)
        print(f"\n📹 Camera: {actual_width}x{actual_height} @ {actual_fps} FPS (optimized)")
        print("📹 Mode: BACK OF HAND recognition")
        print("\n⌨️  CORE CONTROLS:")
        print("  • SPACE - Add space")
        print("  • BACKSPACE - Delete last character")
        print("  • C - Clear all text")
        print("  • H - Show/hide help guide")
        print("  • S - Show/hide statistics")
        print("\n⌨️  TRAINING CONTROLS:")
        print("  • 1 - Toggle TRAINING MODE (enter/exit)")
        print("  • 2 - TRAIN MODEL (auto-removes outliers)")
        print("  • 3-9, 0 - Select letters to train:")
        print("    3=A/K/U  4=B/L/V  5=C/M/W  6=D/N/X  7=E/O/Y")
        print("    8=F/P/Z  9=G/Q    0=H/R/I/S/J/T")
        print("  • ENTER - Capture sample (auto-crops hand photo)")
        print("  • B - Bulk train (advanced)")
        print("  • N - Show ML statistics")
        print("  • D - Toggle DEBUG mode")
        print("\n⌨️  EXIT:")
        print("  • ESC - Save & quit")
        print("  • Q - Quit without saving")
        print("\n✋ Usage:")
        print("  • Show the BACK of your hand to the camera")
        print("  • Hold gesture for 1 second to add letter")
        print("  • Wait 1.5 seconds before next letter (cooldown)")
        print("  • Make clear gestures for best results")
        print("\n✨ Features:")
        print("  • 121 colorful dots (21 green + 100 yellow)")
        print("  • Finger labels on each fingertip")
        print("  • FINGER STATUS panel during training")
        print("  • Automatic photo capture during training")
        print("  • Optimized 40-50 FPS performance")
        print("=" * 60)
        
        prev_time = 0
        greeting_end_time = 0  # Track when to stop showing greeting
        
        while True:
                success, img = cap.read()
                if not success:
                    print("❌ Failed to capture video")
                    continue
                
                # Flip image horizontally for mirror effect
                img = cv2.flip(img, 1)
                
                # Detect hands with enhanced visuals
                img = self.detector.find_hands(img, draw=True)
                landmarks = self.detector.find_position(img)
                
                # Check for wave gesture
                wave_detected = False
                current_time = time.time()
                
                # Check if back of hand
                is_back_of_hand = self.detector.is_back_of_hand(landmarks) if landmarks else False
                
                # ALWAYS show finger status panel when hand is detected
                if landmarks:
                    img = self.detector.draw_finger_state_indicator(img, landmarks, 10, 200)
                
                # ========== LEARNING MODE LOGIC (SIMPLIFIED) ==========
                if self.learning_mode and landmarks:
                    # Show training UI
                    h_learn, w_learn = img.shape[:2]
                    
                    if self.current_training_letter:
                        # Currently training a specific letter
                        count = self.training_count.get(self.current_training_letter, 0)
                        
                        # Show training info
                        cv2.rectangle(img, (10, 10), (w_learn - 10, 180), (0, 100, 200), -1)
                        cv2.putText(img, f"TRAINING: {self.current_training_letter}", (w_learn//2 - 150, 50),
                                   cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
                        cv2.putText(img, f"Samples collected: {count}", (w_learn//2 - 150, 100),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
                        
                        # Show expected finger states for A, V, W
                        expected_hints = {
                            'A': 'Expected: 0 fingers UP (closed fist)',
                            'V': 'Expected: 2 fingers UP (Index + Middle)',
                            'W': 'Expected: 3 fingers UP (Index + Middle + Ring)'
                        }
                        if self.current_training_letter in expected_hints:
                            cv2.putText(img, expected_hints[self.current_training_letter], 
                                       (w_learn//2 - 300, 130),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)
                        
                        if self.detector.is_hand_stable:
                            cv2.putText(img, "Press ENTER to capture this gesture!", (w_learn//2 - 250, 165),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                        else:
                            cv2.putText(img, "Hold STILL to capture...", (w_learn//2 - 200, 165),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2, cv2.LINE_AA)
                    else:
                        # No letter selected yet
                        cv2.rectangle(img, (10, 10), (w_learn - 10, 180), (100, 0, 100), -1)
                        cv2.putText(img, "LEARNING MODE ACTIVE", (w_learn//2 - 200, 50),
                                   cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 255), 2, cv2.LINE_AA)
                        cv2.putText(img, "Press any letter key (A-Z) to start training", (w_learn//2 - 300, 100),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.putText(img, "Then press ENTER to capture each sample", (w_learn//2 - 280, 150),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Classify letter if hand detected
                # Note: Stability check is now more lenient (15% threshold)
                current_letter = ""
                confidence = 0.0
                ml_prediction = None
                ml_confidence = 0.0
                
                if landmarks and not self.learning_mode:  # Skip in learning mode
                    # ONLY use ML prediction - no rule-based classifier
                    if self.ml_enabled and self.ml_trainer:
                        # Get finger states for prediction
                        finger_states = self.detector.get_finger_states(landmarks)
                        
                        # Extract hand region for HOG features
                        hand_image = None
                        try:
                            h_img, w_img = img.shape[:2]
                            x_coords = [lm[1] for lm in landmarks]
                            y_coords = [lm[2] for lm in landmarks]
                            x_min = max(0, int(min(x_coords) * w_img) - 40)
                            x_max = min(w_img, int(max(x_coords) * w_img) + 40)
                            y_min = max(0, int(min(y_coords) * h_img) - 40)
                            y_max = min(h_img, int(max(y_coords) * h_img) + 40)
                            
                            # Validate dimensions
                            if x_max > x_min and y_max > y_min and x_max <= w_img and y_max <= h_img:
                                hand_image = img[y_min:y_max, x_min:x_max]
                                # Verify image is not empty
                                if hand_image.size == 0:
                                    hand_image = None
                        except Exception as e:
                            pass  # If cropping fails, proceed without image features
                        
                        # Predict with landmarks, finger states, AND hand image
                        ml_prediction, ml_confidence = self.ml_trainer.predict(landmarks, finger_states, hand_image)
                        
                        # Apply rule-based corrections for V vs W confusion
                        if ml_prediction in ['V', 'W'] and finger_states:
                            finger_count = sum([
                                finger_states.get('thumb', False),
                                finger_states.get('index', False),
                                finger_states.get('middle', False),
                                finger_states.get('ring', False),
                                finger_states.get('pinky', False)
                            ])
                            
                            # V should have exactly 2 fingers (index + middle)
                            # W should have exactly 3 fingers (index + middle + ring)
                            if ml_prediction == 'W' and finger_count == 2:
                                # Likely V, not W
                                if finger_states.get('index') and finger_states.get('middle') and not finger_states.get('ring'):
                                    print(f"🔧 Correcting W→V (only 2 fingers detected)")
                                    ml_prediction = 'V'
                                    ml_confidence *= 0.9  # Slightly reduce confidence
                            elif ml_prediction == 'V' and finger_count == 3:
                                # Likely W, not V
                                if finger_states.get('index') and finger_states.get('middle') and finger_states.get('ring'):
                                    print(f"🔧 Correcting V→W (3 fingers detected)")
                                    ml_prediction = 'W'
                                    ml_confidence *= 0.9
                        
                        if ml_confidence > self.ml_confidence_threshold:
                            current_letter = ml_prediction
                            confidence = ml_confidence
                            print(f"🤖 ML prediction: {ml_prediction} ({ml_confidence:.2%})")
                    # If no ML model trained, no letters will be detected
                    
                    self.last_confidence = confidence
                    
                    # Boost confidence if hand is stable
                    if confidence > 0 and self.detector.is_hand_stable:
                        stability_bonus = 0.05
                        confidence = min(confidence + stability_bonus, 1.0)
                    
                    # Show detections with STRICT threshold
                    if current_letter and confidence > 0.65:  # STRICT: Only show high confidence
                        stability_status = "stable" if self.detector.is_hand_stable else "moving"
                        print(f"👁️  Detected: {current_letter} (confidence: {confidence:.2f}, hand: {stability_status})")
                    
                    # Add to gesture timeline - STRICT threshold
                    if current_letter and confidence > 0.60:  # STRICT: High confidence for timeline
                        if not self.gesture_timeline or self.gesture_timeline[-1][0] != current_letter:
                            self.gesture_timeline.append((current_letter, confidence))
                            self.total_gestures_detected += 1
                    elif confidence < 0.65:  # STRICT: Reject low confidence
                        # Low confidence - ignore
                        current_letter = ""
                        confidence = 0.0
                
                # PRACTICE MODE: Check if detected letter matches target (STRICT)
                if self.practice_mode and current_letter and confidence > 0.75:  # STRICT: High confidence required
                    if self.check_practice_letter(current_letter):
                        current_letter = ""  # Reset after successful match
                
                # Handle letter detection with hold time (only in normal mode)
                current_time = time.time()
                time_held = 0
                
                # Get image dimensions for cooldown display
                h, w = img.shape[:2]
                
                # Check if we're still in cooldown period
                time_since_last_letter = current_time - self.last_letter_added_time
                in_cooldown = time_since_last_letter < self.letter_cooldown
                
                if current_letter and current_letter != "" and not self.practice_mode:
                    if in_cooldown:
                        # Still in cooldown - show cooldown indicator
                        cooldown_remaining = self.letter_cooldown - time_since_last_letter
                        cv2.putText(img, f"Cooldown: {cooldown_remaining:.1f}s", 
                                   (w//2 - 100, h - 50),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.color_warning, 2, cv2.LINE_AA)
                        self.last_letter = ""  # Reset to prevent starting hold during cooldown
                    elif current_letter == self.last_letter:
                        # Same letter held (and not in cooldown)
                        time_held = current_time - self.letter_start_time
                        
                        # Draw circular progress indicator
                        img = self.draw_progress_indicator(img, time_held, self.hold_time)
                        
                        if time_held >= self.hold_time:
                            # Add letter to text
                            self.current_text += current_letter
                            self.letter_history.append(current_letter)
                            self.letters_added += 1
                            self.last_letter = ""
                            self.letter_start_time = current_time
                            self.last_letter_added_time = current_time  # Start cooldown
                            self.play_sound('letter')
                            
                            # Check for word completion
                            suggestions = self.get_word_suggestions()
                            if suggestions:
                                print(f"✅ Added: '{current_letter}' | Text: {self.current_text} | Suggestions: {', '.join(suggestions)}")
                            else:
                                print(f"✅ Added: '{current_letter}' | Text: {self.current_text}")
                    else:
                        # New letter detected (and not in cooldown)
                        self.last_letter = current_letter
                        self.letter_start_time = current_time
                else:
                    # No valid letter detected
                    self.last_letter = ""
                
                # Draw enhanced UI overlay
                img = self.draw_ui_overlay(img, current_letter, confidence, is_back_of_hand)
                
                # Draw gesture timeline
                img = self.draw_gesture_timeline(img)
                
                # Draw word suggestions
                img = self.draw_word_suggestions(img)
                
                # Show greeting animation if wave was recently detected
                if current_time < greeting_end_time:
                    img = self.show_wave_greeting(img)
                
                # Show practice mode overlay if enabled
                if self.practice_mode:
                    img = self.draw_practice_mode(img)
                
                # Show help overlay if enabled
                if self.show_help:
                    img = self.draw_help_overlay(img)
                
                # Show stats overlay if enabled
                if self.show_stats:
                    img = self.draw_stats_overlay(img)
                
                # Show recording indicator if recording
                if self.recording:
                    cv2.circle(img, (30, 30), 10, (0, 0, 255), -1)
                    cv2.putText(img, "REC", (50, 40), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                    duration = int(time.time() - self.recording_start_time)
                    cv2.putText(img, f"{duration}s", (100, 40), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                
                # Show stability indicator
                if landmarks:
                    stability_text = "STABLE" if self.detector.is_hand_stable else "MOVING"
                    stability_color = (0, 255, 0) if self.detector.is_hand_stable else (0, 165, 255)
                    cv2.putText(img, stability_text, (img.shape[1] - 150, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, stability_color, 2, cv2.LINE_AA)
                
                # Calculate and display FPS
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
                prev_time = curr_time
                
                cv2.putText(img, f"FPS: {int(fps)}", (img.shape[1] - 150, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_warning, 2, cv2.LINE_AA)
                
                # Write frame to video if recording
                if self.recording and self.video_writer:
                    self.video_writer.write(img)
                
                # Update analytics
                if current_letter and confidence > 0:
                    self.analytics['avg_confidence'].append(confidence)
                    if len(self.analytics['avg_confidence']) > 100:
                        self.analytics['avg_confidence'].pop(0)
                
                # Show the image
                cv2.imshow("ASL Translator - Enhanced v2.0 🚀", img)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                # DEBUG: Show key code when in learning mode (if debug enabled)
                if self.debug_mode and key != 255 and self.learning_mode:
                    print(f"🔍 Key pressed: {key} (char: '{chr(key) if 32 <= key <= 126 else '?'}')")
                
                if key == ord('q'):
                    print("\n" + "=" * 60)
                    print("👋 Exiting without saving...")
                    print(f"📝 Final text: {self.current_text}")
                    print("=" * 60)
                    break
                elif key == 27:  # ESC key
                    print("\n" + "=" * 60)
                    print("💾 Saving and exiting...")
                    filename = self.save_to_file()
                    if filename:
                        print(f"✅ Saved to: {filename}")
                    print(f"📝 Final text: {self.current_text}")
                    print("=" * 60)
                    break
                elif key == ord(' '):
                    self.current_text += " "
                    print(f"➕ Added space | Text: {self.current_text}")
                elif key == 8 or key == 127:  # Backspace or Delete
                    if self.current_text:
                        deleted = self.current_text[-1]
                        self.current_text = self.current_text[:-1]
                        print(f"⬅️  Deleted: '{deleted}' | Text: {self.current_text}")
                elif key == ord('c') or key == ord('C'):
                    self.current_text = ""
                    self.letter_history.clear()
                    print("🗑️  Cleared all text")
                elif key == ord('h') or key == ord('H'):
                    self.show_help = not self.show_help
                    print(f"📚 Help {'shown' if self.show_help else 'hidden'}")
                elif key == ord('s') or key == ord('S'):
                    self.show_stats = not self.show_stats
                    print(f"📊 Statistics {'shown' if self.show_stats else 'hidden'}")
                
                # GAMIFICATION FEATURES DISABLED (keys 1-8)
                # elif key in [ord('1'), ord('2'), ord('3')]:
                #     # Accept word suggestion
                #     suggestions = self.get_word_suggestions()
                #     suggestion_idx = int(chr(key)) - 1
                #     if suggestion_idx < len(suggestions):
                #         words = self.current_text.split()
                #         if words:
                #             words[-1] = suggestions[suggestion_idx]
                #             self.current_text = " ".join(words) + " "
                #             print(f"✨ Accepted suggestion: {suggestions[suggestion_idx]}")
                # elif key == ord('4'):
                #     # Toggle practice mode
                # elif key == ord('5'):
                #     # Toggle recording
                # elif key == ord('6'):
                #     # Toggle voice output
                # elif key == ord('7'):
                #     # Add last word to custom dictionary
                # elif key == ord('8'):
                #     # Show gamification stats
                
                # Debug mode toggle (Press 'D')
                elif key == ord('d') or key == ord('D'):
                    self.debug_mode = not self.debug_mode
                    if self.debug_mode:
                        print("\n🔍 DEBUG MODE ENABLED - Detailed logs will be shown")
                    else:
                        print("\n🔍 DEBUG MODE DISABLED - Clean output")
                
                # Direct letter typing mode (Press 'T') - TYPE LETTERS DIRECTLY
                elif key == ord('t') or key == ord('T'):
                    if self.learning_mode:
                        self.direct_letter_mode = not self.direct_letter_mode
                        if self.direct_letter_mode:
                            print("\n⌨️  DIRECT LETTER MODE ENABLED")
                            print("💡 Now you can press A-Z keys directly to select letters!")
                            print("💡 Press T again to go back to number keys")
                        else:
                            print("\n⌨️  DIRECT LETTER MODE DISABLED")
                            print("💡 Use number keys (3-9, 0) to select letters")
                    else:
                        print("\n⚠️  You must be in training mode first!")
                        print("💡 Press 1 to enter training mode")
                
                # Learning mode (Press '1') - ENTER TRAINING MODE
                elif key == 49:  # Key '1'
                    self.learning_mode = not self.learning_mode
                    if not self.learning_mode:
                        self.current_training_letter = None
                        self.direct_letter_mode = False  # Reset when exiting
                        print("\n❌ Training mode deactivated")
                        print("💡 Press 1 again to re-enter training mode")
                    else:
                        print("\n" + "=" * 60)
                        print("🎓 TRAINING MODE ACTIVATED")
                        print("=" * 60)
                        print("📝 Instructions:")
                        print("  • Press T to enable DIRECT LETTER TYPING (A-Z keys)")
                        print("  • OR use NUMBER keys (3-9, 0) to select letters:")
                        print("    3=A/K/U  4=B/L/V  5=C/M/W  6=D/N/X  7=E/O/Y")
                        print("    8=F/P/Z  9=G/Q    0=H/R/I/S/J/T")
                        print("  • Make ASL sign and hold steady")
                        print("  • Press ENTER repeatedly to capture 15-20 samples")
                        print("  • Press 2 when done to TRAIN THE MODEL")
                        print("  • Press 1 to exit training mode")
                        print("\n💡 TIP: Photos auto-cropped to hand region only!")
                        print("=" * 60)
                
                # Train ML model (Press '2') - TRAIN MODEL
                elif key == 50:  # Key '2'
                    print("\n🧠 TRAINING MODEL (with automatic outlier removal)...")
                    if self.load_ml_trainer():
                        result = self.ml_trainer.bulk_train_with_outlier_removal()
                        # Result is a tuple (accuracy, outliers_dict)
                        if result and result[0]:  # Check if accuracy is not None
                            accuracy, outliers = result
                            self.ml_enabled = True
                            self.learning_mode = False  # Exit learning mode
                            self.current_training_letter = None
                            print(f"✅ Model trained! Accuracy: {accuracy:.2%}")
                            print("🎉 ML model is now ACTIVE and ready to use!")
                            print("💡 Make ASL gestures and the model will recognize them!")
                        else:
                            print("❌ Training failed - need more samples")
                            print("💡 TIP: Capture at least 10 samples for 2+ different letters")
                
                # Bulk train with outlier removal (Press 'B') - Check BEFORE letter key handling
                elif key == ord('b') or key == ord('B'):
                    print("\n🚀 BULK TRAINING with outlier removal...")
                    if self.load_ml_trainer():
                        result = self.ml_trainer.bulk_train_with_outlier_removal()
                        # Result is a tuple (accuracy, outliers_dict)
                        if result and result[0]:  # Check if accuracy is not None
                            accuracy, outliers = result
                            self.ml_enabled = True
                            self.learning_mode = False  # Exit learning mode
                            self.current_training_letter = None
                            print(f"✅ Model trained! Accuracy: {accuracy:.2%}")
                            print("🎉 ML model is now ACTIVE and ready to use!")
                            print("💡 Make ASL gestures and the model will recognize them!")
                        else:
                            print("❌ Training failed - need more samples")
                            print("💡 TIP: Capture at least 10 samples for 2+ different letters")
                
                # Handle A-Z key presses in DIRECT LETTER MODE
                elif self.learning_mode and self.direct_letter_mode and (65 <= key <= 90 or 97 <= key <= 122):
                    letter = chr(key).upper()
                    self.current_training_letter = letter
                    count = self.training_count.get(letter, 0)
                    print(f"\n🎯 Selected letter: {letter} (Current samples: {count})")
                    print("💡 Make the gesture and press ENTER to capture")
                
                # Handle NUMBER key presses in learning mode (3-9, 0 to select letters)
                elif self.learning_mode and not self.direct_letter_mode and (48 == key or (51 <= key <= 57)):  # Keys 0, 3-9
                    number = key - 48  # Convert to 0-9
                    
                    # Skip keys 1 and 2 (they're commands)
                    if number in [1, 2]:
                        continue
                    
                    # Get available letters for this number
                    available_letters = self.number_to_letters.get(number, [])
                    if not available_letters:
                        print(f"⚠️  No letters mapped to key {number}")
                        print("💡 Use keys 3-9 or 0 to select letters")
                        continue
                    
                    # Cycle through letters for this number
                    if number not in self.current_number_index:
                        self.current_number_index[number] = 0
                    else:
                        self.current_number_index[number] = (self.current_number_index[number] + 1) % len(available_letters)
                    
                    letter = available_letters[self.current_number_index[number]]
                    self.current_training_letter = letter
                    count = self.training_count.get(letter, 0)
                    
                    # Show all available letters for this number
                    letters_str = " → ".join(available_letters)
                    print(f"\n🎯 Key {number}: {letters_str}")
                    print(f"   Now training: {letter} (Current samples: {count})")
                    print(f"💡 Press {number} again to cycle, or press ENTER to capture")
                
                # Warning if number key pressed while NOT in learning mode
                elif not self.learning_mode and (48 == key or (51 <= key <= 57)):
                    number = key - 48
                    if number not in [1, 2]:  # Don't warn for commands
                        print(f"\n⚠️  Key '{number}' pressed but NOT in training mode!")
                        print("💡 Press 1 to enter TRAINING MODE first")
                
                # Handle ENTER key to capture gesture in learning mode
                elif self.learning_mode and key == 13 and self.current_training_letter:  # ENTER key
                    if landmarks and self.detector.is_hand_stable:
                        # Load ML trainer if needed
                        if not self.ml_trainer_loaded:
                            self.load_ml_trainer()
                        
                        if self.ml_trainer_loaded:
                            # Get finger states
                            finger_states = self.detector.get_finger_states(landmarks)
                            
                            # Add training sample WITH finger states
                            success = self.ml_trainer.add_training_sample(
                                landmarks, 
                                self.current_training_letter,
                                finger_states=finger_states
                            )
                            
                            if success:
                                if self.current_training_letter not in self.training_count:
                                    self.training_count[self.current_training_letter] = 0
                                self.training_count[self.current_training_letter] += 1
                                count = self.training_count[self.current_training_letter]
                                
                                # IMPROVED PHOTO CAPTURE - Only hand region, no overlays
                                photo_saved = False
                                photo_path = None
                                
                                # Always show photo capture attempt
                                print(f"\n📸 Capturing photo for {self.current_training_letter}...")
                                if self.debug_mode:
                                    print(f"🔍 DEBUG: Starting photo capture for {self.current_training_letter}")
                                try:
                                    import os
                                    import datetime
                                    
                                    # Create training_photos directory if it doesn't exist
                                    photo_dir = "training_photos"
                                    if not os.path.exists(photo_dir):
                                        os.makedirs(photo_dir)
                                        if self.debug_mode:
                                            print(f"📁 Created directory: {photo_dir}")
                                    
                                    # Create letter-specific subdirectory
                                    letter_dir = os.path.join(photo_dir, self.current_training_letter)
                                    if not os.path.exists(letter_dir):
                                        os.makedirs(letter_dir)
                                        if self.debug_mode:
                                            print(f"📁 Created directory: {letter_dir}")
                                    
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: Directories created. Letter dir: {letter_dir}")
                                    
                                    # Generate timestamp filename
                                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                                    
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: Capturing fresh frame from camera...")
                                    # Capture a FRESH frame without overlays
                                    ret_clean, img_clean = cap.read()
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: Frame capture result: {ret_clean}, shape: {img_clean.shape if ret_clean else 'None'}")
                                    
                                    if not ret_clean or img_clean is None:
                                        raise ValueError("Failed to capture clean frame from camera")
                                    
                                    # Flip the frame
                                    img_clean = cv2.flip(img_clean, 1)
                                    h_img, w_img = img_clean.shape[:2]
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: Frame flipped. Size: {w_img}x{h_img}")
                                    
                                    # Extract hand bounding box from landmarks
                                    x_coords = [lm[1] for lm in landmarks]
                                    y_coords = [lm[2] for lm in landmarks]
                                    
                                    x_min = max(0, int(min(x_coords) * w_img) - 40)
                                    x_max = min(w_img, int(max(x_coords) * w_img) + 40)
                                    y_min = max(0, int(min(y_coords) * h_img) - 40)
                                    y_max = min(h_img, int(max(y_coords) * h_img) + 40)
                                    
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: Crop region: x[{x_min}:{x_max}], y[{y_min}:{y_max}]")
                                    
                                    # Validate coordinates
                                    if x_max <= x_min or y_max <= y_min:
                                        raise ValueError(f"Invalid crop coordinates: x[{x_min}:{x_max}], y[{y_min}:{y_max}]")
                                    
                                    # Crop to hand region
                                    hand_only = img_clean[y_min:y_max, x_min:x_max].copy()
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: Cropped hand image shape: {hand_only.shape}")
                                    
                                    # Validate crop is not empty
                                    if hand_only.size == 0:
                                        raise ValueError("Cropped region is empty")
                                    
                                    # Save hand-only photo
                                    filename_hand = os.path.join(letter_dir, f"{self.current_training_letter}_{count:03d}_{timestamp}_hand.jpg")
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: Attempting to save to: {filename_hand}")
                                    
                                    success_write = cv2.imwrite(filename_hand, hand_only)
                                    if self.debug_mode:
                                        print(f"🔍 DEBUG: cv2.imwrite result: {success_write}")
                                    
                                    if success_write:
                                        photo_saved = True
                                        photo_path = filename_hand
                                        print(f"📸 ✅ Photo saved successfully: {filename_hand}")
                                    else:
                                        raise ValueError("cv2.imwrite returned False")
                                    
                                except Exception as e:
                                    print(f"❌ Photo save failed with error: {e}")
                                    import traceback
                                    traceback.print_exc()
                                
                                # Save photo path to training sample
                                if photo_saved and self.ml_trainer_loaded:
                                    # Update the last sample with photo path
                                    if len(self.ml_trainer.training_data) > 0:
                                        self.ml_trainer.training_data[-1]['photo_path'] = photo_path
                                        self.ml_trainer.save_training_data()
                                
                                if photo_saved:
                                    print(f"✅ Captured! {self.current_training_letter}: {count} samples (photo + finger states saved)")
                                else:
                                    print(f"✅ Captured! {self.current_training_letter}: {count} samples (landmarks + finger states saved, photo failed)")
                                
                                self.play_sound('success')
                                
                                # Suggest when to train
                                if count == 15:
                                    print("💡 TIP: You have 15 samples - good time to train! Press M or B")
                            else:
                                print("❌ Failed to save sample")
                    else:
                        if not landmarks:
                            print("⚠️  No hand detected! Show your hand to the camera")
                        else:
                            print("⚠️  Hand not stable! Hold still and try again")
                
                elif key == ord('n') or key == ord('N'):
                    # Show ML training statistics
                    if not self.ml_trainer_loaded:
                        if not self.load_ml_trainer():
                            print("❌ Cannot show stats - ML trainer failed to load")
                            continue
                    
                    print("\n" + "=" * 60)
                    print("📊 ML TRAINING STATISTICS")
                    print("=" * 60)
                    stats = self.ml_trainer.get_statistics()
                    if stats:
                        print("Samples per letter:")
                        for letter, count in sorted(stats.items()):
                            bar = "█" * min(count, 50)
                            print(f"   {letter}: {count:3d} {bar}")
                        print(f"\n📦 Total samples: {len(self.ml_trainer.training_data)}")
                        print(f"🤖 ML enabled: {self.ml_enabled}")
                        if self.ml_trainer.model:
                            print("✅ Model trained and ready")
                        else:
                            print("⚠️  Model not trained yet (press 'M' to train)")
                    else:
                        print("📦 No training data collected yet")
                        print("💡 Press 'T' to enter learning mode and capture gestures")
                    print("=" * 60)
        
        # Cleanup
        try:
            if self.recording:
                self.stop_recording()
            
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
        
        # Final statistics
        print(f"\n✨ Session complete!")
        print("=" * 60)
        print("📊 FINAL STATISTICS")
        print("=" * 60)
        print(f"Session Letters: {self.letters_added}")
        print(f"Duration: {self.get_session_duration()}")
        print(f"Letters/Min: {self.get_letters_per_minute():.1f}")
        print("=" * 60)
        
        if self.current_text:
            print(f"📋 Translated text: {self.current_text}")
        else:
            print("📋 No text was translated in this session.")


def main():
    """Entry point for the application with error handling"""
    try:
        translator = ASLTranslator()
        translator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Ensure cleanup
        try:
            cv2.destroyAllWindows()
        except:
            pass


if __name__ == "__main__":
    main()
