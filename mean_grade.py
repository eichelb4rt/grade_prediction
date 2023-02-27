import numpy as np


def mean_grade(grades):
    weights = grades[:, 1].astype(np.float32)
    values = grades[:, 2].astype(np.float32)
    return sum(weights * values) / sum(weights)

def speculated_mean_grade(current_grades, speculated_grades):
    speculated_all_grades = np.concatenate(
        (current_grades, speculated_grades), axis=0)
    return mean_grade(speculated_all_grades)
