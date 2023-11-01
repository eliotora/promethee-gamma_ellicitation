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


def next_approx(w, indT, incT, Pf, asked_pref, i, j):
    return w, indT, incT, Pf


def elicitationProcedure():
    # dataset = "data/HDI20_Classic"
    # dataset = "data/SHA_TOP15"
    dataset = "data/HDI20_1and3_quartiles"
    A, w, pref_fct_desc = load_dataset(dataset)
    pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]
    asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]
    dm = DecisionMaker(A=A, pf=pref_fct)
    Pf = random() * 5
    indT = random() / 5
    incT = max(0.15, indT) + random() / 5
    w_approx = [random() for _ in range(len(pref_fct))]
    w_approx = [i / sum(w_approx) for i in w_approx]

    pgammainst = PrometheeGammaInstance(A, w_approx, pref_fct, indT, incT, Pf)
    pgammainst.compute_preferences()

    i, j = determine_next_query(A, w)
    asked_pref[i][j] = dm.query(i, j)
    print(asked_pref[i][j])
    w, indT, incT, Pf = next_approx(w, indT, incT, Pf, asked_pref, i, j)


if __name__ == "__main__":
    elicitationProcedure()
