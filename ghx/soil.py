from ghx.base_properties import BasePropertiesClass
from ghx.my_print import PrintClass


class SoilClass(BasePropertiesClass):
    def __init__(self, json_data, print_output):

        BasePropertiesClass.__init__(self, json_data, print_output)

        try:
            self.undisturbed_temp = json_data['Temperature']
        except:  # pragma: no cover
            PrintClass.my_print("....'Temperature' key not found", 'warn')
            PrintClass.fatal_error(message="Error initializing SoilClass")

        self.heat_capacity = self.specific_heat * self.density
        self.thermal_diffusivity = self.conductivity / (self.density * self.specific_heat)
