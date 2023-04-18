from tflite_runtime.interpreter import Interpreter
from PIL import Image
import numpy as np
import time


class Model:
    def __init__(self, interpreter=Interpreter("model.tflite")):
        self.interpreter.allocate_tensors()
        
    def classifyImage(self, img):
        input_index = self.interpreter.get_input_details()[0]['index']
        output_index = self.interpreter.get_output_details()[0]['index']

        img = img.resize((100, 100))
        input_tensor = np.expand_dims(img, axis=0)
        self.interpreter.set_tensor(input_index, input_tensor)

        self.interpreter.invoke()

        prediction =  self.interpreter.get_tensor(output_index)[0]

        return prediction



