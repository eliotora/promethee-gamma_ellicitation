from promethee_gamma import PrometheeGammaInstance
class PrometheeGeneticHandler(PrometheeGammaInstance):
    def __init__(self, Alt, wts, pref_fun, indT, incT, Pf):
        super().__init__(Alt, wts, pref_fun, indT, incT, Pf)

    def updatePhis(self, i, j, rel):
        pass