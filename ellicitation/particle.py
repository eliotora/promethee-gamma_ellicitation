from random import random

from promethee_gamma import PrometheeGammaInstance
from copy import *
import numpy as np


class Particle:
    def __init__(self, w, indT, incT, Pf, A, prefFun, acceleration_coefs=None):
        if acceleration_coefs is None:
            acceleration_coefs = [2, 2]
        self.weights = w
        self.Ti = indT
        self.Tj = incT
        self.Pf = Pf
        self.position = w + [self.Ti, self.Tj, self.Pf]
        self.handler = PrometheeGammaInstance(A, w, prefFun, indT, incT, Pf)
        self.velocity = [0 for _ in w] + [0, 0, 0]
        self.personal_best = deepcopy(self.position)
        self.personal_best_fitness = 0
        self.global_best = None
        self.fitness = 0
        self.acoef1 = acceleration_coefs[0]
        self.acoef2 = acceleration_coefs[1]

    def evaluate(self, knownPref):
        computedPref = self.handler.pref
        self.fitness = 0
        for i in range(len(knownPref)):
            for j, pref in enumerate(knownPref[i]):
                if pref == 0:
                    pass
                elif pref == computedPref[i][j]:
                    self.fitness += 1
        if self.fitness > self.personal_best_fitness:
            self.personal_best_fitness = self.fitness
            self.personal_best = deepcopy(self.position)
        return self.fitness

    def update_global_best(self, global_best):
        self.global_best = global_best

    def move(self):
        dim = len(self.position)
        speed1 = np.eye(dim) * np.array([random() for _ in range(dim)])
        speed2 = np.eye(dim) * np.array([random() for _ in range(dim)])
        self.velocity += (self.acoef1 * speed1.dot((self.personal_best - self.position)) +
                          self.acoef2 * speed2.dot((self.global_best - self.position)))
        self.position += self.velocity
