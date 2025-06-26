from flask import Flask, request, jsonify
import os

# ✅ Keep using placeholder logic from core (if accessible locally)
try:
    from core.ob_detector import detect_order_block
except ImportError:
    # Use dummy fallback if core module not found
    def detect_order_block(ohlcv):
        return {"type": "buy", "score": 0.85}

app = Flask(__name__)

# ✅ New: Root check endpoint
@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "✅ VIX75 OB API is live and ready!"})

# ✅ Main signal handler
@app.route('/signal', methods=['POST'])
def get_signal():
    try:
        data = request.json

        if 'ohlcv' not in data:
            return jsonify({"error": "Missing 'ohlcv' key in JSON"}), 400

        ob_signal = detect_order_block(data['ohlcv'])
        if not ob_signal:
            return jsonify({"signal": "none"})

        return jsonify({
            "signal": ob_signal['type'],
            "confidence": ob_signal['score']
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

# ✅ Render-compatible runner
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
