import numpy as np


class Base:
    """
    Pinel, P. 2003. Amelioration, Validation et Implantation D'un Algorithme de Calcul pour Evaluer le Transfert Thermique Dans les Puits Verticaux de Systemes de Pompes a Chaleur Geothermiques. M.S.Sc. Thesis. Ecole Polytechnique Montreal

    ** Bernier, M.A., Labib, R., Pinel, P., and Paillot, R. 2004. 'A multiple load aggregation algorithm for annual hourly simulations of GCHP systems.' HVAC&R Research, 10(4): 471-487.

    ** Equation is referenced here, but it has typos
    """

    def __init__(self):
        pass

    def q1(self, t):
        term_1 = self.A * np.sin(np.pi * (t - self.B) / 12)
        term_2 = np.sin(self.F * np.pi * (t - self.B) / 8760)

        result = term_1 * term_2
        if self.print_output: print("q1: %f" % (result))

        return result

    def q2(self, t):
        term_1 = (168 - self.C) / 168
        term_2 = 0.0
        for i in range(1, 4):
            term_2 += (np.cos(i * np.pi * self.C / 84) - 1) * (np.sin(i * np.pi * (t - self.B) / 84)) / (i * np.pi)

        result = term_1 + term_2
        if self.print_output: print("q2: %f" % (result))

        return result

    def FL(self, t):
        result = np.floor(self.F * (t - self.B) / 8760)
        if self.print_output: print("FL: %f" % (result))

        return result

    def signum(self, t):
        term_1 = np.cos(self.F * np.pi * (t - self.G) / 4380) + self.E

        if self.print_output: print("SN T1: %f" % (term_1))

        if term_1 >= 0:
            if self.print_output: print("SN: %f" % (1))
            return 1
        else:
            if self.print_output: print("SN: %f" % (-1))
            return -1

    def Q(self, t):
        q1 = self.q1(t)
        q2 = self.q2(t)
        FL = self.FL(t)
        SN = self.signum(t)

        if self.print_output: print("q1 x q2: %f" % (q1 * q2))
        if self.print_output: print("pow(-1.0, FL): %f" % (pow(-1.0, FL)))
        if self.print_output: print("abs(q1 x q2): %f" % (np.abs(q1 * q2)))
        if self.print_output: print("D x pow(-1.0, FL) x SN: %f" % (self.D * pow(-1.0, FL) * SN))

        return (q1 * q2) + pow(-1.0, FL) * np.abs(q1 * q2) + self.D * pow(-1.0, FL) * SN

    def make_loads(self):
        outfile = open("loads.csv", 'w')
        outfile.write("Hour, Load\n")

        for i in range(8760):
            outfile.write("%d,%0.2f\n" % (i + 1, self.Q(i)))

        outfile.close()


class Asymmetric(Base):
    def __init__(self, amplitude, print_output=False):
        self.A = amplitude
        self.B = 1000
        self.C = 80
        self.D = 0.01
        self.E = 0.95
        self.F = 4.0 / 3.0
        self.G = 2190
        self.print_output = print_output


class Symmetric(Base):
    def __init__(self, amplitude, print_output=False):
        self.A = amplitude
        self.B = 2190
        self.C = 80
        self.D = 0.01
        self.E = 0.95
        self.F = 2.0
        self.G = 0.0
        self.print_output = print_output


Asymmetric(2000).make_loads()
