from __future__ import division
import sys

from ghx_print import PrintClass


class BasePropertiesClass:

    def __init__(self, json_data, print_output):

        try:
            self.conductivity = json_data['Conductivity']
        except:  # pragma: no cover
            PrintClass.my_print("....'Conductivity' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BasePropertiesClass")

        try:
            self.specific_heat = json_data['Specific Heat']
        except:  # pragma: no cover
            PrintClass.my_print("....'Specific Heat' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BasePropertiesClass")

        try:
            self.density = json_data['Density']
        except:  # pragma: no cover
            PrintClass.my_print("....'Density' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing BasePropertiesClass")
