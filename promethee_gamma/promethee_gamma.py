from instance_reader import load_dataset
import preference_functions as pf
from PrometheePlotter import PrometheePlotter


class PrometheeGammaInstance:
    gamma_flag = False
    phi_flag = False
    pref_flag = False

    def __init__(self, Alt, wts, pref_fun, indifference_threshold=0.15, incomparability_threshold=0.15, pref_factor=1):
        self.A = Alt  # Alternatives
        self.w = wts  # weights
        self.pref_fct = pref_fun  # preference functions
        self.gammas = [[0 for _ in self.A] for _ in self.A]
        self.phis_c = [[0 for _ in self.w] for _ in self.A]
        self.pref = [[0 for _ in self.A] for _ in self.A]
        self.Ti = indifference_threshold
        self.Tj = incomparability_threshold
        self.Pf = pref_factor
        self.plotter = PrometheePlotter()

    def compute_gammas(self):
        """
        Compute a matrix nxn of gamma values
        """
        if not self.phi_flag: self.compute_phis_c()
        for (ai, a) in enumerate(self.A):
            for (bi, b) in enumerate(self.A):
                gamma = 0
                for (c, weight) in enumerate(self.w):
                    if a[c] > b[c]:
                        gamma += weight * (self.phis_c[ai][c] - self.phis_c[bi][c])
                self.gammas[ai][bi] = gamma
        self.gamma_flag = True

    def compute_phis_c(self):
        """
        Compute a matrix of phis, each element [a][c] is a phi_c for the alternative a over the criterion c
        """
        for ai, a in enumerate(self.A):
            for c, weight in enumerate(self.w):
                phi = 0
                for b in self.A:
                    phi += self.pref_fct[c].value(a[c] - b[c]) - self.pref_fct[c].value(b[c] - a[c])
                phi /= len(self.A) - 1
                self.phis_c[ai][c] = phi
        self.phi_flag = True

    def compute_preferences(self):
        if not self.gamma_flag: self.compute_gammas()
        rel_ij = [0, 0, 0, 0]

        for i in range(len(self.gammas)):
            for j in range(len(self.gammas)):
                rel_ij[0] = self.Ti - max(self.gammas[i][j], self.gammas[j][i])
                rel_ij[1] = min(self.gammas[i][j], self.gammas[j][i]) - self.Tj
                rel_ij[2] = (self.gammas[i][j] - self.gammas[j][i]) / self.Pf
                rel_ij[3] = - rel_ij[2]
                if (rel_ij[0] >= max(rel_ij[2], rel_ij[3])) or (rel_ij[1] <= 0 and rel_ij[2] <= 0 and rel_ij[3] <= 0):
                    self.pref[i][j] = 1
                elif rel_ij[1] >= max(rel_ij[2], rel_ij[3]):
                    self.pref[i][j] = 2
                elif rel_ij[2] >= rel_ij[3]:
                    self.pref[i][j] = 3
                else:
                    self.pref[i][j] = 4
        self.pref_flag = True

    def plot(self):
        self.plotter.plot_gammas(self.gammas, self.pref, self.Pf, self.Ti, self.Tj)


if __name__ == "__main__":
    # dataset = "data/HDI20_Classic"
    # dataset = "data/SHA_TOP15"
    dataset = "data/HDI20_1and3_quartiles"
    A, w, pref_fct_desc = load_dataset(dataset)
    pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]

    instance = PrometheeGammaInstance(A, w, pref_fct, 0.15, 0.15, 4)
    instance.compute_preferences()

    instance.plot()
