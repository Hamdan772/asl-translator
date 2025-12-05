import numpy as np
import tensorflow as tf


class KeyPointClassifier(object):
    def __init__(
        self,
        model_path='slr/model/slr_model.tflite',
        num_threads=1,
    ):
        #: Initializing tensor interpreter
        self.interpreter = tf.lite.Interpreter(
            model_path=model_path,
            num_threads=num_threads
        )
        self.interpreter.allocate_tensors()

        #: Input Output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(self, landmark_list, confidence_threshold=0.7):
        """
        Classify hand landmarks and return prediction with confidence.
        
        :param landmark_list: Pre-processed landmark coordinates
        :param confidence_threshold: Minimum confidence to accept prediction (0.0-1.0)
        :return: Tuple of (class_index, confidence) or (25, 0.0) if below threshold
        """
        input_details_tensor_index = self.input_details[0]['index']

        #: Feeding landmarks to the tensor interpreter
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32)
        )

        #: Invoking interpreter for prediction
        self.interpreter.invoke()

        #: Getting tensor index from output details
        output_details_tensor_index = self.output_details[0]['index']

        #: Getting all the prediction probabilities
        result = self.interpreter.get_tensor(output_details_tensor_index)
        probabilities = np.squeeze(result)
        
        #: Get the highest confidence and its index
        confidence = float(np.max(probabilities))
        result_index = int(np.argmax(probabilities))
        
        #: Only return valid prediction if above threshold
        if confidence >= confidence_threshold:
            return result_index, confidence
        else:
            return 25, confidence
            
