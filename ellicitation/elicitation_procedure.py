from numpy.random import randint
from tqdm import tqdm

from ellicitation import misc
from promethee_gamma import PrometheePlotter
from decision_maker import DecisionMaker
from genetic_population_handler import GeneticPopulationHandler
from query_selector import *
from ball_walk_method import SampleBasedProcedure


def determine_next_query(A):
    i = randint(0, len(A) - 1)
    j = randint(0, len(A) - 1)
    while i == j:
        j = randint(0, len(A) - 1)
    return i, j


def elicitationProcedure(A, pref_fct, query_nbr, size, procedure, query_selector):
    # Create decision maker with random or chosen parameters
    dm = DecisionMaker(A, pref_fct)
    # dm = DecisionMaker(A, pref_fct, w, 0.15, 0.15, 4)

    # Setup memory of results of query
    asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]

    # Plotter for utils
    plotter = PrometheePlotter()

    # Accuracies
    accuracies = []

    # Procedure
    procedure = procedure(size, A, pref_fct, query_selector, dm.pgInstance.phis_c)

    # print("Query: ", end=" ")
    for q in tqdm(range(query_nbr)):
        i, j = procedure.next_query()

        while asked_pref[i][j] != 0:
            # i, j, d = popManager.determine_next_query()
            i, j = determine_next_query(A)

        asked_pref[i][j] = dm.pgInstance.pref[i][j]
        w, Ti, Tj, Pf = procedure.assimilate_query(i, j, dm.pgInstance.pref[i][j])

        accuracy = misc.evaluate_parameters(A, pref_fct, dm.indT, dm.incT, dm.w, Ti, Tj, w, dm.pgInstance.pref)
        accuracies.append(accuracy)
    print()
    w, Ti, Tj, Pf = procedure.analyse_sample()
    print(w, "\n", Ti, Tj, Pf, "\n", dm.w, dm.indT, dm.incT, dm.prefFact ,"\n", accuracies)
    return w, Ti, Tj, Pf, accuracies
