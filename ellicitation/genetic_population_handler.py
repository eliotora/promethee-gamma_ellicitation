from random import random, choice
import numpy as np
from genetic_approx import GeneticSolution
from query_selector import *


class GeneticPopulationHandler:
    mutationProb = 0.2

    def __init__(self, pop_size, A, pref_fct, query_selector, phi_c):
        self.asked_pref = [[0 for _ in range(len(A))] for _ in range(len(A))]
        self.gen_nbr = 50
        self.A = A
        self.phi_c = phi_c
        self.pref_fct = pref_fct
        self.query_selector = query_selector
        self.population = []
        for i in range(pop_size):
            Pf = random() * 5
            indT = random() / 5
            incT = max(0.15, indT) + random() / 5
            w = [random() for _ in range(len(pref_fct))]
            w = [i / sum(w) for i in w]
            self.population.append(GeneticSolution(w, indT, incT, Pf, A, pref_fct))

    def evalPop(self, ):
        for e in self.population:
            e.evaluate(self.asked_pref)
        self.population.sort(key=lambda e: e.fitness)

    def nextGen(self):
        newGen = []
        while len(newGen) < len(self.population):
            # parent1, parent2 = self.mixedSelection()
            parent1, parent2 = self.tournamentSelect(), self.tournamentSelect()
            # parent1, parent2 = self.rouletteSelect(), self.rouletteSelect()
            child = self.crossover(parent1, parent2)
            # child = self.crossover2(parent1, parent2)
            if random() <= self.mutationProb:
                child.mutate()
            child.evaluate(self.asked_pref)
            newGen.append(child)

        totalPop = self.population + newGen
        totalPop.sort(key=lambda e: e.fitness)
        self.population = totalPop[len(totalPop)//2:]

    def tournamentSelect(self):
        """
        Tournament selection between two random element of population
        :return: two parents
        """
        parent1 = choice(self.population)
        parent2 = choice(self.population)

        while parent1 == parent2:
            parent2 = choice(self.population)

        return parent1 if parent1.fitness >= parent2.fitness else parent2

    def rouletteSelect(self, exception=None):
        """
        Biased roulette selection
        :return: one parent
        """
        if exception != None:
            population = self.population[:]
            population.remove(exception)
        else:
            population = self.population
        fitnessSum = sum([e.fitness for e in population])

        normalizedProportion = [e.fitness / fitnessSum for e in population]
        cumulTotal = 0
        normalizedProb = []
        for e in normalizedProportion:
            cumulTotal += e
            normalizedProb.append(cumulTotal)

        selectVal = random()
        res = None

        for i in range(len(population)):
            if normalizedProb[i] >= selectVal:
                res = population[i]

        if res is None:
            print("Roulette Failed")
            raise Exception

        return res

    def mixedSelection(self):
        """
        50% chance for tournament selection
        50% chance for biased roulette selection
        :return: two parents
        """
        if random() < 0.5:
            p1 = self.tournamentSelect()
            p2 = self.tournamentSelect()
            while p1 == p2:
                p2 = self.tournamentSelect()
            return p1, p2
        else:
            p1 = self.rouletteSelect()
            p2 = self.rouletteSelect(exception=p1)
            while p1 == p2:
                print("Arggg")
                p2 = self.rouletteSelect()
            return p1, p2

    def crossover(self, p1:GeneticSolution, p2:GeneticSolution):
        """
        Crossover operator between two parents
        :param p1: an element of the current population
        :param p2: a different element of the current population
        :return: a new solution based on the genome of the two parents
        """
        w_new = [(p1.weights[i] + p2.weights[i]) / 2 for i in range(len(p1.weights))]
        indT_new = (p1.Ti + p2.Ti) / 2
        incT_new = (p1.Tj + p2.Tj) / 2
        Pf = (p1.prefFactor + p2.prefFactor) / 2
        return GeneticSolution(w_new, indT_new, incT_new, Pf, self.A, self.pref_fct)

    def crossover2(self, p1:GeneticSolution, p2:GeneticSolution):
        """
        Crossover operator between two parents
        :param p1: an element of the current population
        :param p2: a different element of the current population
        :return: a new solution based on the genome of the two parents
        """
        mixing_genome = [0 if random() < 0.5 else 1 for _ in range(len(p1.weights))]
        w_new = [p1.weights[i] if mixing_genome[i] == 0 else p2.weights[i] for i in mixing_genome[:-3]]
        w_new = [w/sum(w_new) for w in w_new]
        which = random()
        indT_new = p1.Ti if which < 0.5 else p2.Ti
        incT_new = p1.Tj if which < 0.5 else p2.Tj
        Pf = p1.prefFactor if which < 0.5 else p2.prefFactor
        return GeneticSolution(w_new, indT_new, incT_new, Pf, self.A, self.pref_fct)

    def next_query(self):
        if self.query_selector == vote_based_query:
            return self.query_selector(self.A, self.population)
        elif self.query_selector == discrimination_power_based_query:
            phic = self.population[0].handler.phis_c
            samples = [p.weights + [p.Ti] + [p.Tj] + [p.prefFactor] for p in self.population]
            return self.query_selector(phic, samples)

    def assimilate_query(self, i, j, answer):
        self.asked_pref[i][j] = answer
        best = sum([1 for i in range(len(self.asked_pref)) for j in range(len(self.asked_pref)) if self.asked_pref[i][j] != 0])

        self.evalPop()
        for g in range(self.gen_nbr):
            self.nextGen()
            worst = min(self.population, key=lambda e: e.fitness)
            if worst.fitness == best:
                break
        return self.analyse_sample()

    def getSolution(self):
        return self.population[-1]

    def analyse_sample(self):
        data = []
        res = []
        total = 0
        samples = [[w for w in p.weights] + [p.Ti, p.Tj, p.prefFactor] for p in self.population]
        for c in range(len(samples[0])):
            x = [s[c] for s in samples]
            data.append(x)
            total += max(x) - min(x)
            res.append(np.percentile(x, 50))
        return res[:-3], res[-3], res[-2], res[-1]

    def name(self):
        return "genetic"