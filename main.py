import numpy as np
from mean_grade import mean_grade
from needed_grades import needed_grades
from argparse import ArgumentParser


def parse():
    parser = ArgumentParser(description="What grades you got?")
    parser.add_argument('-w', "--wanted", metavar="grade", dest="wanted", type=float)
    args = parser.parse_args()
    show_needed_grades = not args.wanted is None
    wanted_grade = args.wanted
    return show_needed_grades, wanted_grade

def main():
    show_needed_grades, wanted_grade = parse()
        
    graded = np.array([
        ["QA", 3, 1.3],
        ["PC I", 6, 1.3],
        ["CompVis I", 6, 1.0],
        ["Lerntheorie", 6, 1.0],
        ["Algorithm Engineering", 6, 1.3],
        ["Visualisierung", 6, 1.3],
        ["ECDS", 3, 2.3],
        ["AGML", 6, 1.3],
        ["Causal Inference", 3, 1.3],
        ["AGML LAB", 4, 1.0],
        ["Mustererkennung", 6, 1.7],
        ["Unity", 3, 1.3],
        ["Komplexitätstheorie", 6, 1.0],
        ["Komplexitätstheorie LAB", 6, 1.0],
        ["Graphische Modelle", 9, 1.0],
    ])
    
    not_graded = np.array([
        ["ML & DM", 6],
        ["GM LAB", 3],
        ["GTPC", 6],
    ])

    print(f"current grade: {mean_grade(graded)}")
    if not show_needed_grades:
        return
    
    print(f"wanted grade: {wanted_grade}")
    
    edge_grades, respective_means = needed_grades(graded, not_graded, wanted_grade)
    for i, grades in enumerate(edge_grades):
        print(f"\nPossible solution: (grade = {respective_means[i]})\n{grades}")


if __name__ == "__main__":
    main()
