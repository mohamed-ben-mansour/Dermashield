from django.shortcuts import render

# Create your views here.
import tensorflow as tf

import os
import numpy as np
from django.shortcuts import render
from django.conf import settings

from .forms import ImageUploadForm


#5dmet amine

# # Recreate the architecture of the CNN model
# img_height, img_width, num_classes = 180, 180, 9

# model = tf.keras.models.Sequential([
#     # Rescaling Layer
#     tf.keras.layers.Rescaling(1.0 / 255, input_shape=(img_height, img_width, 3)),
#     # Convolutional and Pooling Layers
#     tf.keras.layers.Conv2D(32, 3, padding="same", activation='relu'),
#     tf.keras.layers.MaxPool2D(),
#     tf.keras.layers.Conv2D(64, 3, padding="same", activation='relu'),
#     tf.keras.layers.MaxPool2D(),
#     tf.keras.layers.Conv2D(128, 3, padding="same", activation='relu'),
#     tf.keras.layers.MaxPool2D(),
#     tf.keras.layers.Dropout(0.15),
#     tf.keras.layers.Conv2D(256, 3, padding="same", activation='relu'),
#     tf.keras.layers.MaxPool2D(),
#     tf.keras.layers.Dropout(0.20),
#     tf.keras.layers.Conv2D(512, 3, padding="same", activation='relu'),
#     tf.keras.layers.MaxPool2D(),
#     tf.keras.layers.Dropout(0.25),
#     # Flatten and Dense Layers
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(1024, activation="relu"),
#     tf.keras.layers.Dense(num_classes, activation='softmax'),
# ])

# # Compile the model
# opt = tf.keras.optimizers.Adam(learning_rate=0.001)
# model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Load weights into the model
# weights_path = os.path.join(settings.BASE_DIR, 'D:\\gl_detection\\cnn_fc_model.h5')
# model.load_weights(weights_path)
# print("Model weights loaded successfully!")

# def process_image(image_path):
#     """Preprocess the image for the CNN model."""
#     img = tf.keras.preprocessing.image.load_img(image_path, target_size=(img_height, img_width))  # Resize to match the model's input shape
#     img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0  # Normalize pixel values
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     return img_array

# def predict_image(request):
#     """Handle image upload and prediction."""
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the uploaded image to a temporary location
#             image = form.cleaned_data['image']
#             image_path = os.path.join(settings.MEDIA_ROOT, image.name)
#             with open(image_path, 'wb+') as f:
#                 for chunk in image.chunks():
#                     f.write(chunk)

#             # Process the image and make a prediction
#             processed_image = process_image(image_path)
#             predictions = model.predict(processed_image)  # Model output: probabilities for 9 classes
#             predicted_class = np.argmax(predictions, axis=1)[0]  # Get the index of the highest probability
            
#             # Map the predicted class index to the actual class name
#             class_names = ['Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'Class7', 'Class8', 'Class9']  # Update with your actual class names
#             result = class_names[predicted_class]

#             # Clean up the temporary file
#             os.remove(image_path)

#             return render(request, 'result.html', {'result': result})
#     else:
#         form = ImageUploadForm()

#     return render(request, 'upload.html', {'form': form})



<<<<<<< HEAD
# Load your CNN model (once when the server starts)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'D:\\gl_detection\\model.h5')
model = tf.keras.models.load_model(MODEL_PATH)

def process_image(image_path):
    """Preprocess the image for the CNN model."""
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))  # Adjust size as per your model
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0  # Normalize the image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
=======
# # Load your CNN model (once when the server starts)
# MODEL_PATH = os.path.join(settings.BASE_DIR, 'D:\\gl_detection\\model.h5')
# model = tf.keras.models.load_model(MODEL_PATH)

# def process_image(image_path):
#     """Preprocess the image for the CNN model."""
#     img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))  # Adjust size as per your model
#     img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0  # Normalize the image
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     return img_array

# def predict_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the uploaded image to a temporary location
#             image = form.cleaned_data['image']
#             image_path = os.path.join(settings.MEDIA_ROOT, image.name)
#             with open(image_path, 'wb+') as f:
#                 for chunk in image.chunks():
#                     f.write(chunk)
            
#             # Process the image and get prediction
#             processed_image = process_image(image_path)
#             prediction = model.predict(processed_image)[0][0]  # Get the single output value

#             # Classify the result
#             if prediction > 0.5:
#                 result = "Malignant Tumor"
#             else:
#                 result = "Benign Tumor"
            
#             # Clean up the temporary file
#             os.remove(image_path)
            
#             return render(request, 'result.html', {'result': result})
#     else:
#         form = ImageUploadForm()

#     return render(request, 'upload.html', {'form': form})





# import os
# import pandas as pd
# import h5py
# import joblib
# from django.shortcuts import render
# from .forms import CancerRiskForm

# # Step 1: Load the model when the server starts
# h5_file_path = 'D:\\gl_prediction\\pred.h5'
# joblib_file_path = 'D:\\gl_prediction\\random_forest_model.joblib'  # Temporary file path

# # Extract the model from the .h5 file
# with h5py.File(h5_file_path, "r") as h5f:
#     if "random_forest_model" in h5f:
#         model_data = h5f["random_forest_model"][()]  # Extract binary data
#         with open(joblib_file_path, "wb") as f:
#             f.write(model_data)
#     else:
#         raise KeyError("Key 'random_forest_model' not found in the .h5 file")

# # Load the model with joblib
# model1 = joblib.load(joblib_file_path)
# print("Model loaded successfully!")

