"""
The class extension for the population object that contains the custom_binary_c_logging functionality
"""

# pylint: disable=E1101


from binarycpython.utils.custom_logging_functions import (
    autogen_C_logging_code,
    binary_c_log_code,
    create_and_load_logging_function,
)
from binarycpython.utils.functions import remove_file


class custom_binary_c_logging:
    """
    Extension for the Population class containing the code for custom_binary_c_logging class methods
    """

    def __init__(self, **kwargs):
        """
        Init function for the custom_binary_c_logging class extension
        """

        return

    def _set_custom_logging(self):
        """
        Function/routine to set all the custom logging so that the function memory pointer
        is known to the grid.

        When the memory adress is loaded and the library file is set we'll skip rebuilding the library
        """

        # Only if the values are the 'default' unset values
        if (
            self.population_options["custom_logging_func_memaddr"] == -1
            and self.population_options["_custom_logging_shared_library_file"] is None
        ):
            self.vb_info(
                "Creating and loading custom logging functionality",
            )
            # C_logging_code gets priority of C_autogen_code
            if self.population_options["C_logging_code"]:
                # Generate entire shared lib code around logging lines
                custom_logging_code = binary_c_log_code(
                    self.population_options["C_logging_code"],
                    verbosity=self.population_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                )

                # Load memory address
                (
                    self.population_options["custom_logging_func_memaddr"],
                    self.population_options["_custom_logging_shared_library_file"],
                ) = create_and_load_logging_function(
                    custom_logging_code,
                    verbosity=self.population_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                    custom_tmp_dir=self.population_options["tmp_dir"],
                )

            elif self.population_options["C_auto_logging"]:
                # Generate real logging code
                logging_line = autogen_C_logging_code(
                    self.population_options["C_auto_logging"],
                    verbosity=self.population_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                )

                # Generate entire shared lib code around logging lines
                custom_logging_code = binary_c_log_code(
                    logging_line,
                    verbosity=self.population_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                )

                # Load memory address
                (
                    self.population_options["custom_logging_func_memaddr"],
                    self.population_options["_custom_logging_shared_library_file"],
                ) = create_and_load_logging_function(
                    custom_logging_code,
                    verbosity=self.population_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                    custom_tmp_dir=self.population_options["tmp_dir"],
                )
        else:
            self.vb_info(
                "Custom logging library already loaded. Not setting them again.",
            )

    def _clean_up_custom_logging(self, evol_type):
        """
        Function to clean up the custom logging.
        Has two types:
            'single':
                - removes the compiled shared library
                    (which name is stored in population_options['_custom_logging_shared_library_file'])
                - TODO: unloads/frees the memory allocated to that shared library
                    (which is stored in population_options['custom_logging_func_memaddr'])
                - sets both to None
            'multiple':
                - TODO: make this and design this
        """

        if evol_type == "single":
            self.vb_info(
                "Cleaning up the custom logging stuff. type: single",
            )

            # TODO: Explicitly unload the library

            # Reset the memory adress location
            self.population_options["custom_logging_func_memaddr"] = -1

            # remove shared library files
            if self.population_options["_custom_logging_shared_library_file"]:
                remove_file(
                    self.population_options["_custom_logging_shared_library_file"],
                    self.population_options["verbosity"],
                )
                self.population_options["_custom_logging_shared_library_file"] = None

        if evol_type == "population":
            self.vb_info(
                "Cleaning up the custom logging stuffs. type: population",
            )

            # TODO: make sure that these also work. not fully sure if necessary tho.
            #   whether its a single file, or a dict of files/mem addresses

        if evol_type == "MC":
            pass
