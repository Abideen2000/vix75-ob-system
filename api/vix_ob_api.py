
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/signal', methods=['POST'])
def get_signal():
    data = request.json
    ob_signal = detect_order_block(data['ohlcv'])
    if not ob_signal:
        return jsonify({"signal": "none"})
    features = extract_features(ob_signal)
    if confirm_signal(features):
        return jsonify({"signal": ob_signal['type'], "confidence": ob_signal['score']})
    return jsonify({"signal": "filtered"})
