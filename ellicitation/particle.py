from random import random

from basic_instance import BasicInstance
from promethee_gamma import PrometheeGammaInstance
from copy import *
import numpy as np


class Particle:
    def __init__(self, w, indT, incT, Pf, A, prefFun, acceleration_coefs=None):
        if acceleration_coefs is None:
            acceleration_coefs = [2, 2]
        self.weights = w
        self.inertia = 1
        self.Ti = indT
        self.Tj = incT
        self.Pf = Pf
        self.position = np.array(w + [self.Ti, self.Tj, self.Pf])
        self.handler = PrometheeGammaInstance(A, w, prefFun, indT, incT, Pf)
        self.handler = BasicInstance(A, prefFun)
        self.velocity = np.array([0 for _ in w] + [0, 0, 0]).astype("float64")
        self.personal_best = deepcopy(self.position)
        self.personal_best_fitness = 0
        self.global_best = None
        self.global_best_fitness = 0
        self.fitness = 0
        self.acoef1 = acceleration_coefs[0]
        self.acoef2 = acceleration_coefs[1]
        self.indicators = self.handler.compute_indicators(self.handler.compute_gammas(self.weights), self.Ti, self.Tj, self.Pf)
        self.pref = self.handler.prefs_from_indicators(self.indicators)


    def evaluate(self, knownPref):
        self.indicators = self.handler.compute_indicators(self.handler.compute_gammas(self.weights), self.Ti, self.Tj, self.Pf)
        self.pref = self.handler.prefs_from_indicators(self.indicators)
        self.fitness = 0
        for i in range(len(knownPref)):
            for j, pref in enumerate(knownPref[i]):
                if pref == 0:
                    pass
                elif pref == self.pref[i][j]:
                    self.fitness += 1
        if self.fitness >= self.personal_best_fitness:
            self.personal_best_fitness = self.fitness
            self.personal_best = deepcopy(self.position)
        return self.fitness

    def update_global_best(self, global_best, fitness):
        self.global_best = global_best
        self.global_best_fitness = fitness

    def move(self):
        dim = len(self.position)
        speed1 = np.eye(dim) * np.array([random() for _ in range(dim)])
        speed2 = np.eye(dim) * np.array([random() for _ in range(dim)])
        self.velocity = (self.velocity * self.inertia +
                         (self.personal_best_fitness - self.fitness) * self.acoef1 * speed1.dot((self.personal_best - self.position)) +
                         (self.global_best_fitness - self.fitness) * self.acoef2 * speed2.dot((self.global_best - self.position)))
        self.position += self.velocity
        if self.position[-3] < 0:
            self.position[-3] = 0
        if self.position[-2] < self.position[-3]:
            self.position[-2] = self.position[-3]
        if self.position[-1] <= 0:
            self.position[-1] = 0.001
        for i in range(len(self.position[:-3])):
            if self.position[i] < 0:
                self.position[i] = 0
        self.position = np.append(np.array([w/sum(self.position[:-3]) for w in self.position[:-3]]), self.position[-3:])
        self.weights = self.position[:-3]
        self.Ti = self.position[-3]
        self.Tj = self.position[-2]
        self.Pf = self.position[-1]

        # print("After: ", self.position)
        # self.check_constraints()

    def check_constraints(self):
        w = self.position[:-3]
        Ti = self.position[-3]
        Tj = self.position[-2]
        Pf = self.position[-1]
        for weight in w:
            if weight <0:
                print("Weight: ", weight)
        print(sum(w))
        if Ti < 0 or Tj < Ti or Pf <= 0:
            print("Error on parameters")

    def set_inertia(self, inertia):
        self.inertia = inertia

    def reset_inertia(self):
        self.inertia = 1

    def reset_velocity(self):
        self.velocity = np.array([0 for _ in self.weights] + [0, 0, 0]).astype("float64")