import requests
import numpy as np
import pandas as pd

SERVER_URL = 'http://127.0.0.1:30001'  # Server endpoint

def preprocess_data(filepath):
    """
    Load and preprocess the dataset.
    """
    # Load dataset
    data = pd.read_csv(filepath)

    # Drop rows with missing or invalid values
    data = data.dropna()

    # Example preprocessing: select relevant features and target
    X = data[['temp_max', 'temp_min']].values  # Features (2 features)
    y = data['precipitation'].values          # Target

    # Check for constant features (zero std deviation)
    std_devs = np.std(X, axis=0)
    if np.any(std_devs == 0):
        raise ValueError("One or more features have zero variance!")

    # Normalize features for stability
    X = (X - np.mean(X, axis=0)) / std_devs

    return X, y

def train_local_model(X, y, weights, bias, learning_rate, epochs):
    """
    Train a local linear regression model using gradient descent.
    """
    n_samples = X.shape[0]
    for epoch in range(epochs):
        # Predictions
        y_pred = np.dot(X, weights) + bias
        # Compute gradients
        error = y_pred - y
        grad_weights = (1 / n_samples) * np.dot(X.T, error)
        grad_bias = (1 / n_samples) * np.sum(error)

        # Check for NaN or inf gradients
        if np.isnan(grad_weights).any() or np.isnan(grad_bias) or np.isinf(grad_weights).any() or np.isinf(grad_bias):
            print("Numerical instability detected! Stopping training.")
            break

        # Update weights and bias
        weights -= learning_rate * grad_weights
        bias -= learning_rate * grad_bias

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
    filepath = './client/houston-weather.csv'  # Ensure this file path is correct
    X, y = preprocess_data(filepath)

    # Hyperparameters
    learning_rate = 0.01
    epochs = 10

    # Fetch global model
    global_weights, global_bias = fetch_global_model()
    print(f"Fetched global model: weights={global_weights}, bias={global_bias}")

    # Train locally
    local_weights, local_bias = train_local_model(X, y, global_weights, global_bias, learning_rate, epochs)
    print(f"Trained locally: weights={local_weights}, bias={local_bias}")

    # Send updates to server
    send_local_updates(local_weights, local_bias)
