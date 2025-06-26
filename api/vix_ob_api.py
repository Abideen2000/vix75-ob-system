from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/signal', methods=['POST'])
def get_signal():
    data = request.json

    # Placeholder: you must import these from your core/ directory
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

# ✅ Render-compatible runner
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
