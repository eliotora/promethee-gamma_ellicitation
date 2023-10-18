from instance_reader import load_dataset
import preference_functions as pf


class PrometheeGammaInstance:
    gamma_flag = False
    phi_flag = False
    pref_flag = False

    def __init__(self, Alt, wts, pref_fun, indifference_threshold=0.15, incomparability_threshold=0.15, pref_factor=1):
        self.A = Alt  # Alternatives
        self.w = wts  # weights
        self.pref_fct = pref_fun  # preference functions
        self.gammas = [[0 for _ in A] for _ in A]
        self.phis_c = [[0 for _ in w] for _ in A]
        self.I = [[False for _ in A] for _ in A]
        self.J = [[False for _ in A] for _ in A]
        self.P = [[False for _ in A] for _ in A]
        self.Ti = indifference_threshold
        self.Tj = incomparability_threshold
        self.Pf = pref_factor

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
                self.gammas[a][b] = gamma
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
                self.phis_c[a][c] = phi
        self.phi_flag = True

    def compute_preferences(self):
        if not self.gamma_flag: self.compute_gammas()
        rel_ij = [0, 0, 0, 0]

        for i in range(len(self.gammas)):
            for j in range(len(self.gammas[i + 1:])):
                rel_ij[0] = self.Ti - max(self.gammas[i][j], self.gammas[j][i])
                rel_ij[1] = min(self.gammas[i][j], self.gammas[j][i]) - self.Tj
                rel_ij[2] = (self.gammas[i][j] - self.gammas[j][i]) / self.Pf
                rel_ij[3] = - rel_ij[2]
                if (rel_ij[0] >= max(rel_ij[2], rel_ij[3])) or (rel_ij[1] <= 0 and rel_ij[2] <= 0 and rel_ij[3] <= 0):
                    self.I[i][j] = True
                elif rel_ij[1] >= max(rel_ij[2], rel_ij[3]):
                    self.J[i][j] = True
                elif rel_ij[2] >= rel_ij[3]:
                    self.P[i][j] = True
                else:
                    self.P[j][i] = True
        self.pref_flag = True


if __name__ == "__main__":
    dataset = "data/HDI20_Classic"
    A, w, pref_fct_desc = load_dataset(dataset)
    pref_fct = [pf.make_pref_fct(c["type"], c["ceils"]) for c in pref_fct_desc]

    instance = PrometheeGammaInstance(A, w, pref_fct)
    instance.compute_gammas()
    print(instance.gammas)
