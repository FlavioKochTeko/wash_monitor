import json


def load_program():

    programs = []

    try:
        with open("program_database.json") as f:
            for line in f:
                programs.append(json.loads(line))
    except FileNotFoundError:
        pass

    return programs


def compare_program(current_phases, program):
    score = 0
    db_phases = program["phases"]

    for i in range(min(len(current_phases), len(db_phases))):
        phase_now = current_phases[i][0]
        phase_db = db_phases[i][0]

        if phase_now == phase_db:
            score += 1

    return score


def detect_program(current_phases):

    program = load_program()

    best_program = None
    best_score = 0

    for program in program:
        score = compare_program(current_phases, program)

        if score > best_score:
            best_score = score
            best_program = program

    return best_program
