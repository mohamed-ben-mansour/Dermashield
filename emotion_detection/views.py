import cv2
import numpy as np
import tensorflow as tf
from django.http import StreamingHttpResponse
from django.shortcuts import render
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load pre-trained emotion detection model and face cascade
model = tf.keras.models.load_model('emotion_detection/models/model_file_30epochs.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define emotion labels
emotion_labels = ['Angry','Disgust', 'Fear', 'Happy','Neutral','Sad','Surprise']

def preprocess_face(face_roi):
    """Preprocess the face region for the model."""
    resized = cv2.resize(face_roi, (48, 48))
    normalized = resized / 255.0
    return np.expand_dims(normalized, axis=(0, -1))

def predict_emotion(face_roi):
    """Predict emotion for a given face region."""
    processed_face = preprocess_face(face_roi)
    predictions = model.predict(processed_face)
    return emotion_labels[np.argmax(predictions)]

def gen_frames():
    """Generator function for reading frames, detecting emotions, and sending frames to the browser."""
    camera = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = camera.read()
            if not success:
                logging.error("Failed to capture frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                sub_face = gray[y:y+h, x:x+w]
                emotion_label = predict_emotion(sub_face)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()

def video_feed(request):
    """Stream video frames with emotion detection."""
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
def live_emotion_detection(request):
    """Render the HTML page for live emotion detection."""
    return render(request, 'emotion_detection/video_stream.html')
