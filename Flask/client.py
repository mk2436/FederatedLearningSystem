import requests
import numpy as np

SERVER_URL = 'http://127.0.0.1:5000'  # Update with server address if needed

def train_local_model(X, y, weights, bias, learning_rate, epochs):
    """
    Train linear regression locally.
    """
    n_samples = X.shape[0]
    for _ in range(epochs):
        # Predictions
        y_pred = np.dot(X, weights) + bias
        # Compute gradients
        error = y_pred - y
        grad_weights = (1 / n_samples) * np.dot(X.T, error)
        grad_bias = (1 / n_samples) * np.sum(error)
        # Update weights and bias
        weights -= learning_rate * grad_weights
        bias -= learning_rate * grad_bias
    return weights, bias

def fetch_global_model():
    """
    Fetch the current global model from the server.
    """
    response = requests.get(f'{SERVER_URL}/get_model')
    model = response.json()
    return np.array(model['weights']), model['bias']

def send_local_updates(weights, bias):
    """
    Send local updates to the server.
    """
    response = requests.post(f'{SERVER_URL}/submit_updates', json={
        'weights': weights.tolist(),
        'bias': bias
    })
    print(response.json())

if __name__ == '__main__':
    # Simulated client dataset
    np.random.seed(42)
    X = np.random.rand(100, 2)  # 100 samples, 2 features
    y = np.random.rand(100)    # Target values

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
