from decision_maker import DecisionMaker
from instance_reader import load_dataset
from promethee_gamma import PrometheeGammaInstance, I, J, P, nP
from random import random, randint
import preference_functions as pf
from genetic_population_handler import GeneticPopulationHandler
from promethee_gamma import PrometheePlotter


def determine_next_query(A, w):
    i = randint(0, len(A))
    j = randint(0, len(A))
    while i == j:
        j = randint(0, len(A))
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
    asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]

    # Create decision maker with random or chosen parameters
    dm = DecisionMaker(A, pref_fct)
    # dm = DecisionMaker(A, pref_fct, w, 0.15, 0.15, 4)

    # Plotter for utils
    plotter = PrometheePlotter()

    # Random values to start with one solution
    # Pf = random() * 5
    # indT = random() / 5
    # incT = max(0.15, indT) + random() / 5
    # w_approx = [random() for _ in range(len(pref_fct))]
    # w_approx = [i / sum(w_approx) for i in w_approx]
    #
    # pgammainst = PrometheeGammaInstance(A, w_approx, pref_fct, indT, incT, Pf)
    # pgammainst.compute_preferences()

    # Genetic method (in progress)
    popManager = GeneticPopulationHandler(100, A, pref_fct)
    popManager.evalPop(dm.pgInstance.pref)
    solution = popManager.population[-1]
    print("Best fitness: ", solution.fitness, solution)
    plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, solution.prefFactor, solution.Ti, solution.Tj)
    for i in range(100):
        print("Gen ", i)
        popManager.nextGen(dm.pgInstance.pref)
        solution = popManager.population[-1]
        print("Best fitness: ", solution.fitness, solution)
        if solution.fitness == maxFitness:
            break
    plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, solution.prefFactor, solution.Ti, solution.Tj)

    # i, j = determine_next_query(A, w)
    # asked_pref[i][j] = dm.query(i, j)
    # print(asked_pref[i][j])
    # # w, indT, incT, Pf = next_approx(w, indT, incT, Pf, asked_pref, i, j)
    # solution = GeneticSolution(w_approx, indT, incT, Pf, A, pref_fct)
    # print("Fitness: " + str(solution.evaluate(dm.pgInstance.pref)))
    # error = []
    # for i, line in enumerate(solution.handler.pref):
    #     l = []
    #     for j, elem in enumerate(line):
    #         if elem == dm.pgInstance.pref[i][j]:
    #             l.append(1)
    #         else:
    #             l.append(-1)
    #     error.append(l)
    #     print(l)
    #
    # print("Errors: ", str(sum([sum(l) for l in error])))



    # plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, solution.prefFactor, solution.Ti, solution.Tj)
    plotter.plot_gammas(dm.pgInstance.gammas, dm.pgInstance.pref, dm.prefFact, dm.indT, dm.incT)
    error = (sum([abs(dm.w[i] - solution.weights[i])/dm.w[i] for i in range(len(dm.w))]) +
             abs(dm.prefFact - solution.prefFactor)/dm.prefFact +
             abs(dm.indT - solution.Ti)/dm.indT +
             abs(dm.incT - solution.Tj)/dm.incT)
    print(error, error/(len(dm.w)+3))


if __name__ == "__main__":
    elicitationProcedure()
