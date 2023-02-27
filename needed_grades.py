import numpy as np
from mean_grade import mean_grade, speculated_mean_grade

POSSIBLE_GRADES = np.array([1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0])


def digits_in_base(number, base):
    digits = []
    while number > 0:
        digits.append(number % base)
        number //= base
    return digits


def assignment_int_to_list(n_grades, max_steps, assignment_int):
    digits = digits_in_base(assignment_int, max_steps)
    return np.pad(np.array(digits, dtype=int), (0, n_grades - len(digits)), 'constant', constant_values=0)


def possible_assigments(n_grades, max_steps):
    grade_assignments = []
    assignment_ids = []
    base = min(len(POSSIBLE_GRADES), max_steps)
    max_assignment = base ** n_grades - 1
    for assignment_int in range(max_assignment):
        assignment_list = assignment_int_to_list(
            n_grades, base, assignment_int)
        if sum(assignment_list) == max_steps:
            grade_assignments.append(POSSIBLE_GRADES[assignment_list])
            assignment_ids.append(assignment_int)
    return grade_assignments, assignment_ids


def generate_possible_assigments(n_grades, max_steps):
    base = min(len(POSSIBLE_GRADES), max_steps + 1)
    max_assignment = base ** n_grades - 1
    # steps, array of assignments
    grade_assignments = {}
    assignment_ids = {}
    for steps in range(max_steps + 1):
        grade_assignments[steps] = []
        assignment_ids[steps] = []

    for assignment_int in range(max_assignment):
        assignment_list = assignment_int_to_list(
            n_grades, base, assignment_int)
        steps = int(sum(assignment_list))
        if steps > max_steps:
            continue
        grade_assignments[steps].append(POSSIBLE_GRADES[assignment_list])
        assignment_ids[steps].append(assignment_int)
    return grade_assignments, assignment_ids


def assign(not_graded, grades):
    return [[name, credits, grade] for (name, credits), grade in zip(not_graded, grades)]

def exists_worse(grades, satisfying_grades):
    for grades_worse in satisfying_grades:
        np_grades = np.array(grades)
        np_grades_worse = np.array(grades_worse)
        if np.all(np_grades <= np_grades_worse) and not np.all(np_grades == np_grades_worse):
            return True
    return False
                


def needed_grades(current_grades, not_graded, wanted_mean):
    speculated_grades = np.array(
        [[module[0], module[1], POSSIBLE_GRADES[0]] for module in not_graded])

    speculated_mean = speculated_mean_grade(current_grades, speculated_grades)
    if speculated_mean > wanted_mean:
        print(
            f"Can not reach wanted grade. Best possible is: {speculated_mean}")
        return [], []

    satisfying_grades = []
    respective_means = []
    max_steps = (len(POSSIBLE_GRADES) - 1) * len(not_graded)
    # max_steps = 4
    possible_assigments, step_ids = generate_possible_assigments(
        len(not_graded), max_steps)
    for steps in range(max_steps):
        assignments = possible_assigments[steps]
        ids = step_ids[steps]
        for assignment, assignment_id in zip(assignments, ids):
            speculated_grades = assign(not_graded, assignment)
            speculated_mean = speculated_mean_grade(
                current_grades, speculated_grades)
            if speculated_mean <= wanted_mean:
                satisfying_grades.append(speculated_grades)
                respective_means.append(speculated_mean)
    # post-processing: remove possible assignments that are strictly better than another assignment
    post_processed_satisfying_grades = []
    post_processed_respective_means = []
    for grades, mean in zip(satisfying_grades, respective_means):
        # check if there is an assignment that is strictly worse
        if not exists_worse(grades, satisfying_grades):
            post_processed_satisfying_grades.append(grades)
            post_processed_respective_means.append(mean)
    return post_processed_satisfying_grades, post_processed_respective_means
