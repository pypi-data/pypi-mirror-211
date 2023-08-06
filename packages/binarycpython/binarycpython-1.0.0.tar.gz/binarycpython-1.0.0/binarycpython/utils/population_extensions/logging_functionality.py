"""
The class extension for the population object that contains general logging functionality

TODO: https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
"""

import functools

from binarycpython.utils.logging_functions import verbose_print

# pylint: disable=E1101


class logging_functionality:
    """
    Extension for the Population class containing the general logging class methods
    """

    def __init__(self, **kwargs):
        """
        Init function for the custom_binary_c_logging class extension
        """

    # def _set_loggers(self):
    #     """
    #     Function to set the loggers for the execution of the grid
    #     """

    #     # Set up logger
    #     self.logger = logging.getLogger("population_logger")
    #     self.logger.setLevel(verbosity_level_dict[self.population_options["verbosity"]])

    #     # Reset handlers
    #     for handler in self.logger.handlers:
    #         if isinstance(handler, logging.FileHandler):
    #             handler.close()
    #     self.logger.handlers = []

    #     Set formatting of output
    #     log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")

    #     # Make handler for output to stdout
    #     handler_stdout = logging.StreamHandler(sys.stdout)
    #     handler_stdout.setFormatter(log_formatter)
    #     handler_stdout.setLevel(verbosity_level_dict[self.population_options["verbosity"]])
    #     self.logger.addHandler(handler_stdout)

    #     # make handler for output to file
    #     if self.population_options.get("log_file", ""):
    #         population_logfile = self.population_options["log_file"]

    #         # Create directory
    #         os.makedirs(os.path.dirname(population_logfile), exist_ok=True)

    #         handler_file = logging.FileHandler(
    #             filename=os.path.join(population_logfile)
    #         )
    #         handler_file.setFormatter(log_formatter)
    #         handler_file.setLevel(verbosity_level_dict[self.population_options["verbosity"]])
    #         self.logger.addHandler(handler_file)

    ############
    # verbose functions
    def verbose_print(self, message, minimal_verbosity):
        """
        Wrapper method for the verbose print that calls the verbose print with the correct newline
        """

        # Pass the rest to the original verbose print
        verbose_print(
            message=message,
            verbosity=self.population_options["verbosity"],
            minimal_verbosity=minimal_verbosity,
            logger=self.logger,
            newline=self.population_options["log_newline"],
        )

    # Partial binds
    vb_critical = functools.partialmethod(verbose_print, minimal_verbosity=0)
    vb_error = functools.partialmethod(verbose_print, minimal_verbosity=1)
    vb_warning = functools.partialmethod(verbose_print, minimal_verbosity=2)
    vb_info = functools.partialmethod(verbose_print, minimal_verbosity=3)
    vb_debug = functools.partialmethod(verbose_print, minimal_verbosity=4)
