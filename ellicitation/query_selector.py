import numpy as np
import scipy.stats as ss


def vote_based_query(A, population):
    best_to_query = [0, 0, 0]
    for i in range(len(A)):
        for j in range(len(A)):
            votes = [1, 1, 1, 1]
            for solution in population:
                votes[solution.handler.pref[i][j] - 1] += 1
            # disagreement = np.sqrt(votes[0] ** 2 + votes[1] ** 2 + votes[2] ** 2 + votes[3] ** 2)
            disagreement = (votes[0])*(votes[1])*(votes[2])*(votes[3])
            if disagreement > best_to_query[2]:
                best_to_query = [i, j, disagreement]
    return best_to_query[:-1]


def discrimination_power_based_query(phi_c, samples, beta=30, alpha=10):
    """
    1. Compute analytical center
    2. The beta with the best netflow are kept
    3. From these the gamma pairs which have the constraint closest to center are kept
    4. ask the question with the pair which split the samples the best
    """

    def compute_center(samples):
        # return analytical_center.compute_center(samples, constraints)
        # old code but necessary since constraint are not linear
        center = [0 for _ in range(len(samples[0]))]
        for sample in samples:
            center = np.add(center, sample)

        center = [ci / len(samples) for ci in center]
        return center

    def beta_best(phi_c, w, beta):
        netflows = [np.dot(phi_c[i], w) for i in range(len(phi_c))]
        neg_netflows = [-s for s in netflows]
        ranks = list(ss.rankdata(neg_netflows))  # Ties are not dealt with
        r = sorted(ranks)
        ranking = [ranks.index(x) for x in r]
        return ranking[:beta]

    def alpha_candidate_queries(phi_c, bests, w_center, alpha):
        n = len(bests)
        # origin = [0 for c in range(len(phi_c[0]))]
        distances = []
        for x, i in enumerate(bests):
            for j in bests[x + 1:]:
                constraint_point = np.subtract(phi_c[i], phi_c[j])
                distance = abs(np.dot(constraint_point, w_center)) / np.linalg.norm(constraint_point)
                distances.append((distance, i, j))

        # distances.sort(reverse=True) # replace by true because we want closest to the center
        distances.sort()  # replace by true because we want closest to the center
        # print(distances)
        candidates = distances[:alpha]
        return [(c[1], c[2]) for c in candidates]

    def most_discriminating_query(phi_c, queries, samples):
        def compute_score_new(query, samples, delta_phis):
            # for each possible answer, how much is the largest remaining range reduced ?
            remainings = [[] for i in range(4)]

            for point in samples:
                gamma_ij, gamma_ji = 0, 0
                for c in range(len(delta_phis)):
                    if delta_phis[c] > 0:
                        gamma_ij += delta_phis[c] * point[c]
                    else:
                        gamma_ji -= delta_phis[c] * point[c]  # since delta_phis negative
                if gamma_ij <= point[-3] and gamma_ji <= point[-3]:
                    remainings[2].append(point)
                elif gamma_ij >= point[-2] and gamma_ji >= point[-2]:
                    remainings[3].append(point)
                elif np.dot(point[:-3], delta_phis) > 0:
                    remainings[0].append(point)
                else:
                    remainings[1].append(point)

            scores = []
            for rel_remaining_points in remainings:
                if len(rel_remaining_points) == 0:
                    continue

                score_rel = []
                for c in range(len(samples[0])):
                    parameter_values = [v[c] for v in rel_remaining_points]
                    # if len(parameter_values) > 0:
                    score_rel.append(max(parameter_values) - min(parameter_values))
                    # else:
                    # s += 1

                scores.append(sum(score_rel))

            # print("\t\tQuery:", query, ["{0:0.2f}".format(s) for s in scores], np.mean(scores), [len(r) for r in remainings])

            return np.mean(scores)

        k = len(phi_c[0])
        best_query, best_score = queries[0], 1000000
        for query in queries:
            i, j = query
            delta_phis = [phi_c[i][c] - phi_c[j][c] for c in range(k)]
            # constraint_B = [phi_c[j][c] - phi_c[i][c] for c in range(k)] + [0, 0]

            # why this np.dot ? should we check if positive or negative ?
            # remaining = sum(np.dot(point[:2], constraint) for point in samples)
            # remaining = sum([1 for point in samples if np.dot(point[:2], delta_phis) > 0])
            # shouldn't we check what happens if incomparability or indifference ?
            # score = min(remaining, len(samples)-remaining)
            score = compute_score_new(query, samples, delta_phis)

            # score = compute_score(query, samples, delta_phis)
            if score < best_score:
                best_query, best_score = query, score
            # print(i,j, remaining)

        return best_query

    # print("next query: ")
    w_center = compute_center(samples)  # to adapt using analytical center -> see analytical_center2.py
    w_center = w_center[:-3]
    #   print("\t center:", list(w_center))

    bests = beta_best(phi_c, w_center, beta)
    # print("\t bests:", bests)
    query_candidates = alpha_candidate_queries(phi_c, bests, w_center, alpha)
    # print("\t query_candidates:", query_candidates)
    query = most_discriminating_query(phi_c, query_candidates, samples)
    # print("\t query: ", query)

    return query
