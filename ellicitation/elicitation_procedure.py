from numpy.random import randint

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


class ElicitationProcedure:
    def __init__(self, A, pref_fct, query_nbr, size):
        # Create decision maker with random or chosen parameters
        dm = DecisionMaker(A, pref_fct)
        # dm = DecisionMaker(A, pref_fct, w, 0.15, 0.15, 4)

        # Setup memory of results of query
        asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]

        # Plotter for utils
        plotter = PrometheePlotter()

        # Procedure
        # procedure = GeneticPopulationHandler(size, A, pref_fct, vote_based_query)
        # procedure = GeneticPopulationHandler(size, A, pref_fct, discrimination_power_based_query)
        # procedure = SampleBasedProcedure(size, A, pref_fct, vote_based_query, dm.pgInstance.phis_c)
        procedure = SampleBasedProcedure(size, A, pref_fct, discrimination_power_based_query, dm.pgInstance.phis_c)

        for q in range(query_nbr):
            print(q)
            i, j = procedure.next_query()
            print("Query:", i, j, asked_pref[i][j])

            while asked_pref[i][j] != 0:
                # i, j, d = popManager.determine_next_query()
                i, j = determine_next_query(A)
                print("Random query chosen: ", i, j)

            asked_pref[i][j] = dm.pgInstance.pref[i][j]
            procedure.assimilate_query(i, j, dm.pgInstance.pref[i][j])

        self.solution = procedure.getSolution()
        plotter.plot_gammas(self.solution.handler.gammas, self.solution.handler.pref, self.solution.prefFactor,
                            self.solution.Ti, self.solution.Tj, "Best solution")
        plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, self.solution.prefFactor, self.solution.Ti,
                            self.solution.Tj,"Best solution on DMs preferences and gammas")
