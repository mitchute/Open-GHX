
from termcolor import cprint


class PrintClass:

    def __init__(self, print_output):

        """
        class constructor
        """

        self.print_output = print_output
        self.color_fail = 'red'
        self.color_warn = 'yellow'
        self.color_success = 'green'

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
