from decision_maker import DecisionMaker
from instance_reader import load_dataset
from random import randint
import preference_functions as pf
from genetic_population_handler import GeneticPopulationHandler
from promethee_gamma import PrometheePlotter
from query_selector import *
from elicitation_procedure import ElicitationProcedure


def determine_next_query(A, w):
    i = randint(0, len(A)-1)
    j = randint(0, len(A)-1)
    while i == j:
        j = randint(0, len(A)-1)
    return i, j


def next_approx(w, indT, incT, Pf, asked_pref, i, j):
    return w, indT, incT, Pf


def elicitationProcedure():
    # Choose dataset and load it
    # dataset = "data/HDI20_Classic"
    # dataset = "data/SHA_TOP15"
    dataset = "data/HDI20_1and3_quartiles"
    A, w, pref_fct_desc = load_dataset(dataset)
    pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]
    maxFitness = len(A)**2
    print("Max fitness is:", maxFitness)

    # Setup memory of results of query
    query_nbr = 10
    # query_nbr = 20
    # query_nbr = 50
    asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]

    popManager.evalPop(dm.pgInstance.pref)
    solution = popManager.population[-1]
    plotter.plot_gammas(solution.handler.gammas, solution.handler.pref, solution.prefFactor, solution.Ti, solution.Tj, "Best solution")
    plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, solution.prefFactor, solution.Ti, solution.Tj, "Best solution on DMs preferences and gammas")
    print("Best: ", popManager.population[-1].fitness)
    print("Worst: ", popManager.population[0].fitness)

    plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, dm.prefFact, dm.indT, dm.incT, "DM preferences")



if __name__ == "__main__":
    # elicitationProcedure()
    dataset = "data/HDI20_1and3_quartiles"
    A, w, pref_fct_desc = load_dataset(dataset)
    pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]
    ElicitationProcedure(A, pref_fct, 20, 100)


