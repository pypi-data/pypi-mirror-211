from flask import Flask, request, jsonify
import dill
import numpy as np

app = Flask('app')

with open('./save/model.pickle', 'rb') as f:
    model = dill.load(f)


@app.route('/', methods=['GET'])
def home():
    return 'Simple Linear Regression'


@app.route('/stream', methods=['POST'])
def stream():
    """
    The func takes a payload of one record and return the prediction for that record.
    Examples:
        curl -X POST -H 'Content-Type: application/json' -d '[8]' http://127.0.0.1:5000/stream
    """
    input_data = request.get_json()
    try:
        input_data = np.array(input_data, dtype=np.float32)
    except Exception as e:
        return jsonify(f'{type(e).__name__}::{e}')
    if input_data.shape == (1,):
        input_data = np.array(input_data).reshape((-1, 1))
        prediction = model.predict(input_data)
        result = {'prediction': prediction.tolist()}
        return jsonify(result)
    return jsonify(f'Bad input shape! Expected shape: (1,). Received shape: {input_data.shape}.')


@app.route('/batch', methods=['POST'])
def batch():
    """
    The func takes an array of multiple records and return an array of predictions.
    Examples:
        curl -X POST -H 'Content-Type: application/json' -d '[[1],[2],[3],[4]]' http://127.0.0.1:5000/batch
    """
    input_data = request.get_json()
    try:
        input_data = np.array(input_data, dtype=np.float32)
    except Exception as e:
        return jsonify(f'{type(e).__name__}::{e}')
    if input_data.ndim == 2:
        if input_data.shape[1] == 1:
            predictions = model.predict(input_data)
            result = {'predictions': predictions.tolist()}
            return jsonify(result)
    return jsonify(f'Bad input shape! Expected shape: (batch_size, 1). Received shape: {input_data.shape}.')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # with open('save/model.pickle', 'rb') as f:
    #     model = pickle.load(f)
# else:
#     app.run()
