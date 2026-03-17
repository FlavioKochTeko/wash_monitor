from datetime import datetime, timedelta


IDLE = "IDLE"
RUNNING = "RUNNING"
FINISHED = "FINISHED"
LOW_POWER = "LOW_POWER"

power_threshold = 1


def state_machine(
    power: float, state: str, start_time: datetime, low_power_start: datetime
) -> tuple:
    """Verwaltet den Zustand der Waschmaschine basierend auf dem Stromverbrauch.

    Args:
        power: Aktueller Stromverbrauch in Watt
        state: Aktueller Zustand (IDLE. RUNNING, LOW_POWER, FINISHED).
        start_time: Startzeitpunkt des Waschvorgangs.
        low_power_start: Zeitpunkt seit dem die Leistung niedrig ist.

    Returns:
        Tuple mit (state, start_time, low_power_start).
    """

    if state == IDLE and power > power_threshold:
        state = RUNNING
        start_time = datetime.now()
        print(f"Waschmaschine gestartet um {start_time.strftime('%H:%M:%S')}")

    elif state == RUNNING and power < power_threshold:
        state = LOW_POWER
        low_power_start = datetime.now()

    elif state == LOW_POWER:
        if power > power_threshold:
            state = RUNNING
            low_power_start = None

        elif low_power_start and datetime.now() - low_power_start > timedelta(
            seconds=5  # Fake Sensor: 5s - produktiv: 70s
        ):
            state = FINISHED
            print("Waschmaschine ist fertig")

    elif state == FINISHED and power < power_threshold:
        state = IDLE
        start_time = None
        low_power_start = None
        print("Reset")
    return state, start_time, low_power_start
