from random import random, randint

from basic_instance import BasicInstance


class GeneticSolution:
    def __init__(self, w, indT, incT, Pf, A, prefFun):
        self.weights = w
        self.Ti = indT
        self.Tj = incT
        self.prefFactor = Pf
        self.genome = [w, indT, incT, Pf]
        self.handler = BasicInstance(A, prefFun)
        self.indicators = self.handler.compute_indicators(self.handler.compute_gammas(w), self.Ti, self.Tj, self.prefFactor)
        self.pref = self.handler.prefs_from_indicators(self.indicators)
        self.fitness = 0

    def evaluate(self, knownPref):
        self.pref = self.handler.compute_preferences(self.weights, self.Ti, self.Tj, self.prefFactor)
        self.fitness = 0
        for i in range(len(knownPref)):
            for j, pref in enumerate(knownPref[i]):
                if pref == 0:
                    pass
                elif pref == self.pref[i][j]:
                    self.fitness += 1
        return self.fitness

    def mutate(self):
        for i in range(len(self.weights)):
            self.weights[i] += random() * 0.05 * (-1)**randint(0, 1)
        self.weights = [w/sum(self.weights) for w in self.weights]

        self.Ti += random() * 0.3 * (-1) ** randint(0, 1)
        self.Tj = min(self.Ti, self.Tj + random() * 0.3 * (-1) ** randint(0, 1))
        self.prefFactor += random() * 2 * (-1) ** randint(0, 1)
        if self.prefFactor <= 0:
            self.prefFactor = 0.001

