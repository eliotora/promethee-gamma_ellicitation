import pprint

from decision_maker import DecisionMaker
from ellicitation import misc
from instance_reader import load_dataset
import random as rd
import preference_functions as pf
from genetic_population_handler import GeneticPopulationHandler
from promethee_gamma import PrometheePlotter
from ball_walk_method import SampleBasedProcedure
from query_selector import *
from elicitation_procedure import elicitationProcedure
from particle_handler import ParticleHandler


def determine_next_query(A, w):
    i = rd.randint(0, len(A) - 1)
    j = rd.randint(0, len(A) - 1)
    while i == j:
        j = rd.randint(0, len(A) - 1)
    return i, j


def next_approx(w, indT, incT, Pf, asked_pref, i, j):
    return w, indT, incT, Pf


def compute_accuracy(A, pref_fct, query_nbr, tests, size, procedure, query_selector):
    all_accuracies = []

    for test_id in range(tests):
        print("##########", test_id, "##########")
        rd.seed(test_id)
        np.random.seed(test_id)
        rd.shuffle(A)

        w, Ti, Tj, Pf, accuracies = elicitationProcedure(A, pref_fct, query_nbr, size, procedure, query_selector)
        all_accuracies.append(accuracies)

    return all_accuracies


if __name__ == "__main__":
    # elicitationProcedure()
    SHA_Q13 = "data/SHA_1and3_quartiles"
    HDI_Q13 = "data/HDI_1and3_quartiles"
    HDI_20 = "data/HDI20_Classic"
    EPI2020_Q13 = "data/EPI2020_1and3_quartiles"
    TIMES_Q13 = "data/TIMES_1and3_quartiles"
    # datasets = [SHA_Q13, HDI_Q13, HDI_20, EPI2020_Q13, TIMES_Q13]
    datasets = [HDI_Q13]
    # procedures = [SampleBasedProcedure, GeneticPopulationHandler]
    # procedures = [SampleBasedProcedure]
    # procedures = [GeneticPopulationHandler]
    procedures = [ParticleHandler]
    query_selectors = [vote_based_query, discrimination_power_based_query, votes_with_percentages]
    # query_selectors = [vote_based_query]
    # query_selectors = [votes_with_percentages]
    # query_selectors = [discrimination_power_based_query]

    query_number = 20
    size = 100
    tests = 1

    for procedure in procedures:
        for query_selector in query_selectors:
            accuracies = []
            for dataset in datasets:
                print(procedure.__name__, query_selector.__name__, dataset, "refs:", query_number, "tests:", tests,
                      "samples:", size)
                A, w, pref_fct_desc = load_dataset(dataset)
                pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]

                accuracies_dataset = compute_accuracy(A, pref_fct, query_number, tests, size, procedure, query_selector)

                misc.print_accuracies(accuracies_dataset)
                accuracies.append(accuracies_dataset)

            file_name = procedure.__name__ + "_" + query_selector.__name__ + "_query_" + str(
                query_number) + "_tests_" + str(tests) + "_size_" + str(size)
            with open("../results/" + file_name + ".txt", "w") as file:
                for ai, a in enumerate(accuracies):
                    file.write(datasets[ai] + " ")
                    file.write(str(a) + "\n")
