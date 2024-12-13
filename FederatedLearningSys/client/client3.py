import requests
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

SERVER_URL = 'http://127.0.0.1:30001'  # Server endpoint

def preprocess_data(filepath):
    """
    Load and preprocess the dataset.
    """
    # Load dataset
    data = pd.read_csv(filepath)

    # Drop rows with missing or invalid values
    data = data.dropna()

    # Select relevant features and target
    X = data[['temp_max', 'temp_min']].values  # Features (2 features)
    y = data['precipitation'].values          # Target

    return X, y

def train_local_model(X, y):
    """
    Train a local Random Forest regression model.
    """
    model = RandomForestRegressor(n_estimators=10, random_state=42)  # Initialize Random Forest
    model.fit(X, y)  # Train model

    # For Random Forest, there are no explicit "weights" like in linear regression.
    # Instead, we can approximate feature importance as "weights" and set bias to 0.
    weights = model.feature_importances_  # Feature importance
    bias = 0  # Bias doesn't exist explicitly in Random Forest

    return weights, bias

def fetch_global_model():
    """
    Fetch the current global model from the server.
    """
    try:
        response = requests.get(f'{SERVER_URL}/get_model')
        response.raise_for_status()
        model = response.json()
        return np.array(model['weights']), model['bias']
    except requests.RequestException as e:
        print(f"Error fetching global model: {e}")
        exit()

def send_local_updates(weights, bias):
    """
    Send local updates to the server.
    """
    try:
        response = requests.post(f'{SERVER_URL}/submit_updates', json={
            'weights': weights.tolist(),
            'bias': bias
        })
        print(response.json())
    except requests.RequestException as e:
        print(f"Error sending updates: {e}")

if __name__ == '__main__':
    # Preprocess the data
    filepath = './FederatedLearningSys/client/michigan-weather.csv'  # Ensure this file path is correct
    X, y = preprocess_data(filepath)

    # Fetch global model (optional, for logging)
    global_weights, global_bias = fetch_global_model()
    print(f"Fetched global model: weights={global_weights}, bias={global_bias}")

    # Train locally using Random Forest
    local_weights, local_bias = train_local_model(X, y)
    print(f"Trained locally: weights={local_weights}, bias={local_bias}")

    # Send updates to server
    send_local_updates(local_weights, local_bias)
