import requests  # Kommunikation mit HA über HTTP
import time  # damit machen wir pausen
from datetime import datetime  # für den Zeitstempel
from dotenv import load_dotenv
import os  # zugangsdaten lesen von der .env Datei

load_dotenv()

# IP und Token Geheimhalten!!!

HA_URL = os.getenv("HA_URL")
# IP meiner HA wird von der .env Datei importiert

TOKEN = os.getenv("TOKEN")
# dauerhafter Zugangsschlüssel wird von der .env Datei importiert

# damit sind wir berechtigt auf die Daten zuzugreifen
headers = {
    "Authorization": f"Bearer {TOKEN}",  # Authorization: sagt HA "Bin Berechtigt" / Bearer: ist Standard Format für API-Aut
    "Content-Type": "application/json",  # mit welcher Datei wir arbeiten (JSON)
}


def get_power():
    url = f"{HA_URL}/api/states/sensor.mystrom_device_leistung"  # Das ist der API Endpunkt für meinen Sensor
    response = requests.get(
        url, headers=headers
    )  # fragt nach dem aktuellen Zustand des Sensors
    response.raise_for_status()  # Überprüft Fehler (Token, Sensor, HA Offline)
    data = response.json()  # HA antwortet mit JSON so lesen wir es
    return float(data["state"])  # so wandeln wir state im JSON file in eine Zahl um


filename = f"wash_{datetime.now().strftime('%Y%m%d-%H%M')}.csv"  # Dateiname

with open(filename, "w") as f:  # Datei öffnen und schliessen
    f.write(
        "Datum      Zeit    ; Leistung\n"
    )  # kopfzeile erstellen \n ist zeilenumbruch

try:
    while True:
        power = get_power()
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        with open(filename, "a") as f:
            f.write(f"{timestamp}; {power}\n")

        print(f"{timestamp} - {power} W")  # Ausgabe akuelle Leistung
        time.sleep(5)
except KeyboardInterrupt:
    print("\nAufzeichnung beendet.")


#   *INFO*
# print(f".....")       = Variable direkt in den Text einfügen
# .raise_for_status()   = kommt von import request
# Exception             = sind alle Fehler gemeint (ValueError, TypeError, HTTPError,...)
# with                  = öffne etwas und räume automatisch wieder auf = datei öffnet und schliesst sich wieder
# \n                    = erstellt einen zeilenumbruch
