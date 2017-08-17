import numpy as np

from ghx.base_properties import BasePropertiesClass
from ghx.my_print import PrintClass
from ghx.pipe import PipeClass
from ghx.soil import SoilClass


class BoreholeClass:
    def __init__(self, json_data, print_output):

        try:
            self.name = json_data['Name']
        except:  # pragma: no cover
            PrintClass.my_print("....'Name' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BoreholeClass")

        try:
            self.location = json_data['Location']
        except:  # pragma: no cover
            PrintClass.my_print("....'Location' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BoreholeClass")

        try:
            self.depth = json_data['Depth']
        except:  # pragma: no cover
            PrintClass.my_print("....'Depth' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BoreholeClass")

        try:
            self.radius = json_data['Radius']
            self.diameter = self.radius * 2
        except:  # pragma: no cover
            PrintClass.my_print("....'Radius' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BoreholeClass")

        try:
            self.shank_space = json_data['Shank Spacing']
        except:  # pragma: no cover
            PrintClass.my_print("....'Shank Spacing' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BoreholeClass")

        self.soil = SoilClass(json_data['Soil'], print_output)
        self.grout = BasePropertiesClass(json_data['Grout'], print_output)
        self.pipe = PipeClass(json_data['Pipe'], json_data['Fluid'], json_data['Soil']['Temperature'], print_output)

        # validate shank spacing
        if self.shank_space > (2 * self.radius - self.pipe.outer_diameter) \
                or self.shank_space < self.pipe.outer_diameter:  # pragma: no cover
            PrintClass.my_print("Invalid shank spacing", 'warn')
            PrintClass.my_print("Check shank spacing, pipe diameter, and borehole radius", 'warn')
            PrintClass.fatal_error(message="Error initializing BoreholeClass")

        self.resist_bh_ave = None
        self.resist_bh_total_internal = None
        self.resist_bh_grout = None
        self.resist_bh = None

        self.theta_1 = self.shank_space / (2 * self.radius)
        self.theta_2 = self.radius / self.pipe.outer_radius
        self.theta_3 = 1 / (2 * self.theta_1 * self.theta_2)
        self.sigma = (self.grout.conductivity - self.soil.conductivity) / \
                     (self.grout.conductivity + self.soil.conductivity)
        self.beta = None

        self.calc_bh_resistance()

    def calc_bh_average_resistance(self):

        """
        Calculates the average thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 13
        """

        self.beta = 2 * np.pi * self.grout.conductivity * self.pipe.resist_pipe

        final_term_1 = np.log(self.theta_2 / (2 * self.theta_1 * (1 - self.theta_1 ** 4) ** self.sigma))
        num_final_term_2 = self.theta_3 ** 2 * (1 - (4 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4)) ** 2
        den_final_term_2_pt_1 = (1 + self.beta) / (1 - self.beta)
        den_final_term_2_pt_2 = self.theta_3 ** 2 * \
                                (1 + (16 * self.sigma * self.theta_1 ** 4) / (1 - self.theta_1 ** 4) ** 2)
        den_final_term_2 = den_final_term_2_pt_1 + den_final_term_2_pt_2
        final_term_2 = num_final_term_2 / den_final_term_2

        self.resist_bh_ave = (1 / (4 * np.pi * self.grout.conductivity)) * (self.beta + final_term_1 - final_term_2)

        return self.resist_bh_ave

    def calc_bh_total_internal_resistance(self):

        """
        Calculates the total internal thermal resistance of the borehole using the first-order multipole method.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 26
        """

        self.beta = 2 * np.pi * self.grout.conductivity * self.pipe.resist_pipe

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

        return self.resist_bh_total_internal

    def calc_bh_grout_resistance(self):

        """
        Calculates borehole resistance. Use for validation.
        """

        self.resist_bh_grout = self.calc_bh_average_resistance() - self.pipe.resist_pipe / 2.0

        return self.resist_bh_grout

    def calc_bh_resistance(self):

        """
        Calculates the effective thermal resistance of the borehole assuming a uniform heat flux.

        Javed, S. & Spitler, J.D. Calculation of Borehole Thermal Resistance. In 'Advances in
        Ground-Source Heat Pump Systems,' pp. 84. Rees, S.J. ed. Cambridge, MA. Elsevier Ltd. 2016.

        Eq: 3-67

        Coefficients for equations 13 and 26 from Javed & Spitler 2016 calculated here.

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 14
        """

        # only update if flow rate has changed
        if self.pipe.fluid.flow_rate != self.pipe.fluid.flow_rate_prev:
            self.beta = 2 * np.pi * self.grout.conductivity * self.pipe.calc_pipe_resistance()
            self.calc_bh_average_resistance()
            self.calc_bh_total_internal_resistance()

        resist_short_circuiting = (1 / (3 * self.resist_bh_total_internal)) \
                                  * (self.depth / self.pipe.fluid.heat_capacity()) ** 2

        self.resist_bh = self.resist_bh_ave + resist_short_circuiting

        return self.resist_bh
