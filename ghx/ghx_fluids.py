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
            self.flow_rate_prev = 0.0
        except:  # pragma: no cover
            self.my_print("....'Flow Rate' key not found", self._color_warn)
            self.fatal_error(message="Error initializing FluidsClass")

        self.temperature = initial_temp
        self.temperature_prev = None
        self.pressure = 101325
        self.mass_flow_rate = self.calc_mass_flow_rate()
        self.dens_val = self.dens()
        self.cp_val = self.cp()
        self.visc_val = self.visc()
        self.cond_val = self.cond()
        self.pr_val = self.pr()
        self.heat_capacity_val = self.heat_capacity()

    def dens(self):

        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid density in [kg/m3]
        """
        if self.temperature != self.temperature_prev:
            self.dens_val = cp.PropsSI('D', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

        return self.dens_val

    def cp(self):

        """
        Determines the fluid specific heat as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid specific heat.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid specific heat in [J/kg-K]
        """

        if self.temperature != self.temperature_prev:
            self.cp_val = cp.PropsSI('C', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

        return self.cp_val

    def visc(self):

        """
        Determines the fluid viscosity as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid viscosity in [Pa-s]
        """

        if self.temperature != self.temperature_prev:
            self.visc_val = cp.PropsSI('V', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

        return self.visc_val

    def cond(self):

        """
        Determines the fluid conductivity as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid conductivity in [W/m-K]
        """

        if self.temperature != self.temperature_prev:
            self.cond_val = cp.PropsSI('L', 'T', self.temperature + self.celsius_to_kelvin, 'P', self.pressure, self.fluid_type)

        return self.cond_val

    def pr(self):

        """
        Determines the fluid Prandtl as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :returns fluid Prandtl number
        """

        return self.cp() * self.visc() / self.cond()

    def heat_capacity(self):

        """
        Calculates fluid thermal capacitance
        """

        return self.mass_flow_rate * self.cp()

    def calc_mass_flow_rate(self):

        """
        Calculates the fluid mass flow rate
        """

        self.mass_flow_rate = self.flow_rate * self.dens()

        return self.mass_flow_rate

    def update_fluid_state(self, new_temp=None, new_flow_rate = None):

        """
        Updates fluid state as necessary
        """

        if new_temp is not None:
            self.temperature_prev = self.temperature
            self.temperature = new_temp

        if new_flow_rate is not None:
            self.flow_rate_prev = self.flow_rate
            self.flow_rate = new_flow_rate
            self.calc_mass_flow_rate()
