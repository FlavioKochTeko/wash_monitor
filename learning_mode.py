import time
import json


class LearningMode:
    """Zeichnet einen Waschvorgan auf und speichert ihn als Referenzprofil."""

    def __init__(self):
        self.learning_active: bool = False
        self.phase_sequence: list = []
        self.last_phase: str = None
        self.phase_start: float = None

    def start_learning(self) -> None:
        """Startet den Lernmodus und setzt alle Variabeln zurück."""

        print("Lernmodus gestartet. Bitte führen Sie ein Waschprogramm durch.")
        self.learning_active = True
        self.phase_sequence = []
        self.last_phase = None
        self.phase_start = None

    def record_phase(self, phase: str) -> None:
        """Speichert eine erkannte Phase und berechnet die Dauer der vorherigen.

        Args:
            phase: Name der aktuell erkannten Phase (z.B. 'HEATING').
        """

        if not self.learning_active:
            return

        now = time.time()

        if phase != self.last_phase:
            if self.last_phase is not None:
                duration = now - self.phase_start
                self.phase_sequence.append([self.last_phase, duration])

            self.phase_start = now
            self.last_phase = phase

    def stop_learning(self) -> None:
        """Beendet den Lernmodus und speichert das Profil."""

        if not self.learning_active:
            return

        now = time.time()

        if self.last_phase is not None:
            duration = now - self.phase_start
            self.phase_sequence.append([self.last_phase, duration])
        print("Learning Mode gestoppt.")
        total_duration = sum(duration for phase, duration in self.phase_sequence)

        program = {
            "name": input("Name des Waschprogramms: "),
            "total_duration": total_duration,
            "phases": self.phase_sequence,
        }
        with open("program_database.json", "a") as file:
            json.dump(program, file)
            file.write("\n")

        self.learning_active = False
