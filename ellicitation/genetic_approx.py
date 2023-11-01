from random import random, randint

from genetic_handler import PrometheeGeneticHandler


class GeneticSolution:
    def __init__(self, w, indT, incT, Pf, A, prefFun):
        self.weights = w
        self.Ti = indT
        self.Tj = incT
        self.prefFactor = Pf
        self.genome = [w, indT, incT, Pf]
        self.handler = PrometheeGeneticHandler(A, w, prefFun, indT, incT, Pf)
        self.handler.compute_preferences()
        self.fitness = 0

    def evaluate(self, knownPref):
        computedPref = self.handler.pref
        for i in range(len(knownPref)):
            for j, pref in enumerate(knownPref[i]):
                if pref == 0:
                    pass
                elif pref == computedPref[i][j]:
                    self.fitness += 1
        return self.fitness

    def mutate(self):
        for i in range(len(self.weights)):
            self.weights[i] += random() * 0.05 * (-1)**randint(0, 1)
        self.weights = [w/sum(self.weights) for w in self.weights]

        self.Ti += random() * 0.3 * (-1) ** randint(0, 1)
        self.Tj += min(self.Ti, random() * 0.3 * (-1) ** randint(0, 1))
        self.prefFactor += random() * 2 * (-1) ** randint(0, 1)
        if self.prefFactor <= 0:
            self.prefFactor = 0.001

