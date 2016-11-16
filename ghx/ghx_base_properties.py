from __future__ import division
import sys

from ghx_print import *


class BasePropertiesClass(PrintClass):

    def __init__(self, json_data, print_output):

        PrintClass.__init__(self, print_output)

        try:
            self.conductivity = json_data['Conductivity']
        except:  # pragma: no cover
            self.my_print("....'Conductivity' key not found", self._color_warn)
            self.fatal_error(message="Error initializing BasePropertiesClass")

        try:
            self.specific_heat = json_data['Specific Heat']
        except:  # pragma: no cover
            self.my_print("....'Specific Heat' key not found", self._color_warn)
            self.fatal_error(message="Error initializing BasePropertiesClass")

        try:
            self.density = json_data['Density']
        except:  # pragma: no cover
            self.my_print("....'Density' key not found", self._color_warn)
            self.fatal_error(message="Error initializing BasePropertiesClass")
