import cv2
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models
import numpy as np
import json

model = models.load_model("manga_hq_classifier.keras")
class_names = ["classic", "manga"]

img=cv2.imread("input.jpg")
img=cv2.resize(img, (128,128))

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

prediction = model.predict(np.array([img]) / 255)
index = np.argmax(prediction)
p_dict = {}

for i, probability in enumerate(prediction[0]):
    try:
        print(f"Class: {class_names[i]}, Probability: {probability:.4f}")
        p_dict[f"{class_names[i]}"] = float(probability)
    except IndexError:
        pass

p_dict["prediction"] = class_names[index]

json.dump(p_dict, open(f"output.json", "w+"))                                                          
