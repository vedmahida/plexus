"""
Flask integration service — legacy enterprise API gateway.
Handles OAuth2 token issuance and SOAP-to-REST bridging.
"""

import logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"service": "integration-service", "status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
