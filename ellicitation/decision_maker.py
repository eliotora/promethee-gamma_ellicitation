from promethee_gamma import *
from random import *


class DecisionMaker:
    def __init__(self, A, pf):
        self.indT = random() / 5
        self.incT = max(0.15, self.indT) + random() / 5
        self.prefF = random() * 5
        self.w = [random() for _ in range(len(pf))]
        self.w = [i / sum(self.w) for i in self.w]
        self.pgInstance = PrometheeGammaInstance(A, self.w, pf, self.indT, self.incT, self.prefF)
        self.pgInstance.compute_preferences()
        self.relations = self.pgInstance.pref

    def query(self, i, j):
        return self.relations[i][j]
