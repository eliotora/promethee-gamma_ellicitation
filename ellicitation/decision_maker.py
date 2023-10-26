from promethee_gamma.promethee_gamma import PrometheeGammaInstance
from random import *
from promethee_gamma.preference_functions import make_pref_fct

class decisionMaker:
    def __init__(self, A, pf):
        self.indT = random() / 5
        self.incT = max(0.15, self.indT) + random() / 5
        self.prefF = random() * 5
        self.w = [random() for _ in range(len(A))]
        self.w = [i / sum(self.w) for i in self.w]

        self.pgInstance = PrometheeGammaInstance(A, self.w, pf, self.indT, self.incT, self.prefF)
        self.pgInstance.compute_preferences()
