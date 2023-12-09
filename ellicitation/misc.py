from promethee_gamma import PrometheeGammaInstance
import numpy as np


def evaluate_parameters(A, preference_functions, Ti_real, Tj_real, w_real, Ti, Tj, w, real_relations=None):
    n = len(A)
    score = 0
    t = 0
    pg_sol = PrometheeGammaInstance(A, w, preference_functions, Ti, Tj)
    pg_sol.compute_preferences()
    rels = pg_sol.pref
    if real_relations is None:
        pg_real = PrometheeGammaInstance(A, w_real, preference_functions, Ti_real, Tj_real)
        pg_real.compute_preferences()
        real_relations = pg_real.pref

    for i in range(n):
        for j in range(i + 1, n):
            t += 1
            rel = rels[i][j]
            # rel_real = pg.compute_preference_relation(gammas_real[i][j], gammas_real[j][i], Ti_real, Tj_real)
            rel_real = real_relations[i][j]
            # print(t-1,":", i, j, gammas_real[i][j], gammas_real[j][i], rel_real, rel)
            if rel == rel_real:
                score += 1
            # elif errors is not None:
            # print("error:", i, j, rel, rel_real)
            #     errors[rel_real][rel] += 1
            else:
                # print(t-1,":", i, j, gammas_real[i][j], gammas_real[j][i], rel_real, rel)
                1

    return score / t


def print_accuracies(accuracies):
    accuracies = [np.mean([x[i] for x in accuracies]) for i in range(len(accuracies[0]))]
    print(["{0:0.2f}".format(ac) for ac in accuracies])
    return
