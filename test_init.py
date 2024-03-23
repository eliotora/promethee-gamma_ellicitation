from ellicitation.genetic_population_handler import GeneticPopulationHandler
from ellicitation.ball_walk_method import SampleBasedProcedure
from ellicitation.query_selector import *
from ellicitation.particle_handler import ParticleHandler

procedures_dict = {
    # SampleBasedProcedure.__name__: SampleBasedProcedure,
    # GeneticPopulationHandler.__name__: GeneticPopulationHandler,
    ParticleHandler.__name__: ParticleHandler
}

query_selector_dict = {
    discrimination_power_based_query.__name__: discrimination_power_based_query,
    vote_based_query.__name__: vote_based_query,
    votes_with_percentages.__name__: votes_with_percentages,
    votes_with_scores.__name__: votes_with_scores,
}

def init_tests(methods, test_nbr):
    with open("todo_tests.txt", "w") as file:
        for method in methods:
            for test in range(test_nbr):
                file.write(", ".join([e.__name__ for e in method]) + ", " + str(test) + "\n")


if __name__ == "__main__":
    procedures = list(procedures_dict.values())
    queries = list(query_selector_dict.values())
    methods = [[p, q] for p in procedures for q in queries]
    init_tests(methods, 10)
