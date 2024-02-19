from ellicitation.genetic_population_handler import GeneticPopulationHandler
from ellicitation.ball_walk_method import SampleBasedProcedure
from ellicitation.query_selector import discrimination_power_based_query, vote_based_query
import os

procedures_dict = {
    SampleBasedProcedure.__name__: SampleBasedProcedure,
    GeneticPopulationHandler.__name__: GeneticPopulationHandler
}

query_selector_dict = {
    discrimination_power_based_query.__name__: discrimination_power_based_query,
    vote_based_query.__name__: vote_based_query
}


def init_tests(methods, test_nbr):
    with open("todo_tests.txt", "w") as file:
        for method in methods:
            for test in range(test_nbr):
                file.write(", ".join([e.__name__ for e in method]) + ", " + str(test) + "\n")


def run_test(file_path):
    try:
        with open("tests_done.txt", "r") as file:
            data_done = file.readlines()
            for i in range(len(data_done)):
                data_done[i] = data_done[i].strip('\n')
            print(data_done)
    except FileNotFoundError:
        file = open("tests_done.txt", "w")
        file.close()
        data_done = []

    with open(file_path, "r", newline="") as file:
        data_todo = file.readlines()
        for row in data_todo:
            row_striped = row.strip('\r\n')
            if row_striped not in data_done:
                content = row_striped.split(", ")
                config = [procedures_dict[content[0]], query_selector_dict[content[1]], int(content[2])]
                print("Running: ", config)
                with open("tests_done.txt", "a", newline="") as file:
                    file.write(row)
    os.remove("tests_done.txt")
    os.remove(file_path)


if __name__ == "__main__":
    procedures = [SampleBasedProcedure, GeneticPopulationHandler]
    queries = [discrimination_power_based_query, vote_based_query]
    methods = [[p, q] for p in procedures for q in queries]
    init_tests(methods, 5)
    #
    run_test("todo_tests.txt")
