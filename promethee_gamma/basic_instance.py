from PrometheePlotter import PrometheePlotter, I, J, P, nP

class BasicInstance:
    phi_flag = False

    def __init__(self, A, pref_fct):
        self.A = A
        self.size = len(A)
        self.pref_fct = pref_fct
        self.phis_c = [[0 for _ in self.pref_fct] for _ in range(self.size)]

    def compute_phis_c(self):
        for ai, a in enumerate(self.A):
            for ci, c in enumerate(self.pref_fct):
                phi = 0
                for b in self.A:
                    phi += self.pref_fct[ci].value(a[ci] - b[ci]) - self.pref_fct[ci].value(b[ci] - a[ci])
                phi /= len(self.A) - 1
                self.phis_c[ai][ci] = phi
        self.phi_flag = True

    def compute_gammas(self, w):
        gammas = [[0 for _ in range(self.size)] for _ in range(self.size)]
        if not self.phi_flag: self.compute_phis_c()
        for (ai, a) in enumerate(self.A):
            for (bi, b) in enumerate(self.A):
                gamma = 0
                for (c, weight) in enumerate(w):
                    if a[c] > b[c]:
                        gamma += weight * (self.phis_c[ai][c] - self.phis_c[bi][c])
                gammas[ai][bi] = gamma
        return gammas

    def compute_indicators(self, gammas, Ti, Tj, Pf):
        indicators = [[[0, 0, 0, 0] for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                indicators[i][j][0] = Ti - max(gammas[i][j], gammas[j][i])
                indicators[i][j][1] = min(gammas[i][j], gammas[j][i]) - Tj
                indicators[i][j][2] = (gammas[i][j] - gammas[j][i]) / Pf
                indicators[i][j][3] = -indicators[i][j][2]
        return indicators

    def compute_preferences(self, w, Ti, Tj, Pf):
        gammas = self.compute_gammas(w)
        indicators = self.compute_indicators(gammas, Ti, Tj, Pf)
        return self.prefs_from_indicators(indicators)

    def prefs_from_indicators(self, indicators):
        prefs = [[0 for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                if (indicators[i][j][0] >= max(indicators[i][j][2], indicators[i][j][3])) or (
                        indicators[i][j][1] <= 0 and indicators[i][j][2] <= 0 and indicators[i][j][3] <= 0):
                    prefs[i][j] = I
                elif indicators[i][j][1] >= max(indicators[i][j][2], indicators[i][j][3]):
                    prefs[i][j] = J
                elif indicators[i][j][2] >= indicators[i][j][3]:
                    prefs[i][j] = P
                else:
                    prefs[i][j] = nP
        return prefs