import json


def load_program() -> list:
    """Lädt alle gespeicherten Programme aus der Datenbank.

    Returns:
        Liste aller gespeicherten Programme.
    """
    programs = []
    try:
        with open("program_database.json") as f:
            for line in f:
                programs.append(json.loads(line))
    except FileNotFoundError:
        pass
    return programs


def compare_program(current_phases: list, program: dict) -> int:
    """Vergleicht die aktuelle Phasensequenz mit einem gespeicherten Programm.

    Args:
        current_phases: Liste der aktuell erkannten Phasen.
        program: Gespeichertes Programm aus der Datenbank.

    Returns:
        Score als Integer, höher bedeutet bessere Übereinstimmung.
    """
    score = 0
    db_phases = program["phases"]

    for i in range(min(len(current_phases), len(db_phases))):
        phase_now, duration_now = current_phases[i]
        phase_db, duration_db = db_phases[i]

        if phase_now == phase_db:
            if phase_now == "HEATING":
                score += 2

            else:
                score += 1

            time_diff = abs(duration_now - duration_db)
            if time_diff < duration_db * 0.30:
                score += 1

    return score


def detect_program(current_phases: list) -> dict:
    """Sucht das am besten passende Programm in der Datenbank.

    Args:
        current_phases: Liste der aktuell erkannten Phase.

    Returns:
        Das erkannte Programm als Dict
    """
    all_programs = load_program()

    best_program = None
    best_score = 0
    min_score = 3

    for program in all_programs:
        score = compare_program(current_phases, program)
        # Debug (deaktiviert)
        # print(f"Vergleich mit Programm '{program['name']}': Score = {score}")
        if score > best_score:
            best_score = score
            best_program = program

    if best_score >= min_score:
        return best_program
    else:
        return None
