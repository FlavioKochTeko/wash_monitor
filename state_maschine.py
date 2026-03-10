from datetime import datetime, timedelta


IDLE = "IDLE"
RUNNING = "RUNNING"
FINISHED = "FINISHED"
LOW_POWER = "LOW_POWER"

power_threshold = 1

state = IDLE
start_time = None
low_power_start = None


def state_machine(power, state, start_time, low_power_start):

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
            seconds=70  # =5
        ):
            state = FINISHED
            print("Waschmaschine ist fertig")

        elif state == FINISHED and power < power_threshold:
            state = IDLE
            start_time = None
            low_power_start = None
            print("Reset")
    return state, start_time, low_power_start
