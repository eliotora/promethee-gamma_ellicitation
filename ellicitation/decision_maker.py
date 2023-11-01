from promethee_gamma import *
from random import *


class DecisionMaker:
    def __init__(self, A, pf, w=None, indT=None, incT=None, Pf=None):
        if indT is None:
            self.indT = random() / 5
        else:
            self.indT = indT
        if incT is None:
            self.incT = max(0.15, self.indT) + random() / 5
        else:
            self.incT = incT
        if Pf is None:
            self.prefFact = random() * 5
        else:
            self.prefFact = Pf
        if w is None:
            self.w = [random() for _ in range(len(pf))]
            self.w = [i / sum(self.w) for i in self.w]
        else:
            self.w = w

        self.pgInstance = PrometheeGammaInstance(A, self.w, pf, self.indT, self.incT, self.prefFact)
        self.pgInstance.compute_preferences()
        self.relations = self.pgInstance.pref

    def query(self, i, j):
        return self.relations[i][j]
