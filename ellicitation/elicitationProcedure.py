from decision_maker import DecisionMaker
from instance_reader import load_dataset
from promethee_gamma import PrometheeGammaInstance, I, J, P, nP
from random import random, randint
import preference_functions as pf

def determine_next_query(A, w):
    i = randint(0, len(A))
    j = randint(0, len(A))
    while i == j:
        j = randint(0, len(A))
    return i, j

def elicitationProcedure():
    # dataset = "data/HDI20_Classic"
    # dataset = "data/SHA_TOP15"
    dataset = "data/HDI20_1and3_quartiles"
    A, w, pref_fct_desc = load_dataset(dataset)
    pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]

    dm = DecisionMaker(A=A, pf=pref_fct)
    Pf = random() * 5
    indT = random() / 5
    incT =  max(0.15, indT) + random() / 5
    w_approx = [random() for _ in range(len(A))]
    w_approx = [i / sum(w_approx) for i in w_approx]

    pgammainst = PrometheeGammaInstance(A, w_approx, pref_fct, indT, incT, Pf)
    pgammainst.compute_preferences()

    i, j = determine_next_query(A, w)


if __name__=="__main__":
    elicitationProcedure()