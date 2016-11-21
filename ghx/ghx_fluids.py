from __future__ import division

import CoolProp.CoolProp as cp
import numpy as np

from ghx_print import *
from ghx_constants import *


class FluidsClass(ConstantClass, PrintClass):

    """
    Contains all fluid properties, correlations, etc.
    """

    def __init__(self, json_data, initial_temp, print_output):

        ConstantClass.__init__(self)
        PrintClass.__init__(self, print_output)

        try:
            self.fluid_type = json_data['Type']
        except:  # pragma: no cover
            self.my_print("....'Name' key not found", self._color_warn)
            self.fatal_error(message="Error initializing FluidsClass")

        try:
            self.concentration = json_data['Concentration']
        except:  # pragma: no cover
            self.my_print("....'Concentration' key not found", self._color_warn)
            self.fatal_error(message="Error initializing FluidsClass")

        try:
            self.flow_rate = json_data['Flow Rate']
        except:  # pragma: no cover
            self.my_print("....'Flow Rate' key not found", self._color_warn)
            self.fatal_error(message="Error initializing FluidsClass")

        self.mass_flow_rate = None
        self.temperature = initial_temp
        self.pressure = 101325

    def dens(self):

        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid density in [kg/m3]
        """

        return cp.PropsSI('D', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

    def cp(self):

        """
        Determines the fluid specific heat as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid specific heat.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid specific heat in [J/kg-K]
        """

        return cp.PropsSI('C', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

    def visc(self):

        """
        Determines the fluid viscosity as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid viscosity in [Pa-s]
        """

        return cp.PropsSI('V', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

    def cond(self):

        """
        Determines the fluid conductivity as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid conductivity in [W/m-K]
        """

        return cp.PropsSI('L', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

    def pr(self):

        """
        Determines the fluid Prandtl as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid Prandtl number
        """

        return self.cp() * self.visc() / self.cond()

