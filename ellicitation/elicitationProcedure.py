from decision_maker import DecisionMaker
from instance_reader import load_dataset
from random import randint
import preference_functions as pf
from genetic_population_handler import GeneticPopulationHandler
from promethee_gamma import PrometheePlotter


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

    # Create decision maker with random or chosen parameters
    dm = DecisionMaker(A, pref_fct)
    # dm = DecisionMaker(A, pref_fct, w, 0.15, 0.15, 4)

    # Plotter for utils
    plotter = PrometheePlotter()


    # Genetic method (in progress)
    popManager = GeneticPopulationHandler(100, A, pref_fct)
    for q in range(query_nbr):
        # i, j = determine_next_query(A, w)
        i, j, d = popManager.determine_next_query()

        while asked_pref[i][j] != 0:
            # i, j, d = popManager.determine_next_query()
            i, j = determine_next_query(A, w)
            d = 0
        print("\n", i, j, d)

        asked_pref[i][j] = dm.pgInstance.pref[i][j]
        best = sum([1 for i in range(len(asked_pref)) for j in range(len(asked_pref)) if asked_pref[i][j] != 0])
        print(best)

        popManager.evalPop(asked_pref)
        solution = popManager.population[-1]
        # print("Best fitness: ", solution.fitness, solution)
        for g in range(50):
            # print(g, end="\r")
            popManager.nextGen(asked_pref)
            worst = min(popManager.population, key=lambda e: e.fitness)
            print("Gen", g, ", Worst fitness: ", worst.fitness, worst, end="\r")
            if worst.fitness == best:
                break
        solution = popManager.population[-1]
    popManager.evalPop(dm.pgInstance.pref)
    solution = popManager.population[-1]
    plotter.plot_gammas(solution.handler.gammas, solution.handler.pref, solution.prefFactor, solution.Ti, solution.Tj, "Best solution")
    plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, solution.prefFactor, solution.Ti, solution.Tj, "Best solution on DMs preferences and gammas")
    print("Best: ", popManager.population[-1].fitness)
    print("Worst: ", popManager.population[0].fitness)

    plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, dm.prefFact, dm.indT, dm.incT, "DM preferences")
    # error = (sum([abs(dm.w[i] - solution.weights[i])/dm.w[i] for i in range(len(dm.w))]) +
    #          abs(dm.prefFact - solution.prefFactor)/dm.prefFact +
    #          abs(dm.indT - solution.Ti)/dm.indT +
    #          abs(dm.incT - solution.Tj)/dm.incT)
    # print(error, error/(len(dm.w)+3))


if __name__ == "__main__":
    elicitationProcedure()
