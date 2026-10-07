import json
import sys
from urllib import response
import requests
 
with open("credentials.json", "r", encoding="utf-8") as f:
    config = json.load(f)
 
# 1. OAuth-Token holen
try:
    token_response = requests.post(
        config["token_url"],
        data={
            "grant_type": "client_credentials",
            "scope": config["scope"],
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
        },
        timeout=30,
    )
except requests.RequestException as error:
    print("Verbindung zum Token-Endpunkt fehlgeschlagen:", error)
    sys.exit(1)
 
try:
    token_data = token_response.json()
except ValueError:
    print("Token-Antwort war kein JSON:", token_response.text[:1000])
    sys.exit(1)
 
if "access_token" not in token_data:
    print("Token konnte nicht abgerufen werden:")
    print(token_data.get("error"))
    print(token_data.get("error_description"))
    sys.exit(1)
 
print("Token erfolgreich erhalten.")
 
# 2. API mit Bearer-Token und Subscription Key aufrufen
url = config["api_base_url"].rstrip("/") + "/api/v2/marketTimes"
 
params = {
    "dateStart": "2026-10-10",
    "dateEnd":   "2026-10-11"
}
 
headers = {
    "Authorization": f"Bearer {token_data['access_token']}",
    "Ocp-Apim-Subscription-Key": config["api_subscription_key"],
    "Content-Type": "application/json",
    "Accept": "application/json"
}
 
try:
    response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30,
)
    print("API-HTTP-Status:", response.status_code)
    print(response.text[:2000])
 
except requests.RequestException as error:
    print("API-Aufruf fehlgeschlagen:", error)
 
customer_id = config["customer_id"]
url = f"{config['api_base_url'].rstrip('/')}/api/v2/products"
 
response = requests.get(url, headers=headers, timeout=30)
print("API-HTTP-Status:", response.status_code)
print(response.text[:3000])