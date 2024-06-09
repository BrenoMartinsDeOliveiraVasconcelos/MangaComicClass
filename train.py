import cv2
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models
import numpy as np
import os

# Define paths to your image folders for training and testing data
train_data_path = "data/training"
test_data_path = "data/testing"
class_names = ["classic", "manga"]

# Initialize empty lists for images and labels
training_images = []
training_labels = []
testing_images = []
testing_labels = []

# Loop through training folders and images
for class_name in os.listdir(train_data_path):
  class_path = os.path.join(train_data_path, class_name)
  files = os.listdir(class_path)
  index = 0
  for img_file in files:
    index += 1
    print(f"({index}/{len(files)}) classe: {class_name}")
    img = cv2.imread(os.path.join(class_path, img_file))
    # Preprocess your image here (resize, normalization etc.)
    if img is not None:
      img = cv2.resize(img, (128, 128))
      img = img / 255.0  # Normalize pixel values
      training_images.append(img)
      training_labels.append(class_names.index(class_name))  # Assuming you have a class_names list for your categories

# Do similar loop for test data
# Loop through testing folders and images
for class_name in os.listdir(test_data_path):
  class_path = os.path.join(test_data_path, class_name)
  files = os.listdir(class_path)
  index = 0
  for img_file in files:
    index += 1
    print(f"({index}/{len(files)}) classe: {class_name}")
    img = cv2.imread(os.path.join(class_path, img_file))
    # Preprocess your image here (resize, normalization etc.)
    if img is not None:
      img = cv2.resize(img, (128, 128))
      img = img / 255.0  # Normalize pixel values
      testing_images.append(img)
      testing_labels.append(class_names.index(class_name))  # Assuming you have a class_names list for your categories
    else:
      pass


# Convert data to numpy arrays
training_images = np.array(training_images)
training_labels = np.array(training_labels)
testing_images = np.array(testing_images)
testing_labels = np.array(testing_labels)
for i in range(16):
    plt.subplot(4,4,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(training_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[training_labels[i]])


training_images = training_images[:]
training_labels = training_labels[:]
testing_images = testing_images[:]
testing_labels = testing_labels[:]




model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))



model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))

loss, accuracy = model.evaluate(testing_images, testing_labels)
print(f"LOSS: {loss}\nACCURACY: {accuracy}")

model.save("manga_hq_classifier.keras")

