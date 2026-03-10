# from get_power import get_power

from fake_sensor import FakeSensor  # Zum Testen mit einer CSV-Datei
from state_maschine import state_machine
from phase_detect import detect_phase
from learning_mode import LearningMode
from program_detect import detect_program
from datetime import datetime
import time

sensor = FakeSensor(
    "wash_monitor/Wash_data/60°wash(bett)_20260307-1348.csv"
)  # Zum Testen mit einer CSV-Datei

learning_mode = LearningMode()
# learning_mode.start_learning()

state = "IDLE"
start_time = None
low_power_start = None
phase_sequence = []
last_phase = None

try:
    while True:
        power = sensor.read()  # = sensor.read()  # = get_power()
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        if (
            power is None
        ):  # dieser if block löschen, wenn die get_power Funktion implementiert ist.
            print("Simulation fertig")
            break

        state, start_time, low_power_start = state_machine(
            power, state, start_time, low_power_start
        )
        phase = detect_phase(power)

        if phase != last_phase:
            phase_sequence.append((phase, time.time()))
            last_phase = phase

        print(f"{timestamp} - Power: {power} W, State: {state}, Phase: {phase}")

        learning_mode.record_phase(phase)

        if len(phase_sequence) >= 2:
            program = detect_program(phase_sequence)

            if program:
                print("Erkanntes Programm:", program["name"])

        if state == "FINISHED":
            learning_mode.stop_learning()

        time.sleep(5)
except KeyboardInterrupt:
    print("\nAufzeichnung beendet.")
