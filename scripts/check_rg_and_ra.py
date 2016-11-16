from __future__ import division
import numpy as np
import sys


class BasePropertiesClass:

    def __init__(self, cond=None, cp=None, dens=None):

        self.conductivity = cond
        self.specific_heat = cp
        self.density = dens


class PipeClass:

    def __init__(self, d_o=None):
        self.outer_diameter = d_o
        self.outer_radius = self.outer_diameter / 2


class BHResistanceClass:

    def __init__(self, d_po, d_bh, s, soil_cond, grout_cond, resist_pipe):

        self.bh_diameter = d_bh
        self.bh_radius = self.bh_diameter / 2
        self.shank_space = s

        self.soil = BasePropertiesClass(cond=soil_cond, cp=0, dens=0)
        self.grout = BasePropertiesClass(cond=grout_cond, cp=0, dens=0)
        self.pipe = PipeClass(d_po)

        self.resist_pipe = resist_pipe

        self.theta_1 = self.shank_space / (2 * self.bh_radius)
        self.theta_2 = self.bh_radius / self.pipe.outer_radius
        self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
        self.sigma = (self.grout.conductivity - self.soil.conductivity) / \
                     (self.grout.conductivity + self.soil.conductivity)
        self.beta = 2 * np.pi * self.grout.conductivity * self.resist_pipe

        self.resist_bh_total_internal = None
        self.resist_bh_ave = None
        self.resist_grout = None

        self.calc_bh_average_thermal_resistance()
        self.calc_bh_total_internal_thermal_resistance()
        self.calc_bh_grout_thermal_resistance()

    def calc_bh_average_thermal_resistance(self):

        """
        Calculates the average thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 13
        """

        final_term_1 = np.log(self.theta_2 / (2 * self.theta_1 * (1 - self.theta_1 ** 4) ** self.sigma))
        num_final_term_2 = self.theta_3 ** 2 * (1 - (4 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4)) ** 2
        den_final_term_2_pt_1 = (1 + self.beta) / (1 - self.beta)
        den_final_term_2_pt_2 = self.theta_3 ** 2 * \
            (1 + (16 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4) ** 2)
        den_final_term_2 = den_final_term_2_pt_1 + den_final_term_2_pt_2
        final_term_2 = num_final_term_2 / den_final_term_2

        self.resist_bh_ave = (1 / (4 * np.pi * self.grout.conductivity)) * (self.beta + final_term_1 - final_term_2)

    def calc_bh_total_internal_thermal_resistance(self):

        """
        Calculates the total internal thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 26
        """

        final_term_1 = np.log(
            ((1 + self.theta_1 ** 2) ** self.sigma) / (self.theta_3 * (1 - self.theta_1 ** 2) ** self.sigma))
        num_term_2 = self.theta_3 ** 2 * (1 - self.theta_1 ** 4 + 4 * self.sigma * self.theta_1 ** 2) ** 2
        den_term_2_pt_1 = (1 + self.beta) / (1 - self.beta) * (1 - self.theta_1 ** 4) ** 2
        den_term_2_pt_2 = self.theta_3 ** 2 * (1 - self.theta_1 ** 4) ** 2
        den_term_2_pt_3 = 8 * self.sigma * self.theta_1 ** 2 * self.theta_3 ** 2 * (1 + self.theta_1 ** 4)
        den_term_2 = den_term_2_pt_1 - den_term_2_pt_2 + den_term_2_pt_3
        final_term_2 = num_term_2 / den_term_2

        self.resist_bh_total_internal = (1 / (np.pi * self.grout.conductivity)) * \
                                        (self.beta + final_term_1 - final_term_2)

    def calc_bh_grout_thermal_resistance(self):

        self.resist_grout = self.resist_bh_ave - self.resist_pipe / 2

out_file = open("my_data.csv", 'w')

d_po = 0.032
borehole_diameters = [0.096, 0.192, 0.288]
configurations = ['A', 'B', 'C']
soil_conductivity = [4, 3, 2, 1]
grout_conductivity = [0.6, 1.2, 1.8, 2.4, 3.0, 3.6]

out_file.write("Theta 1, Theta 2, Ground Conductivity, Grout Conductivity, Rg, Ra\n")

for d_bh in borehole_diameters:
    for config in configurations:
        for s_k in soil_conductivity:
            for g_k in grout_conductivity:
                if config == 'A':
                    s = d_po
                elif config == 'B':
                    s = d_po + (d_bh - 2 * d_po) / 3
                elif config == 'C':
                    s = d_bh - d_po

                cls = BHResistanceClass(d_po=d_po, d_bh=d_bh, s=s, soil_cond=s_k, grout_cond=g_k, resist_pipe=0.05)

                out_file.write("%f,%f,%f,%f,%f,%f\n" %
                               (cls.theta_1,
                                cls.theta_2,
                                cls.soil.conductivity,
                                cls.grout.conductivity,
                                cls.resist_grout,
                                cls.resist_bh_total_internal))
            out_file.write("\n\n\n")
out_file.close()
