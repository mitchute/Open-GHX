from __future__ import division
import numpy as np

from ghx.ghx_print import PrintClass
from ghx.ghx_base_properties import *
from ghx.ghx_fluids import *


class PipeClass(BasePropertiesClass):

    def __init__(self, json_data_pipe, json_data_fluid, initial_temp, print_output):

        BasePropertiesClass.__init__(self, json_data_pipe, print_output)

        self.fluid = FluidsClass(json_data_fluid, initial_temp, print_output)

        try:
            self.outer_diameter = json_data_pipe['Outside Diameter']
        except:  # pragma: no cover
            PrintClass.my_print("....'Outside Diameter' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing PipeClass")

        try:
            self.thickness = json_data_pipe['Wall Thickness']
        except:  # pragma: no cover
            PrintClass.my_print("....'Wall Thickness' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing PipeClass")

        self.outer_radius = self.outer_diameter / 2
        self.inner_radius = self.outer_radius - self.thickness
        self.inner_diameter = self.outer_diameter - 2 * self.thickness

        self.resist_pipe_convection = None
        self.resist_pipe_conduction = None
        self.resist_pipe = None

        self.calc_pipe_resistance()

    def calc_pipe_conduction_resistance(self):

        """
        Calculates the thermal resistance of a pipe, in [K/(W/m)].

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.
        """

        self.resist_pipe_conduction = np.log(self.outer_diameter / self.inner_diameter) / \
                                            (2 * np.pi * self.conductivity)

        return self.resist_pipe_conduction

    def calc_pipe_convection_resistance(self):

        """
        Calculates the convection resistance using Gnielinski and Petukov, in [k/(W/m)]

        Gneilinski, V. 1976. 'New equations for heat and mass transfer in turbulent pipe and channel flow.'
        International Chemical Engineering 16(1976), pp. 359-368.
        """

        lower_limit = 2000
        upper_limit = 4000

        re = 4 * self.fluid.mass_flow_rate / (self.fluid.visc() * np.pi * self.inner_diameter)

        if re < lower_limit:
            nu = 4.01  # laminar mean(4.36, 3.66)
        elif lower_limit <= re < upper_limit:
            nu_low = 4.01  # laminar
            f = self.friction_factor(re)  # turbulent
            pr = self.fluid.pr()
            nu_high = (f / 8) * (re - 1000) * pr / (1 + 12.7 * (f / 8) ** 0.5 * (pr ** (2 / 3) - 1))
            sigma = 1 / (1 + np.exp(-(re - 3000) / 150))  # smoothing function

            nu = (1 - sigma) * nu_low + sigma * nu_high
        else:
            f = self.friction_factor(re)
            pr = self.fluid.pr()
            nu = (f / 8) * (re - 1000) * pr / (1 + 12.7 * (f / 8) ** 0.5 * (pr ** (2 / 3) - 1))

        h = nu * self.fluid.cond() / self.inner_diameter

        self.resist_pipe_convection = 1 / (h * np.pi * self.inner_diameter)

        return self.resist_pipe_convection

    def friction_factor(self, re):

        """
        Calculates the friction factor in smooth tubes

        Petukov, B.S. 1970. 'Heat transfer and friction in turbulent pipe flow with variable physical properties.'
        In Advances in Heat Transfer, ed. T.F. Irvine and J.P. Hartnett, Vol. 6. New York Academic Press.
        """

        # limits picked be within about 1% of actual values
        lower_limit = 1500
        upper_limit = 5000

        if re < lower_limit:
            return 64.0 / re  # pure laminar flow
        elif lower_limit <= re < upper_limit:
            f_low = 64.0 / re  # pure laminar flow
            f_high = (0.79 * np.log(re) - 1.64) ** (-2.0)  # pure turbulent flow
            sf = 1 / (1 + np.exp(-(re - 3000.0) / 450.0))  # smoothing function
            return (1 - sf) * f_low + sf * f_high
        else:
            return (0.79 * np.log(re) - 1.64) ** (-2.0)  # pure turbulent flow

    def calc_pipe_resistance(self):

        """
        Calculates the combined conduction and convection pipe resistance

        Javed, S. & Spitler, J.D. 2016. 'Accuracy of Borehole Thermal Resistance Calculation Methods
        for Grouted Single U-tube Ground Heat Exchangers.' J. Energy Engineering. Draft in progress.

        Equation 3
        """

        self.resist_pipe = self.calc_pipe_convection_resistance() + self.calc_pipe_conduction_resistance()

        return self.resist_pipe

