from dotenv import load_dotenv
import os
import requests

load_dotenv()

# IP meiner HA wird von der .env Datei importiert
HA_URL = os.getenv("HA_URL")

# dauerhafter Zugangsschlüssel wird von der .env Datei importiert
TOKEN = os.getenv("TOKEN")


# Berechtigung einholen für den Zugriff auf die Daten
headers = {
    "Authorization": f"Bearer {TOKEN}",  # Authorization: sagt HA "Bin Berechtigt" / Bearer: ist Standard Format für API-Aut
    "Content-Type": "application/json",  # mit welcher Datei wir arbeiten (JSON)
}


def get_power():
    # Das ist der API Endpunkt für meinen Sensor
    url = f"{HA_URL}/api/states/sensor.mystrom_device_leistung"
    try:
        # fragt nach dem aktuellen Zustand des Sensors
        response = requests.get(url, headers=headers)
        # Überprüft Fehler (Token, Sensor, HA Offline)
        response.raise_for_status()

        # HA antwortet mit JSON so lesen wir es
        data = response.json()

        # so wandeln wir state im JSON file in eine Zahl um
        power = float(data["state"])

        # gibt die Leistung zurück
        return power

    # Werden die Fehler abgefangen, wird eine Fehlermeldung ausgegeben und 0 zurückgegeben.
    except Exception as e:
        print("Fehler bei get_power:", e)

        # Damit trotzdem ein wert bei Fehlern zurückgegeben wird.
        return 0
