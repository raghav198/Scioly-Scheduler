import os

import cvxpy
import numpy as np

NUM_TEAMS = 1
TEAM_SIZE = 5
NUM_STUDENTS = 12
NUM_EVENTS = 4
NUM_SLOTS = 2


def create_aux_product(var1, var2, dim1, dim2, dim_share):
    aux = [[cvxpy.Variable(dim_share) for k in range(dim2)] for j in range(dim1)]
    aux_constraints = [aux[j][k] <= var1[:, j]
                       for j in range(dim1)
                       for k in range(dim2)]
    aux_constraints += [aux[j][k] <= var2[:, k]
                        for j in range(dim1)
                        for k in range(dim2)]
    aux_constraints += [aux[j][k] >= var1[:, j] + var2[:, k] - 1
                        for j in range(dim1)
                        for k in range(dim2)]

    aux_constraints += [aux[j][k] >= 0
                        for j in range(dim1)
                        for k in range(dim2)]

    return aux, aux_constraints


def optimize_teams(skills, schedule, NUM_TEAMS, TEAM_SIZE):
    NUM_STUDENTS, _NUM_EVENTS_1 = skills.shape
    NUM_SLOTS, _NUM_EVENTS_2 = schedule.shape
    assert _NUM_EVENTS_1 == _NUM_EVENTS_2
    NUM_EVENTS = _NUM_EVENTS_1

    assignments = cvxpy.Variable((NUM_STUDENTS, NUM_EVENTS), boolean=True)
    teams = cvxpy.Variable((NUM_STUDENTS, NUM_TEAMS), boolean=True)

    objective = cvxpy.sum(cvxpy.multiply(assignments, skills))

    students_per_team = [cvxpy.sum(teams[:, k]) <= TEAM_SIZE
                         for k in range(NUM_TEAMS)]

    spe_aux, spe_aux_constraints = create_aux_product(assignments, teams, NUM_EVENTS, NUM_TEAMS, NUM_STUDENTS)

    students_per_event = spe_aux_constraints + [cvxpy.sum(spe_aux[j][k]) <= 2
                                                for j in range(NUM_EVENTS)
                                                for k in range(NUM_TEAMS)]

    no_time_conflicts = [cvxpy.sum(cvxpy.multiply(assignments[i, :], schedule[h, :])) <= 1
                         for i in range(NUM_STUDENTS)
                         for h in range(NUM_SLOTS)]

    team_placement = [cvxpy.sum(teams[i, :]) <= 1 for i in range(NUM_STUDENTS)] + [
        cvxpy.sum(assignments[i, :]) <= NUM_EVENTS * cvxpy.sum(teams[i, :])
        for i in range(NUM_STUDENTS)]

    non_negativity = [teams >= 0, assignments >= 0]

    problem = cvxpy.Problem(cvxpy.Maximize(objective),
                            constraints=non_negativity + students_per_team + students_per_event + no_time_conflicts + team_placement)
    problem.solve(solver='GLPK_MI')

    event_assignments = assignments.value > 0.5
    team_assignments = teams.value > 0.5

    return event_assignments, team_assignments


if __name__ == "__main__":
    skills = None
    if os.path.exists('skills.txt'):
        skills = np.loadtxt('skills.txt')
        if skills.shape != (NUM_STUDENTS, NUM_EVENTS):
            skills = None
    if skills is None:
        _event_participation = np.random.rand(NUM_STUDENTS, NUM_EVENTS) < 0.5
        skills = np.multiply(
            np.random.rand(NUM_STUDENTS, NUM_EVENTS),
            _event_participation)

        # np.savetxt('skills.txt', skills)
    print(skills)
    schedule = np.array(
        [[1, 1, 0, 0],
         [0, 0, 1, 1]])

    event_assignments, team_assignments = optimize_teams(skills, schedule, NUM_TEAMS, TEAM_SIZE)

    print("======Student Participation======")
    for student in range(NUM_STUDENTS):
        events, = np.where(event_assignments[student, :])
        print(
            f"Student #{student} is participating in the following events: {events} and has skills {skills[student, :]}")

    print()
    print("======Team Assignment======")
    for team in range(NUM_TEAMS):
        students, = np.where(team_assignments[:, team])
        print(f"Team {team} has the following students: {students}")

    print()
    print("======Event Assignment======")
    for event in range(NUM_EVENTS):
        students, = np.where(event_assignments[:, event])
        print(f"Event {event} has students {students} participating")

"""
print("\n\nVerifying values")

a = assignments.value
t = teams.value

for j in range(NUM_EVENTS):
    print(f"Event {j}")
    for k in range(NUM_TEAMS):
        x = spe_aux[j][k].value
        print(f"\tTeam {k} = {np.sum(np.multiply(a[:, j], t[:, k]))} ({np.sum(x)})")
# students_per_event = [cvxpy.sum(cvxpy.multiply(assignments[:, j], teams[:, k])) <= 2 
#                         for j in range(NUM_EVENTS)
#                         for k in range(NUM_TEAMS)]

# print(skills)
# print(assignments.value > 0.5)
# print(teams.value > 0.5)
"""
