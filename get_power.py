from dotenv import load_dotenv
import os
import requests

load_dotenv()

HA_URL = os.getenv("HA_URL")
TOKEN = os.getenv("TOKEN")


headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def get_power() -> float:
    """Liest den aktuellen Stromverbauch der Waschmaschine aus Home Assistant

    Returns:
        Leistung in watt, oder 0 bei Fehlern
    """
    url = f"{HA_URL}/api/states/sensor.mystrom_device_leistung"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        power = float(response.json()["state"])
        return power

    except Exception as e:
        print("Fehler bei get_power:", e)
        return 0
