from __future__ import division

import sys
from termcolor import cprint


class PrintClass:

    def __init__(self, print_output):

        """
        class constructor
        """

        self.print_output = print_output
        self._color_fail = 'red'
        self._color_warn = 'yellow'
        self._color_success = 'green'

    def my_print(self, message, color=''):

        """
        prints the message if self.print_output
        default color is black, unless overridden
        """

        if self.print_output:  # pragma: no cover
            if color != '':
                cprint(message, color)
            else:
                print(message)

    def fatal_error(self, message=None):  # pragma: no cover

        """
        Fatal error. Terminate program
        """

        if message is not None:
            self.my_print("%s" % (message), self._color_fail)
        else:
            self.my_print("Fatal error encountered", self._color_fail)

        self.my_print("Program exiting", self._color_fail)
        sys.exit(1)
