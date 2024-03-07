from copy import deepcopy
from random import random

from ellicitation.particle import Particle
from ellicitation.query_selector import *


class ParticleHandler:
    def __init__(self, particle_nbr, A, pref_fct, query_selector, phis_c):
        self.asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]
        self.iterations = 100
        self.A = A
        self.phis_c = phis_c
        self.pref_fct = pref_fct
        self.query_selector = query_selector
        self.particles = []
        self.global_best = []
        self.global_best_fitness = -1
        acceleration_coefs = [0.1, 0.1]
        for i in range(particle_nbr):
            Pf = random() * 5
            indT = random() / 5
            incT = max(0.15, indT) + random() / 5
            w = [random() for _ in range(len(pref_fct))]
            w = [i / sum(w) for i in w]
            self.particles.append(Particle(w, indT, incT, Pf, A, pref_fct, acceleration_coefs))

    def eval_particles(self):
        for p in self.particles:
            f = p.evaluate(self.asked_pref)
            if f > self.global_best_fitness:
                self.global_best_fitness = f
                self.global_best = deepcopy(p.position)
                for p in self.particles:
                    p.update_global_best(self.global_best)
        self.particles.sort(key=lambda p: p.fitness)

    def move(self):
        for p in self.particles:
            p.move()
            f = p.evaluate(self.asked_pref)
            if f > self.global_best_fitness:
                self.global_best_fitness = f
                self.global_best = deepcopy(p.position)
                for p in self.particles:
                    p.update_global_best(self.global_best)

    def next_query(self):
        if self.query_selector.__name__ == vote_based_query.__name__ or self.query_selector.__name__ == votes_with_percentages.__name__:
            return self.query_selector(self.A, self.particles)
        elif self.query_selector.__name__ == discrimination_power_based_query.__name__:
            phic = self.particles[0].handler.phis_c
            samples = [p.weights + [p.Ti] + [p.Tj] + [p.Pf] for p in self.particles]
            return self.query_selector(phic, samples)

    def assimilate_query(self, i, j, answer):
        self.asked_pref[i][j] = answer
        best = sum([1 for i in range(len(self.asked_pref)) for j in range(len(self.asked_pref)) if self.asked_pref[i][j] != 0])

        self.eval_particles()
        for it in range(self.iterations):
            self.move()
            worst = min(self.particles, key=lambda p: p.fitness)
            if worst.fitness == best:
                break
        return self.analyse_sample()

    def getSolution(self):
        return self.particles[-1]

    def analyse_sample(self):
        data = []
        res = []
        total = 0
        samples = [p.position for p in self.particles]
        for c in range(len(samples[0])):
            x = [s[c] for s in samples]
            data.append(x)
            total += max(x) - min(x)
            res.append(np.percentile(x, 50))
        return res[:-3], res[-3], res[-2], res[-1]

    def name(self):
        return 'particles'