print("INFO: Initializing System")
import copy
import csv
import os
import datetime
import time
import subprocess
import threading

import pyautogui
import cv2 as cv
import mediapipe as mp
from dotenv import load_dotenv


def speak_letter(letter):
    """Speak a letter using macOS 'say' command (runs in background thread)."""
    def _speak():
        try:
            subprocess.run(["say", letter], check=False)
        except Exception as e:
            print(f"WARNING: TTS failed: {e}")
    threading.Thread(target=_speak, daemon=True).start()


def switch_camera(current_device, cap, width, height, max_devices=5):
    """Try to switch to the next available camera device."""
    for i in range(1, max_devices + 1):
        next_device = (current_device + i) % max_devices
        cap.release()
        new_cap = cv.VideoCapture(next_device)
        if new_cap.isOpened():
            new_cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
            new_cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
            print(f"INFO: Switched to camera {next_device}")
            return new_cap, next_device
    # If no other camera found, reopen original
    cap = cv.VideoCapture(current_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    print(f"WARNING: No other camera found, staying on camera {current_device}")
    return cap, current_device

from slr.model.classifier import KeyPointClassifier

from slr.utils.args import get_args
from slr.utils.cvfpscalc import CvFpsCalc
from slr.utils.landmarks import draw_landmarks

from slr.utils.draw_debug import get_result_image
from slr.utils.draw_debug import get_fps_log_image
from slr.utils.draw_debug import draw_bounding_rect
from slr.utils.draw_debug import draw_hand_label
from slr.utils.draw_debug import show_fps_log
from slr.utils.draw_debug import show_result

from slr.utils.pre_process import calc_bounding_rect
from slr.utils.pre_process import calc_landmark_list
from slr.utils.pre_process import pre_process_landmark

from slr.utils.logging import log_keypoints
from slr.utils.logging import get_dict_form_list
from slr.utils.logging import get_mode



def main():
    try:
        #: -
        #: Getting all arguments
        load_dotenv()
        args = get_args()

        keypoint_file = "slr/model/keypoint.csv"
        counter_obj = get_dict_form_list(keypoint_file)

        #: cv Capture
        CAP_DEVICE = args.device
        CAP_WIDTH = args.width
        CAP_HEIGHT = args.height

        #: mp Hands
        # USE_STATIC_IMAGE_MODE = args.use_static_image_mode
        USE_STATIC_IMAGE_MODE = True
        MAX_NUM_HANDS = args.max_num_hands
        MIN_DETECTION_CONFIDENCE = args.min_detection_confidence
        MIN_TRACKING_CONFIDENCE = args.min_tracking_confidence

        #: Drawing Rectangle
        USE_BRECT = args.use_brect
        MODE = args.mode
        DEBUG = int(os.environ.get("DEBUG", "0")) == 1
        CAP_DEVICE = 0

        print("INFO: System initialization Successful")
        print("INFO: Opening Camera")

        #: -
        #: Capturing image
        cap = cv.VideoCapture(CAP_DEVICE)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            print("ERROR: Could not open camera device", CAP_DEVICE)
            print("ERROR: Please check if:")
            print("  1. Camera is connected")
            print("  2. Camera permissions are granted")
            print("  3. No other application is using the camera")
            return

        #: Background Image
        background_image = cv.imread("resources/background.png")
        if background_image is None:
            print("ERROR: Could not load background image: resources/background.png")
            cap.release()
            return

        #: -
        #: Setup hands
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=USE_STATIC_IMAGE_MODE,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

        #: -
        #: Load Model
        keypoint_classifier = KeyPointClassifier()

        #: Loading labels
        keypoint_labels_file = "slr/model/label.csv"
        with open(keypoint_labels_file, encoding="utf-8-sig") as f:
            key_points = csv.reader(f)
            keypoint_classifier_labels = [row[0] for row in key_points]

        #: Create ss directory if it doesn't exist
        os.makedirs("ss", exist_ok=True)

        #: -
        #: FPS Measurement
        cv_fps = CvFpsCalc(buffer_len=10)
        print("INFO: System is up & running")
        print("INFO: Press 'c' to switch camera, ESC to exit")
        
        #: -
        #: TTS state tracking (for reading letters aloud after 3 seconds)
        last_detected_letter = ""
        letter_start_time = None
        letter_spoken = False
        TTS_HOLD_DURATION = 3.0  # seconds to hold before speaking
        
        #: -
        #: Confidence threshold (0.0 to 1.0) - predictions below this are ignored
        CONFIDENCE_THRESHOLD = 0.7  # 70% confidence required
        
        #: -
        #: Main Loop Start Here...
        while True:
            #: FPS of open cv frame or window
            fps = cv_fps.get()

            #: -
            #: Setup Quit key for program
            key = cv.waitKey(1)
            if key == 27:  # ESC key
                print("INFO: Exiting...")
                break
            elif key == 57:  # 9
                name = datetime.datetime.now().strftime("%m%d%Y-%H%M%S")
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save(f'ss/{name}.png')
            elif key == ord('c') or key == ord('C'):  # 'c' to switch camera
                cap, CAP_DEVICE = switch_camera(CAP_DEVICE, cap, CAP_WIDTH, CAP_HEIGHT)

            #: -
            #: Camera capture
            success, image = cap.read()
            if not success:
                print("WARNING: Failed to read from camera")
                continue
            
            # Validate image dimensions
            if image is None or image.size == 0:
                print("WARNING: Invalid image from camera")
                continue
            
            image = cv.resize(image, (CAP_WIDTH, CAP_HEIGHT))
            
            #: Flip Image for mirror display
            image = cv.flip(image, 1)
            debug_image = copy.deepcopy(image)
            result_image = get_result_image()
            fps_log_image = get_fps_log_image()

            #: Converting to RBG from BGR
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = hands.process(image)  #: Hand's landmarks
            image.flags.writeable = True

            #: -
            #: DEBUG - Showing Debug info
            if DEBUG:
                MODE = get_mode(key, MODE)
                fps_log_image = show_fps_log(fps_log_image, fps)

            #: -
            #: Start Detection
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

                    #: Calculate  BoundingBox
                    use_brect = True
                    brect = calc_bounding_rect(debug_image, hand_landmarks)

                    #: Landmark calculation
                    landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                    #: Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = pre_process_landmark(landmark_list)

                    #: -
                    #: Checking if in Prediction Mode or in Logging Mode
                    #: If Prediction Mode it will predict the hand gesture
                    #: If in Logging Mode it will Log key-points or landmarks to the csv file

                    if MODE == 0:  #: Prediction Mode / Normal mode
                        #: Hand sign classification with confidence
                        hand_sign_id, confidence = keypoint_classifier(
                            pre_processed_landmark_list, 
                            confidence_threshold=CONFIDENCE_THRESHOLD
                        )

                        if hand_sign_id == 25:
                            hand_sign_text = ""
                            confidence_text = ""
                        else:
                            hand_sign_text = keypoint_classifier_labels[hand_sign_id]
                            confidence_text = f"{confidence * 100:.1f}%"

                        #: -
                        #: TTS: Speak letter after holding same sign for 3 seconds
                        if hand_sign_text != "":
                            if hand_sign_text == last_detected_letter:
                                # Same letter detected, check if 3 seconds have passed
                                if letter_start_time is not None and not letter_spoken:
                                    elapsed = time.time() - letter_start_time
                                    if elapsed >= TTS_HOLD_DURATION:
                                        speak_letter(hand_sign_text)
                                        letter_spoken = True
                                        print(f"INFO: Speaking letter '{hand_sign_text}'")
                            else:
                                # New letter detected, reset timer
                                last_detected_letter = hand_sign_text
                                letter_start_time = time.time()
                                letter_spoken = False
                        else:
                            # No letter detected, reset
                            last_detected_letter = ""
                            letter_start_time = None
                            letter_spoken = False

                        #: Showing Result with confidence
                        result_image = show_result(result_image, handedness, hand_sign_text, confidence_text)

                    elif MODE == 1:  #: Logging Mode
                        log_keypoints(key, pre_processed_landmark_list, counter_obj, data_limit=1000)

                    #: -
                    #: Drawing debug info
                    debug_image = draw_bounding_rect(debug_image, use_brect, brect)
                    debug_image = draw_landmarks(debug_image, landmark_list)
                    debug_image = draw_hand_label(debug_image, brect, handedness)

            #: -
            #: Set main video footage on Background
            
            background_image[170:170 + 480, 50:50 + 640] = debug_image
            background_image[240:240 + 127, 731:731 + 299] = result_image
            background_image[678:678 + 30, 118:118 + 640] = fps_log_image

            # cv.imshow("Result", result_image)
            # cv.imshow("Main Frame", debug_image)
            
            try:
                cv.imshow("Sign Language Recognition", background_image)
            except Exception as e:
                print(f"ERROR: Failed to display window: {e}")
                break

    except KeyboardInterrupt:
        print("\nINFO: Interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            cap.release()
            cv.destroyAllWindows()
            print("INFO: Bye")
        except:
            pass


if __name__ == "__main__":
    main()
