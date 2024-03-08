from copy import deepcopy
from random import random

from ellicitation.particle import Particle
from ellicitation.query_selector import *


class ParticleHandler:
    def __init__(self, particle_nbr, A, pref_fct, query_selector, phis_c):
        self.asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]
        self.iterations = 100
        self.inertia = 1
        self.min_inertia = 0.4
        self.inertia_reduction = (1 - self.min_inertia)/self.iterations
        # self.inertia_reduction = 0
        self.A = A
        self.phis_c = phis_c
        self.pref_fct = pref_fct
        self.query_selector = query_selector
        self.particle_nbr = particle_nbr
        self.particles = []
        self.global_best = []
        self.global_best_fitness = -1
        self.acceleration_coefs = [0.1, 0.2]
        for i in range(particle_nbr):
            Pf = random() * 5
            indT = random() / 5
            incT = max(0.15, indT) + random() / 5
            w = [random() for _ in range(len(pref_fct))]
            w = [i / sum(w) for i in w]
            self.particles.append(Particle(w, indT, incT, Pf, A, pref_fct, self.acceleration_coefs))

    def eval_particles(self):
        if self.mean_distance() < 0.0001:
            self.particles = [self.particles[-1]]
            self.refill_particles()
        for p in self.particles:
            f = p.evaluate(self.asked_pref)
            if f > self.global_best_fitness:
                print("New best fitness", f)
                self.global_best_fitness = f
                self.global_best = deepcopy(p.position)
                for p in self.particles:
                    p.update_global_best(self.global_best)
        self.particles.sort(key=lambda p: p.fitness)
        # print("\nWeights: Pos: ", self.particles[-1].position[:-3], "   Velocity: ", self.particles[-1].velocity[:-3],
        #       "\nTi: Pos:", self.particles[-1].position[-3], "   Velocity: ", self.particles[-1].velocity[-3],
        #       "\nTj: Pos:", self.particles[-1].position[-2], "   Velocity: ", self.particles[-1].velocity[-2],
        #       "\nPf: Pos:", self.particles[-1].position[-1], "   Velocity: ", self.particles[-1].velocity[-1])


    def mean_distance(self):
        distances = []
        for p1 in self.particles:
            for p2 in self.particles:
                if p1 != p2:
                    distances.append(np.linalg.norm(p1.position - p2.position))
        return np.mean(distances)

    def refill_particles(self):
        while len(self.particles) < self.particle_nbr:
            Pf = random() * 5
            indT = random() / 5
            incT = max(0.15, indT) + random() / 5
            w = [random() for _ in range(len(self.pref_fct))]
            w = [i / sum(w) for i in w]
            self.particles.append(Particle(w, indT, incT, Pf, self.A, self.pref_fct, self.acceleration_coefs))
            self.particles[-1].update_global_best(self.global_best)

    def move(self):
        if self.inertia > self.min_inertia:
            self.inertia -= self.inertia_reduction
        for p in self.particles:
            p.move()
            p.set_inertia(self.inertia)
            f = p.evaluate(self.asked_pref)
            if f > self.global_best_fitness:
                print("New best fitness!", f)
                self.global_best_fitness = f
                self.global_best = deepcopy(p.position)
                for p in self.particles:
                    p.update_global_best(self.global_best)
        print("Average distance this time: ", np.average([np.linalg.norm(p.velocity) for p in self.particles]))
        self.inertia = 1

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
            # print("Worst: ", worst.fitness, "\t Best: ", best)
            print("Average fitness at it {}: ".format(it), np.average([p.fitness for p in self.particles]), "\t over ", best)
            if worst.fitness == best:
                print("Broke after {} iterations".format(it))
                break
        # for p in self.particles: p.reset_inertia()
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