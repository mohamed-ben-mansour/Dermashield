import os
import numpy as np
import pandas as pd
import h5py
import joblib
import tensorflow as tf
from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .forms import ImageUploadForm, CancerRiskForm

# Directory containing both CNN and RF models
MODELS_DIR = os.path.join(settings.BASE_DIR, 'model')
CNN_MODEL_FILE = 'model.h5'
RF_H5_FILE = 'pred.h5'
RF_JOBLIB_FILE = 'random_forest_model.joblib'

# Ensure models directory exists
if not os.path.isdir(MODELS_DIR):
    raise ImproperlyConfigured(f"Model directory not found: {MODELS_DIR}")

# # Load CNN model
# cnn_path = os.path.join(MODELS_DIR, CNN_MODEL_FILE)
# if not os.path.isfile(cnn_path):
#     raise ImproperlyConfigured(f"CNN model not found at: {cnn_path}")
# try:
#     cnn_model = tf.keras.models.load_model(cnn_path)
# except Exception as e:
#     raise ImproperlyConfigured(f"Error loading CNN model: {e}")

# Load or extract Random Forest model
rf_joblib_path = os.path.join(MODELS_DIR, RF_JOBLIB_FILE)
rf_h5_path = os.path.join(MODELS_DIR, RF_H5_FILE)

try:
    if os.path.isfile(rf_joblib_path):
        rf_model = joblib.load(rf_joblib_path)
    else:
        if not os.path.isfile(rf_h5_path):
            raise FileNotFoundError(f"RF H5 file not found at: {rf_h5_path}")
        with h5py.File(rf_h5_path, 'r') as h5f:
            if 'random_forest_model' not in h5f:
                raise KeyError("Key 'random_forest_model' missing in H5 file")
            data = h5f['random_forest_model'][()]
        # Save to joblib
        with open(rf_joblib_path, 'wb') as jf:
            jf.write(data)
        rf_model = joblib.load(rf_joblib_path)
except Exception as e:
    raise ImproperlyConfigured(f"Error loading RF model: {e}")

# # Image preprocessing for CNN
# def process_image(image_path):
#     img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
#     arr = tf.keras.preprocessing.image.img_to_array(img) / 255.0
#     return np.expand_dims(arr, axis=0)

# # View: Image Upload & CNN prediction
# def predict_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data['image']
#             image_path = os.path.join(settings.MEDIA_ROOT, image.name)
#             with open(image_path, 'wb+') as f:
#                 for chunk in image.chunks():
#                     f.write(chunk)

#             processed = process_image(image_path)
#             pred_val = cnn_model.predict(processed)[0][0]
#             result = 'Malignant Tumor' if pred_val > 0.5 else 'Benign Tumor'
#             os.remove(image_path)
#             return render(request, 'result.html', {'result': result})
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload.html', {'form': form})

# View: Cancer risk via Random Forest
def detect_cancer_risk(request):
    prediction = None
    if request.method == 'POST':
        form = CancerRiskForm(request.POST)
        if form.is_valid():
            df = pd.DataFrame([{
                'Age': form.cleaned_data['age'],
                'Family_History': int(form.cleaned_data['family_history']),
                'Genetic_Mutation': int(form.cleaned_data['genetic_mutation']),
                'UV_Exposure': int(form.cleaned_data['uv_exposure']),
            }])
            pred = rf_model.predict(df)[0]
            prediction = 'You are in danger' if pred == 1 else 'You are safe'
    else:
        form = CancerRiskForm()

    return render(request, 'detect.html', {'form': form, 'prediction': prediction})