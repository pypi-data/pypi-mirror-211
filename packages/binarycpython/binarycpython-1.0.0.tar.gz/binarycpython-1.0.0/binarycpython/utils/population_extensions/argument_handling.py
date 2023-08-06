"""
Main script to provide the argument handling class extensions
"""

# pylint: disable=E1101

import logging
import os
import sys
from logging import config

import str2bool

from binarycpython.utils.logging_functions import verbosity_level_dict


class argument_handling:
    """
    Extension for the Population class containing the code for source-file sampling functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def set(self, **kwargs) -> None:
        """
        Function to set the values of the population. This is the preferred method to set values
        of functions, as it provides checks on the input.

        the bse_options will get populated with all the those that have a key that is present
        in the self.defaults

        the population_options will get updated with all the those that have a key that is present
        in the self.population_options

        If neither of above is met; the key and the value get stored in a custom_options dict.

        Args:
            via kwargs all the arguments are either set to binary_c parameters, population_options or custom_options (see above)
        """

        ###############
        # Go over all the input
        for key, value in kwargs.items():
            # match to hostname if appropriate
            value = self._match_arg_to_host(arg={key: value})

            ###############
            # Filter out keys for the population_options
            if key in self.population_options.keys():
                self.vb_warning(
                    "adding: {}={} to population_options".format(key, value),
                )

                # validate values
                self._validate_population_options(key, value)

                # Set values
                self.population_options[key] = value

                ###########
                # Handle some actions for specific key setting

                # Update config for loggers
                if key == "log_config_file":
                    if value is not None:
                        # check if file exists
                        if os.path.isfile(value):
                            config.fileConfig(value)
                            self.logger = logging
                        else:
                            raise ValueError(f"File {value} does not exist.")

                    # Unset the loggers
                    if value is None:
                        self.logger = None

                # Update verbosity
                if key == "verbosity":
                    if self.logger is not None:
                        self.logger.setLevel(verbosity_level_dict[value])
                        for handler in self.logger.handlers:
                            handler.setLevel(verbosity_level_dict[value])

                # Update logfile for logging
                if key == "log_file":
                    if self.logger is not None:
                        for handler in self.logger.handlers:
                            if isinstance(handler, logging.FileHandler):
                                handler.close()
                                handler.baseFilename = os.path.abspath(value)

            ###############
            # Filter out keys for the bse_options
            elif key in self.defaults:
                self.vb_warning(
                    "adding: {}={} to BSE_options".format(key, value),
                )
                self.bse_options[key] = value

            ###############
            # Extra check to check if the key fits one of parameter names that end with %d
            elif self._check_key_is_special_param(key):
                self.vb_warning(
                    "adding: {}={} to BSE_options by catching the %d".format(
                        key, value
                    ),
                )
                self.bse_options[key] = value

            ###############
            # The of the keys go into a custom_options dict
            else:
                self.vb_warning(
                    "<<<< Warning: Key does not match previously known parameter: \
                    adding: {}={} to custom_options >>>>".format(
                        key, value
                    ),
                )
                self.custom_options[key] = value

    def _validate_population_options(self, key, value):
        """
        Function to handle validation of the arguments passed to the population options
        """

        # validate
        self.validation_schema({key: value})

    def parse_cmdline(self) -> None:
        """
        Function to handle settings values via the command line in the form x=y, w=z, etc.

        Best to be called after all the .set(..) lines, and just before the .evolve() is called

        If you input any known parameter (i.e. contained in population_options, defaults/bse_options
        or custom_options), this function will attempt to convert the input from string
        (because everything is string) to the type of the value that option had before.

        The values of the bse_options are initially all strings, but after user input they
        can change to ints.

        The value of any new parameter (which will go to custom_options) will be a string.
        """

        # get the cmd-line args in the form x=y
        cmdline_args = sys.argv[1:]

        if cmdline_args:
            self.vb_info(
                "Found cmdline args. Parsing them now",
            )

            # Grab the input and split them up, while accepting only non-empty entries
            # cmdline_args = args
            self.population_options["_commandline_input"] = cmdline_args

            # expand args by hostname
            cmdline_args = self.expand_args_by_hostname(cmdline_args)

            # Make dict and fill it
            cmdline_dict = {}
            for cmdline_arg in cmdline_args:
                split = cmdline_arg.split("=")

                # Check if its actually a key-value pair separated by "="
                if len(split) == 2:
                    parameter = split[0]
                    value = split[1]

                    old_value_found = False

                    # Find an old value
                    if parameter in self.population_options:
                        old_value = self.population_options[parameter]
                        old_value_found = True

                    elif parameter in self.custom_options:
                        old_value = self.custom_options[parameter]
                        old_value_found = True

                    elif parameter in self.bse_options:
                        old_value = self.bse_options[parameter]
                        old_value_found = True

                    elif parameter in self.defaults:
                        # this will revert to a string type, always
                        old_value = self.defaults[parameter]
                        old_value_found = True

                    # (attempt to) convert type
                    if old_value_found:
                        if old_value is not None:
                            try:
                                self.vb_debug(
                                    "Converting type of {} from {} to {}".format(
                                        parameter, type(value), type(old_value)
                                    ),
                                )
                                try:
                                    if isinstance(old_value, bool):
                                        value = str2bool.str2bool(value)
                                    else:
                                        value = type(old_value)(value)
                                    self.vb_debug(
                                        "Success!",
                                    )
                                except Exception as e:
                                    self.vb_error(
                                        "Failed to convert {param} value with type {type}: old_value is '{old}', new value is '{new}', {e}".format(
                                            param=parameter,
                                            old=old_value,
                                            type=type(old_value),
                                            new=split[1],
                                            e=e,
                                        )
                                    )
                                    self.exit(code=1)

                            except ValueError:

                                # might be able to eval the parameter, e.g.
                                # an expression like "2-1" can eval to "1"
                                # which would be valid
                                try:
                                    evaled = eval(value)
                                    value = type(old_value)(evaled)
                                    self.vb_debug(
                                        "Success! (evaled)",
                                    )

                                except ValueError:
                                    self.vb_warning(
                                        "Tried to convert the given parameter {}/value {} to its correct type {} (from old value {}). But that wasn't possible.".format(
                                            parameter, value, type(old_value), old_value
                                        ),
                                    )

                    # Add to dict
                    self.vb_info(
                        "setting {} = {} ".format(parameter, value),
                    )
                    cmdline_dict[parameter] = value

                else:
                    self.vb_error(
                        "Error: I do not know how to process {}: cmdline args should be in the format x=y, yours appears not to be.".format(
                            cmdline_arg
                        ),
                    )
                    self.exit(1)

            # unpack the dictionary into the setting function that handles where the values are set
            self.set(**cmdline_dict)

    def _return_argline(self, parameter_dict=None):
        """
        Function to create the string for the arg line from a parameter dict
        """

        #
        if not parameter_dict:
            parameter_dict = self.bse_options

        argline = "binary_c "

        # Combine all the key value pairs into string
        for param_name in sorted(parameter_dict):
            argline += "{} {} ".format(param_name, parameter_dict[param_name])
        argline = argline.strip()

        return argline

    def _check_key_is_special_param(self, param_key):
        """
        Function to check if the given key is part of the special parameter list
        """

        is_special_key = any(
            [
                True
                if (
                    param_key.startswith(param[:-2])
                    and len(param[:-2]) < len(param_key)
                )
                else False
                for param in self.special_params
            ]
        )

        return is_special_key

    def _check_full_system_dict_keys(self, full_system_dict):
        """
        Function to check the full system dict that will be turned in to a binary_c call
        """

        for key in full_system_dict.keys():
            if key not in self.available_keys:
                # Deal with special keys
                if not self._check_key_is_special_param(key):
                    msg = "Error: Found a parameter unknown to binary_c: {}. Abort".format(
                        key
                    )
                    raise ValueError(msg)
