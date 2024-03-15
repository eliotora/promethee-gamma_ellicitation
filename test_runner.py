import random

import numpy as np

from ellicitation.elicitation_procedure import elicitationProcedure
from ellicitation.genetic_population_handler import GeneticPopulationHandler
from ellicitation.ball_walk_method import SampleBasedProcedure
from ellicitation.particle_handler import ParticleHandler
from ellicitation.query_selector import discrimination_power_based_query, vote_based_query, votes_with_percentages, \
    votes_with_scores
import os
from multiprocessing import Process, Pool

from instance_reader import load_dataset
import preference_functions as pf
import time

procedures_dict = {
    SampleBasedProcedure.__name__: SampleBasedProcedure,
    GeneticPopulationHandler.__name__: GeneticPopulationHandler,
    ParticleHandler.__name__: ParticleHandler
}

query_selector_dict = {
    discrimination_power_based_query.__name__: discrimination_power_based_query,
    vote_based_query.__name__: vote_based_query,
    votes_with_percentages.__name__: votes_with_percentages,
    votes_with_scores.__name__: votes_with_scores,
}

SHA_Q13 = "data/SHA_1and3_quartiles"
HDI_Q13 = "data/HDI_1and3_quartiles"
HDI_20 = "data/HDI20_Classic"
EPI2020_Q13 = "data/EPI2020_1and3_quartiles"
TIMES_Q13 = "data/TIMES_1and3_quartiles"
datasets = [SHA_Q13, HDI_Q13, HDI_20, EPI2020_Q13, TIMES_Q13]

size = 100
query_nbr = 20

def run_config_test(procedure, query, dataset, seed):
    # procedure, query, dataset, seed = config
    A, w, pref_fct_desc = load_dataset(dataset)
    pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]
    random.seed(seed)
    np.random.seed(seed)
    random.shuffle(A)

    start = time.time()

    w, Ti, Tj, Pf, accuracies = elicitationProcedure(A, pref_fct, query_nbr, size, procedure, query)

    end = time.time()
    elapsed = end - start

    for ai, a in enumerate(accuracies):
        with open("test_results.csv", "a") as f:

            values = [
                procedure.__name__,
                query.__name__,
                dataset.strip("data/"),
                seed,
                elapsed,
                a,
                ai,
            ]
            f.write(",".join(map(str, values)) + "\n")


def run_test(file_path):
    try:
        with open("tests_done.txt", "r") as file:
            data_done = file.readlines()
            for i in range(len(data_done)):
                data_done[i] = data_done[i].strip('\n')
            print(data_done)
    except FileNotFoundError:
        file = open("tests_done.txt", "w")
        file.close()
        data_done = []

    with open("test_results.csv", "w") as f:
        f.write(
            ",".join(
                [
                    "procedure",
                    "query_selector",
                    "dataset",
                    "seed",
                    "elapsed_time",
                    "accuracy",
                    "query_nbr",
                ]
            ) + "\n"
        )

    process_nbr = 10
    processes = []


    with open(file_path, "r", newline="") as file:
        data_todo = file.readlines()
        while len(data_todo) > 0:
            row = data_todo.pop(0)
            row_striped = row.strip('\r\n')
            if row_striped not in data_done:
                content = row_striped.split(", ")
                for dataset in datasets:
                    config = [procedures_dict[content[0]], query_selector_dict[content[1]], dataset, int(content[2])]
                    processes.append(Process(target=run_config_test, args=config))

    for i in range(len(processes)//10):
        for p in processes[i*10:i*10+10]:
            p.start()

        for p in processes[i*10:i*10+10]:
            p.join()

    # pool.close()
    # with open("tests_done.txt", "a", newline="") as file:
    #     file.write(row)


    # os.remove("tests_done.txt")
    os.remove(file_path)


if __name__ == "__main__":
    run_test("todo_tests.txt")