# # Step 2: Define the prediction logic
# def detect_cancer_risk(request):
#     prediction = None
#     if request.method == 'POST':
#         form = CancerRiskForm(request.POST)
#         if form.is_valid():
#             # Extract form data
#             age = form.cleaned_data['age']
#             family_history = int(form.cleaned_data['family_history'])
#             genetic_mutation = int(form.cleaned_data['genetic_mutation'])
#             uv_exposure = int(form.cleaned_data['uv_exposure'])

#             # Prepare data for prediction
#             input_data = pd.DataFrame([{
#                 'Age': age,
#                 'Family_History': family_history,
#                 'Genetic_Mutation': genetic_mutation,
#                 'UV_Exposure': uv_exposure
#             }])

#             # Make prediction
#             prediction = model1.predict(input_data)[0]
#             prediction = "You are in danger" if prediction == 1 else "You are safe"
#     else:
#         form = CancerRiskForm()

#     return render(request, 'detect.html', {'form': form, 'prediction': prediction})
from django.shortcuts import render
import tensorflow as tf
import os
import numpy as np
from django.conf import settings
from .forms import ImageUploadForm, CancerRiskForm
import pandas as pd
import h5py
import joblib

# --- CNN MODEL SECTION ---

# BROKEN: Actual model file not found. Replace 'dummy_model_path.h5' with the real path later.
# MODEL_PATH = os.path.join(settings.BASE_DIR, 'D:\\gl_detection\\model.h5')
# model = tf.keras.models.load_model(MODEL_PATH)

# Dummy placeholder logic
def dummy_cnn_predict(processed_image):
    # Simulate prediction result for testing
    return np.array([[0.7]])  # Change this value to test different outputs

def process_image(image_path):
    """Preprocess the image for the CNN model."""
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
>>>>>>> main
    return img_array

def predict_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
<<<<<<< HEAD
            # Save the uploaded image to a temporary location
=======
>>>>>>> main
            image = form.cleaned_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(image_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
<<<<<<< HEAD
            
            # Process the image and get prediction
            processed_image = process_image(image_path)
            prediction = model.predict(processed_image)[0][0]  # Get the single output value

            # Classify the result
=======

            processed_image = process_image(image_path)

            # BROKEN: Actual prediction using model is disabled
            # prediction = model.predict(processed_image)[0][0]

            # DUMMY prediction used instead
            prediction = dummy_cnn_predict(processed_image)[0][0]

>>>>>>> main
            if prediction > 0.5:
                result = "Malignant Tumor"
            else:
                result = "Benign Tumor"
<<<<<<< HEAD
            
            # Clean up the temporary file
            os.remove(image_path)
            
=======

            os.remove(image_path)

>>>>>>> main
            return render(request, 'result.html', {'result': result})
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})


<<<<<<< HEAD



import os
import pandas as pd
import h5py
import joblib
from django.shortcuts import render
from .forms import CancerRiskForm

# Step 1: Load the model when the server starts
h5_file_path = 'D:\\gl_prediction\\pred.h5'
joblib_file_path = 'D:\\gl_prediction\\random_forest_model.joblib'  # Temporary file path

# Extract the model from the .h5 file
with h5py.File(h5_file_path, "r") as h5f:
    if "random_forest_model" in h5f:
        model_data = h5f["random_forest_model"][()]  # Extract binary data
        with open(joblib_file_path, "wb") as f:
            f.write(model_data)
    else:
        raise KeyError("Key 'random_forest_model' not found in the .h5 file")

# Load the model with joblib
model1 = joblib.load(joblib_file_path)
print("Model loaded successfully!")

# Step 2: Define the prediction logic
=======
# --- CANCER RISK PREDICTION SECTION ---

# BROKEN: Model file 'pred.h5' is missing. Replace with actual file later.
# h5_file_path = 'D:\\gl_prediction\\pred.h5'
# joblib_file_path = 'D:\\gl_prediction\\random_forest_model.joblib'
# with h5py.File(h5_file_path, "r") as h5f:
#     if "random_forest_model" in h5f:
#         model_data = h5f["random_forest_model"][()]
#         with open(joblib_file_path, "wb") as f:
#             f.write(model_data)
#     else:
#         raise KeyError("Key 'random_forest_model' not found in the .h5 file")
# model1 = joblib.load(joblib_file_path)

# DUMMY model prediction logic
def dummy_risk_predict(input_df):
    # Simulate a binary classifier output
    return [1]  # Change to [0] for "You are safe"

>>>>>>> main
def detect_cancer_risk(request):
    prediction = None
    if request.method == 'POST':
        form = CancerRiskForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            # Extract form data
=======
>>>>>>> main
            age = form.cleaned_data['age']
            family_history = int(form.cleaned_data['family_history'])
            genetic_mutation = int(form.cleaned_data['genetic_mutation'])
            uv_exposure = int(form.cleaned_data['uv_exposure'])

<<<<<<< HEAD
            # Prepare data for prediction
=======
>>>>>>> main
            input_data = pd.DataFrame([{
                'Age': age,
                'Family_History': family_history,
                'Genetic_Mutation': genetic_mutation,
                'UV_Exposure': uv_exposure
            }])

<<<<<<< HEAD
            # Make prediction
            prediction = model1.predict(input_data)[0]
=======
            # BROKEN: real model prediction temporarily disabled
            # prediction = model1.predict(input_data)[0]

            # DUMMY prediction instead
            prediction = dummy_risk_predict(input_data)[0]

>>>>>>> main
            prediction = "You are in danger" if prediction == 1 else "You are safe"
    else:
        form = CancerRiskForm()

    return render(request, 'detect.html', {'form': form, 'prediction': prediction})
