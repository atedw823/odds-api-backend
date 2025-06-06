from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ODDS_API_KEY = os.getenv("ODDS_API_KEY", "YOUR_API_KEY")
print(f"API KEY IN USE: {ODDS_API_KEY[:6]}...")  # Only first few characters
ODDS_BASE_URL = "https://api.the-odds-api.com/v4"

@app.route("/api/odds", methods=["GET"])
def get_odds():
    sport_key = request.args.get("sport", "basketball_nba")
    region = request.args.get("region", "us")
    market = request.args.get("market", "h2h")
    odds_format = request.args.get("odds_format", "american")

    url = f"{ODDS_BASE_URL}/sports/{sport_key}/odds/?apiKey={ODDS_API_KEY}&regions={region}&markets={market}&oddsFormat={odds_format}"
    response = requests.get(url)

    # Log quota info
    print("Quota Info (GET /api/odds):")
    print("Requests Remaining:", response.headers.get("x-requests-remaining"))
    print("Requests Used:", response.headers.get("x-requests-used"))

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        print("API Error:", response.status_code, response.text)
        return jsonify({"error": response.text}), response.status_code

@app.route("/list-sports", methods=["GET"])
def list_sports():
    url = f"{ODDS_BASE_URL}/sports/?apiKey={ODDS_API_KEY}"
    response = requests.get(url)

    # Log quota info
    print("Quota Info (GET /list-sports):")
    print("Requests Remaining:", response.headers.get("x-requests-remaining"))
    print("Requests Used:", response.headers.get("x-requests-used"))

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        print("API Error:", response.status_code, response.text)
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
