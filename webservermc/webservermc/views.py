from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from os import path as p

realpath = Path(__file__).resolve().parent.parent.parent
upath = p.join(realpath, "webservermc", 'uploads')
fs = FileSystemStorage()

def home(request):
    context = {
        'title': 'Welcome to Our Website!',
    }
    return render(request, 'home.html', context)


@csrf_exempt
def upload(request: WSGIRequest):
    print(f"got request {request}")

    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # Get the image type
            image_type = file.content_type.split('/')[1]
            print(f"Image type: {image_type}")

            # Generate a unique filename (optional)
            filename = f"{file.name}.{image_type}"

            # Define the upload path (modify as needed)
            upload_path = p.join(realpath, "webservermc", 'uploads', filename)

            # Save the image to the specified path
            with open(upload_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Read the image!
            im = Image.open(upload_path)
            im32 = im.resize((128, 128))
            im32 = im32.convert('RGB')

            h = (im.size[0]/im.size[1]) * 300

            im = im.resize((int(h), 300))
            im.save(upload_path)

            # Load the model
            model_path = p.join(realpath, "manga_hq_classifier.keras")

            model = models.load_model(model_path)
            class_names = ["classic", "manga"]

            prediction = model.predict(np.array([im32]) / 255)
            index = np.argmax(prediction)
            p_dict = {}

            for i, probability in enumerate(prediction[0]):
                try:
                    print(f"Class: {class_names[i]}, Probability: {probability:.4f}")
                    p_dict[f"{class_names[i]}"] = float(probability)
                except IndexError:
                    pass

            p_dict["prediction"] = class_names[index]

            textstr = ""

            for k, v in p_dict.items():
                if k != "prediction":
                    v = "{:.4f}".format(v)

                textstr += f"{k} = {v}\n"

            return HttpResponse(textstr+f"\nPATH={fs.url(filename)}")
