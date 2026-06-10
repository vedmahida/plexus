"""
Flask integration service — legacy enterprise API gateway.
Handles OAuth2 token issuance and SOAP-to-REST bridging.
"""

import logging
from flask import Flask, jsonify, request
from oauth.provider import authenticate_user, create_access_token, create_refresh_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"service": "integration-service", "status": "healthy"})


@app.route("/oauth/token", methods=["POST"])
def token():
    """
    OAuth2 password grant endpoint.
    Issues access + refresh tokens for valid credentials.

    Request body:
        grant_type: 'password'
        username: user email
        password: user password

    Returns:
        JSON with access_token, refresh_token, token_type
    """
    data = request.get_json()

    # Validate grant type
    if not data or data.get("grant_type") != "password":
        return jsonify({"error": "unsupported_grant_type"}), 400

    user = authenticate_user(data.get("username", ""),
                             data.get("password", ""))

    # Validate credentials
    if not user:
        logger.warning(f"Failed auth attempt for {data.get('username')}")
        return jsonify({"error": "invalid_credentials"}), 401

    # Issue tokens
    access_token = create_access_token(user["email"], user["role"])
    refresh_token = create_refresh_token(user["email"])

    # Log
    logger.info(f"Token issued for {user['email']}")

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": 3600
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
