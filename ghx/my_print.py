import os
import sys

from termcolor import cprint


class PrintClass:
    print_output = None
    output_path = None
    color_fail = 'red'
    color_warn = 'yellow'
    color_success = 'green'
    log_messages = ""

    def __init__(self, print_output, output_path):

        """
        class constructor
        """
        PrintClass.print_output = print_output
        PrintClass.output_path = output_path

    @staticmethod
    def my_print(message, color=''):

        """
        prints the message if self.print_output
        default color is black, unless overridden
        """

        if PrintClass.print_output:  # pragma: no cover
            if color == '':
                print(message)
            elif color == 'success':
                cprint(message, PrintClass.color_success)
            elif color == 'warn':
                cprint(message, PrintClass.color_warn)
            elif color == 'fail':
                cprint(message, PrintClass.color_fail)
            else:
                print(message)

        PrintClass.log_messages += ('%s\n' % message)

    @staticmethod
    def write_log_file():

        """
        Write log file
        """

        cwd = os.getcwd()

        path_to_output_dir = os.path.join(cwd, PrintClass.output_path)

        if not os.path.exists(path_to_output_dir):
            os.makedirs(path_to_output_dir)

        # open file
        out_file = open(os.path.join(path_to_output_dir, 'ghx.log'), 'w')

        # write log
        out_file.write(PrintClass.log_messages)

        # close it
        out_file.close()

    @staticmethod
    def fatal_error(message=None):  # pragma: no cover

        """
        Fatal error. Terminate program
        """

        if message is not None:
            PrintClass.my_print('%s' % message, PrintClass.color_fail)
        else:
            PrintClass.my_print('Fatal error encountered', PrintClass.color_fail)

        PrintClass.my_print('Program exiting', PrintClass.color_fail)

        PrintClass.write_log_file()
        sys.exit(1)
