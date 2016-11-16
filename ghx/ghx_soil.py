from __future__ import division

from ghx_print import *
from ghx_base_properties import *


class SoilClass(PrintClass, BasePropertiesClass):

    def __init__(self, json_data, print_output):

        PrintClass.__init__(self, print_output)
        BasePropertiesClass.__init__(self, json_data, print_output)

        try:
            self.undisturbed_temp = json_data['Temperature']
        except:  # pragma: no cover
            self.my_print("....'Temperature' key not found", self._color_warn)
            self.fatal_error(message="Error initializing SoilClass")

        self.heat_capacity = self.specific_heat * self.density
        self.thermal_diffusivity = self.conductivity / (self.density * self.specific_heat)
