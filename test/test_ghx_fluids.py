import os
import sys

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ghx'))

import unittest
from ghx.ghx_fluids import *


class TestFluidsClass(unittest.TestCase):

    def test_dens(self):

        """
        Tests fluid density calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        dict_fluid = {'Type': 'Water',
                'Concentration': 100,
                'Flow Rate': 0.000303}

        tolerance = 1.0

        curr_tst = FluidsClass(dict_fluid, 20, False)
        self.assertAlmostEqual(curr_tst.dens(), 998.0, delta=tolerance)

        curr_tst.temperature = 40
        self.assertAlmostEqual(curr_tst.dens(), 992.1, delta=tolerance)

        curr_tst.temperature = 60
        self.assertAlmostEqual(curr_tst.dens(), 983.3, delta=tolerance)

        curr_tst.temperature = 80
        self.assertAlmostEqual(curr_tst.dens(), 971.8, delta=tolerance)

    def test_cp(self):

        """
        Tests fluid specific heat calculation routine

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        dict_fluid = {'Type': 'Water',
                'Concentration': 100,
                'Flow Rate': 0.000303}

        tolerance = 4.0

        curr_tst = FluidsClass(dict_fluid, 20, False)
        self.assertAlmostEqual(curr_tst.cp(), 4182, delta=tolerance)

        curr_tst.temperature = 40
        self.assertAlmostEqual(curr_tst.cp(), 4179, delta=tolerance)

        curr_tst.temperature = 60
        self.assertAlmostEqual(curr_tst.cp(), 4185, delta=tolerance)

        curr_tst.temperature = 80
        self.assertAlmostEqual(curr_tst.cp(), 4197, delta=tolerance)

    def test_visc(self):

        """
        Tests fluid viscosity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        dict_fluid = {'Type': 'Water',
                'Concentration': 100,
                'Flow Rate': 0.000303}

        tolerance = 1E-4

        curr_tst = FluidsClass(dict_fluid, 20, False)
        self.assertAlmostEqual(curr_tst.visc(), 1.002E-3, delta=tolerance)

        curr_tst.temperature = 40
        self.assertAlmostEqual(curr_tst.visc(), 0.653E-3, delta=tolerance)

        curr_tst.temperature = 60
        self.assertAlmostEqual(curr_tst.visc(), 0.467E-3, delta=tolerance)

        curr_tst.temperature = 80
        self.assertAlmostEqual(curr_tst.visc(), 0.355E-3, delta=tolerance)

    def test_cond(self):

        """
        Tests fluid conductivity calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        dict_fluid = {'Type': 'Water',
                'Concentration': 100,
                'Flow Rate': 0.000303}

        tolerance = 1E-2

        curr_tst = FluidsClass(dict_fluid, 20, False)
        self.assertAlmostEqual(curr_tst.cond(), 0.598, delta=tolerance)

        curr_tst.temperature = 40
        self.assertAlmostEqual(curr_tst.cond(), 0.631, delta=tolerance)

        curr_tst.temperature = 60
        self.assertAlmostEqual(curr_tst.cond(), 0.654, delta=tolerance)

        curr_tst.temperature = 80
        self.assertAlmostEqual(curr_tst.cond(), 0.670, delta=tolerance)

    def test_pr(self):

        """
        Tests fluid Prandtl number calculations

        Reference values come from Cengel & Ghajar 2015

        Cengel, Y.A., & Ghajar, A.J. 2015. Heat and Mass Transfer, Fundamentals and Applications.
        McGraw-Hill. New York, New York.
        """

        dict_fluid = {'Type': 'Water',
                'Concentration': 100,
                'Flow Rate': 0.000303}

        tolerance = 1E-1

        curr_tst = FluidsClass(dict_fluid, 20, False)
        self.assertAlmostEqual(curr_tst.pr(), 7.01, delta=tolerance)

        curr_tst.temperature = 40
        self.assertAlmostEqual(curr_tst.pr(), 4.32, delta=tolerance)

        curr_tst.temperature = 60
        self.assertAlmostEqual(curr_tst.pr(), 2.99, delta=tolerance)

        curr_tst.temperature = 80
        self.assertAlmostEqual(curr_tst.pr(), 2.22, delta=tolerance)
