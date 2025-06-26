from flask import Flask, request, jsonify
import os
from core.ob_detector import detect_order_block, extract_features, confirm_signal

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "✅ VIX75 OB API is live and ready!"})

@app.route('/signal', methods=['POST'])
def get_signal():
    data = request.json

    ob_signal = detect_order_block(data['ohlcv'])
    if not ob_signal:
        return jsonify({"signal": "none"})

    features = extract_features(ob_signal)
    if confirm_signal(features):
        return jsonify({
            "signal": ob_signal['type'],
            "confidence": ob_signal['score']
        })

    return jsonify({"signal": "filtered"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
