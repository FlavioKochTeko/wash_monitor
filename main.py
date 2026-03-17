from get_power import get_power
from fake_sensor import FakeSensor
from state_maschine import state_machine
from phase_detect import detect_phase
from learning_mode import LearningMode
from program_detect import detect_program
from datetime import datetime
import time

sensor = FakeSensor("Wash_data/60°wash(bett)_20260307-1348.csv")  #

learning_mode = LearningMode()
# Lernmodus (deaktiviert)
# learning_mode.start_learning()

state = "IDLE"
start_time = None
low_power_start = None
phase_sequence = []
last_phase = None
last_phase_time = time.time()

try:
    while True:
        power = sensor.read()  # Fake Sensor: sensor.read() - produktiv: get_power()
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Fake Sensor: None signalisiert Ende der CSV Datei
        if power is None:
            print("Simulation fertig")
            break

        state, start_time, low_power_start = state_machine(
            power, state, start_time, low_power_start
        )
        phase = detect_phase(power)

        if phase != last_phase:
            duration = time.time() - last_phase_time
            phase_sequence.append([phase, duration])
            last_phase = phase
            last_phase_time = time.time()

        print(f"{timestamp} - Power: {power} W, State: {state}, Phase: {phase}")

        learning_mode.record_phase(phase)

        if len(phase_sequence) >= 2:
            program = detect_program(phase_sequence)
            if program:
                print("Erkanntes Programm:", program["name"])

        if state == "FINISHED" and learning_mode.learning_active:
            learning_mode.stop_learning()

        time.sleep(0)  # Fake Sensor: 0s - produktiv: 5s
except KeyboardInterrupt:
    print("\nAufzeichnung beendet.")
