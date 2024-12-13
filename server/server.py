from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Global model parameters
global_weights = np.zeros(2)  # Example: 2 features
global_bias = 0.0
clients_updates = []

@app.route('/get_model', methods=['GET'])
def get_model():
    """
    Endpoint for clients to fetch the current global model.
    """
    return jsonify({
        'weights': global_weights.tolist(),
        'bias': global_bias
    })

@app.route('/submit_updates', methods=['POST'])
def submit_updates():
    """
    Endpoint for clients to send their updates to the server.
    """
    global clients_updates
    data = request.json
    weights = np.array(data['weights'])
    bias = data['bias']
    clients_updates.append((weights, bias))
    return jsonify({'message': 'Updates received successfully!'})

@app.route('/aggregate', methods=['POST'])
def aggregate():
    """
    Aggregates updates from clients and updates the global model.
    """
    global global_weights, global_bias, clients_updates

    if not clients_updates:
        return jsonify({'message': 'No updates to aggregate!'})

    # Aggregation (Federated Averaging)
    aggregated_weights = np.mean([update[0] for update in clients_updates], axis=0)
    aggregated_bias = np.mean([update[1] for update in clients_updates])

    # Update global model
    global_weights = aggregated_weights
    global_bias = aggregated_bias

    # Clear client updates
    clients_updates = []
    return jsonify({
        'message': 'Global model updated!',
        'weights': global_weights.tolist(),
        'bias': global_bias
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
