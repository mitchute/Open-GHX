from __future__ import division

class ConstantClass:

    """
    All constants
    """

    def __init__(self):
        self.months_in_year = 12
        self.hours_in_month = 730
        self.hours_in_year = self.months_in_year * self.hours_in_month
        self.celsius_to_kelvin = 273.15
