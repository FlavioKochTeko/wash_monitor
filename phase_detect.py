power_history: list = []


def detect_phase(power: float) -> str:
    """Analysiert den aktuellen Stromverbrauch und gibt die Waschphase zurück.

    Args:
        power: Aktueller Stromverbrauch in Watt.

    Returns:
        Name der erkannten Phase als String.
    """

    power_history.append(power)
    if len(power_history) > 10:
        power_history.pop(0)

    if power > 1700:
        return "HEATING"

    elif 400 < power < 1500:
        return "SPIN"

    peaks = sum(1 for p in power_history if 80 < p < 300)
    lows = sum(1 for p in power_history if p < 10)

    if peaks >= 3 and lows >= 3:
        return "WASH"

    elif 50 < power < 400:
        return "RINSE"

    elif 1 < power < 50:
        return "WATER_FILL"
