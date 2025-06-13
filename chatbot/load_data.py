# chatbot/load_data.py
import pandas as pd
import os

def load_medical_data():
    # Path to the dataset (adjust this based on where you stored it)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'Medical_Intelligence_Dataset (1).csv')

    df = pd.read_csv(dataset_path)
    return df[['input', 'output']]  # Extract relevant columns
