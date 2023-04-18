from tflite_runtime.interpreter import Interpreter
from PIL import Image
import numpy as np
import time


class Model:
    interpreter=None
    def __init__(self):
        global interpreter
        interpreter = Interpreter(model_path='model.tflite')
        interpreter.allocate_tensors()
        
    def classifyImage(self, img):
        global interpreter
        input_index = interpreter.get_input_details()[0]['index']
        output_index = interpreter.get_output_details()[0]['index']

        img = img.resize((100, 100))
        img_array = np.asarray(img)
        input_tensor = np.expand_dims(img_array, 0)
    
        interpreter.set_tensor(input_index, input_tensor)

        interpreter.invoke()

        prediction =  interpreter.get_tensor(output_index)[0]

        return prediction


