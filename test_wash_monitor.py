from phase_detect import detect_phase
from state_maschine import state_machine


"""Test für die Waschphasen-Erkennung"""

detector = detect_phase

print(detector(2000))  # T1 Erwartet: HEATING
print(detector(800))  # T2 Erwartet: SPIN
print(detector(20))  # T3 Erwartet: WATER_FILL
print(detector(200))  # T4 Erwartet: RINSE


"""Test für die State-Maschine """

state, s, l = state_machine(
    power=5, state="IDLE", start_time=None, low_power_start=None
)

print(state)  # T5 Erwartet: RUNNING
