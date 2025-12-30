from flask import Flask, jsonify
from data_processing import load_and_compute_trend

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/health')
def health():
    return jsonify(status='ok')


@app.route('/api/insights')
def insights():
    result = load_and_compute_trend('data/sample_data.csv')
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
