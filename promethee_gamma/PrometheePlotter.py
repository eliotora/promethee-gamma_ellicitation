import matplotlib.pyplot as plt

nP = 4
P = 3
J = 2
I = 1
class PrometheePlotter:
    def __init__(self):
        pass

    def plot_gammas(self, gammas, pref, Pf, Ti, Tj):
        gammax = max([max(gamma) for gamma in gammas])
        plt.figure(figsize=(7, 7))
        plt.plot([0, 0], [0, gammax], "k-", [0, gammax], [0, 0], "k-", [Ti, Tj], [Ti, Tj], "r-")
        plt.plot([0, Ti], [Ti * Pf / (Pf + 1), Ti], "b-", [Ti * Pf / (Pf + 1), Ti], [0, Ti], "b-")
        plt.plot([Tj, gammax], [Tj, (gammax + Pf * Tj) / (1 + Pf)], "g-", [Tj, (gammax + Pf * Tj) / (1 + Pf)],
                 [Tj, gammax], "g-")

        for i in range(len(pref)):
            for j in range(i + 1, len(pref)):
                if pref[i][j] == I:
                    plt.plot(gammas[i][j], gammas[j][i], "bo")
                elif pref[i][j] == J:
                    plt.plot(gammas[i][j], gammas[j][i], "go")
                elif pref[i][j] == P or pref[i][j] == nP:
                    plt.plot(gammas[i][j], gammas[j][i], "ro")
        plt.show()


if __name__ == "__main__":
    plot = PrometheePlotter()
    plot.plot_gammas([[1.25]], 0, 0, 0, 2, 0.15, 0.5)
