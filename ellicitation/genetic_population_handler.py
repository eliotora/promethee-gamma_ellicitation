from random import random, choice

from genetic_approx import GeneticSolution


class GeneticPopulationHandler:
    mutationProb = 0.2

    def __init__(self, pop_size, A, pref_fct):
        self.A = A
        self.pref_fct = pref_fct
        self.population = []
        for i in range(pop_size):
            Pf = random() * 5
            indT = random() / 5
            incT = max(0.15, indT) + random() / 5
            w = [random() for _ in range(len(pref_fct))]
            w = [i / sum(w) for i in w]
            self.population.append(GeneticSolution(w, indT, incT, Pf, A, pref_fct))

    def evalPop(self, knownPref):
        for e in self.population:
            e.evaluate(knownPref)
        self.population.sort(key=lambda e: e.fitness)

    def nextGen(self, knownPref):
        newGen = []
        while len(newGen) < len(self.population):
            # parent1, parent2 = self.mixedSelection()
            parent1, parent2 = self.tournamentSelect(), self.tournamentSelect()
            # parent1, parent2 = self.rouletteSelect(), self.rouletteSelect()
            child = self.crossover(parent1, parent2)
            # child = self.crossover2(parent1, parent2)
            if random() <= self.mutationProb:
                child.mutate()
            child.evaluate(knownPref)
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
        mixing_genome = [0 if random() < 0.5 else 1 for _ in range(len(p1.weights) + 3)]
        w_new = [p1.weights[i] if mixing_genome[i] == 0 else p2.weights[i] for i in mixing_genome[:-3]]
        indT_new = p1.Ti if mixing_genome[len(p1.weights)] == 0 else p2.Ti
        incT_new = p1.Tj if mixing_genome[len(p1.weights)+1] == 0 else p2.Tj
        Pf = p1.prefFactor if mixing_genome[-1] == 0 else p2.prefFactor
        return GeneticSolution(w_new, indT_new, incT_new, Pf, self.A, self.pref_fct)
