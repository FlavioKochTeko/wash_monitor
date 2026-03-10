power_history = []  # Liste zum vergleichen der Werte


def detect_phase(power):
    power_history.append(power)
    if len(power_history) > 10:  # Begrenzt die Liste auf 10 Werte
        power_history.pop(
            0
        )  # Entfernt das älteste Element, damit die Liste nicht zu lang wird

    if power > 1700:
        return "HEATING"

    elif 400 < power < 1000:
        return "SPIN"

    # Muster erkennenung: Wenn es 3 Peaks zwischen 80 und 200 gibt und mind. 3 Lows und Peaks, dann ist es die Waschphase
    peaks = sum(1 for p in power_history if 80 < p < 200)
    lows = sum(1 for p in power_history if p < 10)

    if peaks >= 3 and lows >= 3:
        return "WASH"

    # Wenn es keine 3 Peaks und Lows gibt ist es Spülphase
    elif 100 < power < 400:
        return "RINSE"

    elif 1 < power < 50:
        return "WATER_FILL"

    else:
        return "IDLE"
