import random
import numpy as np
from ellicitation.genetic_approx import GeneticSolution
from ellicitation.query_selector import *
from PrometheePlotter import I, J, P, nP


def normalize_weights(constraint):
    w = constraint[:-3]
    w = [wc / sum(w) for wc in w]
    return w + constraint[-3:]


def satisfy_basic_constraints(point):
    # print(point)
    if np.min(point) < 0:  # all terms must be positive
        # print("Min <0")
        return False
    if point[-3] > point[-2]:  # Ti <= Tj
        # print("Ti > Tj")
        return False
    if point[-2] > 1:  # max value for Tj
        # print("Tj > 1")
        return False
    if point[-1] <= 0:
        return False
    return True


def satisfy(point, constraints):
    if not satisfy_basic_constraints(point):
        # print("Basic constraints")
        return False

    for constraint in constraints:
        if not satisfy_single_constraint(point, constraint):
            # print("Single constraints")
            return False
    return True


def satisfy_single_constraint(point, constraint):
    w_point = point[:-3]
    Ti_point = point[-3]
    Tj_point = point[-2]
    w = constraint[:-2]
    Ti = constraint[-2]
    Tj = constraint[-1]
    k = len(w)
    # x = constraint[-1]   # independant term for weights
    if Ti == 0 and Tj == 0:  # normal preference constraint
        if np.dot(w, w_point) <= 0:
            return False
        # if normal preference then can not have indifference or incomparability !
        gij = sum([w[c] * w_point[c] for c in range(k) if w[c] > 0])
        gji = sum([-w[c] * w_point[c] for c in range(k) if w[c] < 0])
        if max(gij, gji) <= Ti_point or min(gij, gji) >= Tj_point:
            return False


    # Ti constraints have shape (wc, 1, 0) with wc being phi_c[i] - phi_c[j] for all c where i > j
    elif Ti == 1:
        if np.dot(w, w_point) > Ti_point:
            return False

    # Tj constraints have shape (wc, 0, 1) with wc being phi_c[i] - phi_c[j] for all c where i > j
    elif Tj == 1:
        if np.dot(w, w_point) < Tj_point:
            return False
    else:
        print("Error! values of Ti, Tj not 1 or 0")

    return True


def ball_walk(constraints, samples, k, Nsamples, delta=0.05):
    """Petit pas dans l'espace des paramètres pour généner un ensemble de samples de cet espace"""
    D = k + 3

    if len(samples) == 0:
        point = [1 / k for c in range(k)] + [0.15, 0.25, 1]
    else:
        point = samples[0]

    for s in range(Nsamples - len(samples)):
        step = [random.random() * delta * 2 - delta for d in range(D)]
        next_point = [point[d] + step[d] for d in range(D)]
        next_point = normalize_weights(next_point)

        while not satisfy(next_point, constraints):
            step = [random.random() * delta * 2 - delta for d in range(D)]
            next_point = [point[d] + step[d] for d in range(D)]
            next_point = normalize_weights(next_point)

        point = next_point

        samples.append(point)
    random.shuffle(samples)
    return


class SampleBasedProcedure:
    def __init__(self, Nsamples, A, pref_fct, query_selector, phi_c):
        self.Nsamples = Nsamples
        self.phi_c = phi_c
        self.pref_fct = pref_fct
        self.query_selector = query_selector
        self.constraints = []
        self.samples = []
        self.A = A
        self.k = len(A[0])
        self.n = len(A)
        self.ball_walk()

    def ball_walk(self, delta=0.05):
        """Petit pas dans l'espace des paramètres pour généner un ensemble de samples de cet espace"""
        D = self.k + 3

        if len(self.samples) == 0:
            point = [1 / self.k for c in range(self.k)] + [0.15, 0.25, 1]
        else:
            point = self.samples[0]

        while len(self.samples) < self.Nsamples:
            step = [random.random() * delta * 2 - delta for d in range(D)]
            next_point = [point[d] + step[d] for d in range(D)]
            next_point = normalize_weights(next_point)

            tries = 0
            while not satisfy(next_point, self.constraints) and tries < 10000:
                step = [random.random() * delta * 2 - delta for d in range(D)]
                next_point = [point[d] + step[d] for d in range(D)]
                next_point = normalize_weights(next_point)
                tries += 1

            point = next_point

            self.samples.append(point)
        random.shuffle(self.samples)
        return

    def next_query(self):
        if self.query_selector.__name__ == discrimination_power_based_query.__name__:
            return self.query_selector(self.phi_c, self.samples)
        elif self.query_selector.__name__ == vote_based_query.__name__ or self.query_selector.__name__ == votes_with_percentages.__name__:
            population = [GeneticSolution(s[:-3], s[-3], s[-2], s[-1], self.A, self.pref_fct) for s in self.samples]
            return self.query_selector(self.A, population)

    def getSolution(self):
        s = self.samples[0]
        return GeneticSolution(s[:-3], s[-3], s[-2], s[-1], self.A, self.pref_fct)

    def assimilate_query(self, i, j, answer):
        new_constraints = self.generate_constraints(i, j, answer)
        self.constraints.extend(new_constraints)
        self.samples = list(filter(lambda s: satisfy(s, new_constraints), self.samples))
        self.ball_walk()
        return self.analyse_sample()

    def generate_constraints(self, i, j, preference_relation):
        new_constraints = []

        if preference_relation == I:
            new_constraints.append([max(0, self.phi_c[i][c] - self.phi_c[j][c]) for c in range(self.k)] + [1, 0])
            new_constraints.append([max(0, self.phi_c[j][c] - self.phi_c[i][c]) for c in range(self.k)] + [1, 0])
        elif preference_relation == J:
            new_constraints.append([max(0, self.phi_c[i][c] - self.phi_c[j][c]) for c in range(self.k)] + [0, 1])
            new_constraints.append([max(0, self.phi_c[j][c] - self.phi_c[i][c]) for c in range(self.k)] + [0, 1])
        elif preference_relation == P:
            new_constraints.append([self.phi_c[i][c] - self.phi_c[j][c] for c in range(self.k)] + [0, 0])
            # constraint on I and J also:
        else:
            new_constraints.append([self.phi_c[j][c] - self.phi_c[i][c] for c in range(self.k)] + [0, 0])

        # print((i, j), pg.REL_NAMES[preference_relation])
        # new_constraints = [[0.1, 0.1, 1, 0], [0.4, 0.3, 0, 1]] # for tests
        return new_constraints

    def analyse_sample(self):
        data = []
        res = []
        total = 0
        # print("samples state:")
        for c in range(len(self.samples[0])):
            x = [s[c] for s in self.samples]
            # print("\t [{0:0.2f}, {1:0.2f}] -> {2:0.2f}".format(min(x), max(x), max(x) - min(x)))
            data.append(x)
            total += max(x) - min(x)
            res.append(np.percentile(x, 50))
        # print("\t {0:0.2f}".format(total))
        return res[:-3], res[-3], res[-2], res[-1]

    def name(self):
        return "ball_walk"