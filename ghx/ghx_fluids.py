import CoolProp.CoolProp as cp
import numpy as np


class FluidsClass:

    def __init__(self):
        pass

    """
    Contains all fluid properties, correlations, etc.
    """

    def dens(self, temp_in_c):

        """
        Determines the fluid density as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns fluid density in [kg/m3]
        """

        return cp.PropsSI('D', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    def cp(self, temp_in_c):

        """
        Determines the fluid specific heat as a function of temperature, in Celsius.
        Uses the CoolProp python library to find the fluid specific heat.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns fluid specific heat in [J/kg-K]
        """

        return cp.PropsSI('C', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    def visc(self, temp_in_c):

        """
        Determines the fluid viscosity as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns fluid viscosity in [Pa-s]
        """

        return cp.PropsSI('V', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    def cond(self, temp_in_c):

        """
        Determines the fluid conductivity as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns fluid conductivity in [W/m-K]
        """

        return cp.PropsSI('L', 'T', temp_in_c + 273.15, 'P', 101325, self.fluid)

    def pr(self, temp_in_c):

        """
        Determines the fluid Prandtl as a function of temperature, in Celsius.
        Uses the CoolProp python library.
        Fluid type is determined from the type of fluid specified for the GHX array object.

        :param temp_in_c: temperature in Celsius
        :returns fluid Prandtl number
        """

        return self.cp(temp_in_c) * self.visc(temp_in_c) / self.cond(temp_in_c)

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
            f_high = (0.79 * np.log(re) - 1.64)**(-2.0)  # pure turbulent flow
            sf = 1 / (1 + np.exp(-(re - 3000.0) / 450.0))  # smoothing function
            return (1 - sf) * f_low + sf * f_high
        else:
            return (0.79 * np.log(re) - 1.64)**(-2.0)  # pure turbulent flow
