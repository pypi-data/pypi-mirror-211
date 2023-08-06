"""
Main script to provide the source-file sampling class extensions. Source-file sampling is an evolution type to
"""

# pylint: disable=E1101

import os

from binarycpython.utils.functions import get_numerical_value


def _source_file_sampling_parse_values(string_value):
    """
    Function to parse values for the source file sampling
    """

    try:
        value = get_numerical_value(string_value)
    except ValueError:
        value = str(string_value)

    return value


class source_file_sampling:
    """
    Extension for the Population class containing the code for source-file sampling functions
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    ###################################################
    # Population from file functions
    #
    # Functions below are used to run populations from
    # a file containing binary_c calls
    ###################################################

    def _source_file_sampling_cleanup(self):
        """
        Cleanup function for the evolution type source file sampling
        """

        pass

    def _source_file_sampling_dry_run(self):
        """
        Function to go through the source_file and count the number of lines and the total probability
        """

        system_generator = self.population_options["_system_generator"]
        total_starcount = 0

        for _ in system_generator:
            total_starcount += 1

        total_starcount = system_generator(self)
        self.population_options["_total_starcount"] = total_starcount

        #
        self.vb_error(
            message="Total starcount with source file sampling will be: {}".format(
                self.population_options["_total_starcount"]
            ),
        )

    def _source_file_sampling_load_file(self, check=False):
        """
        Function that loads the source_file that contains a binary_c calls
        """

        if not os.path.isfile(self.population_options["source_file_sampling_filename"]):
            self.vb_critical("Source file doesnt exist")

        self.vb_error(
            message="Loading source file from {}".format(
                self.population_options["source_file_sampling_filename"]
            ),
        )

        # We can choose to perform a check on the source file, which checks if the lines start with 'binary_c'
        if check:
            source_file_check_filehandle = self.open(
                self.population_options["source_file_sampling_filename"],
                "r",
                encoding="utf-8",
            )
            for line in source_file_check_filehandle:
                if not line.startswith("binary_c"):
                    failed = True
                    break
            if failed:
                self.vb_critical(
                    "Error, sourcefile contains lines that do not start with binary_c",
                )
                raise ValueError

        # Get the filehandle
        source_file_filehandle = self.open(
            self.population_options["source_file_sampling_filename"],
            "r",
            encoding="utf-8",
        )

        self.population_options["_source_file_filehandle"] = source_file_filehandle

        self.vb_error("Source file loaded")

    def _source_file_sampling_system_dict_from_line_header_style(
        self, line, header_list
    ):
        """
        Function to create a dictionary from a line in the source file if 'source_file_sampling_type' == 'column'
        """

        system_dict = {}

        # Clean and split line
        cleaned_line = line.strip()
        split_line = cleaned_line.split()

        # check line length
        if not len(split_line) == len(header_list):
            raise ValueError("Number of columns and values do not match.")

        # Loop over elements of the split line
        for i, split_line_el in enumerate(split_line):
            system_dict[header_list[i]] = _source_file_sampling_parse_values(
                split_line_el
            )

        return system_dict

    def _source_file_sampling_system_dict_from_line_command_style(self, line):
        """
        Function to create a dictionary from a line in the source file if 'source_file_sampling_type' == 'command'
        """

        system_dict = {}

        # chop off binary_c prepend
        if line.startswith("binary_c "):
            line = line.replace("binary_c ", "")
        cleaned_line = line.strip()

        # Split line
        split_line = cleaned_line.split()

        # check if length is correct
        if not len(split_line) % 2 == 0:
            raise ValueError(
                "Number of keys does not match the number of values. Please check the source file"
            )

        # Loop over elements of the split line
        for i in range(0, len(split_line), 2):
            system_dict[split_line[i]] = _source_file_sampling_parse_values(
                split_line[i + 1]
            )

        return system_dict

    def _source_file_sampling_setup(self):
        """
        setup function for the source file sampling evolution method
        """

        # check if file exists
        if not os.path.isfile(self.population_options["source_file_sampling_filename"]):
            self.vb_critical("Source file doesnt exist")

        # check choice of sampling_file type:
        if self.population_options["source_file_sampling_type"] not in [
            "command",
            "column",
        ]:
            raise ValueError(
                "Choice of source_file_sampling_type ({}) not supported. Please choose from ['command', 'column']".format(
                    self.population_options["source_file_sampling_type"]
                )
            )

        # # TODO: re-implement Handle dry run

    def _source_file_sampling_generator(self):
        """
        Generator function for the source file sampling
        """

        # Handle the header line if the source file type
        if self.population_options["source_file_sampling_type"] == "column":
            headerline = (
                self.population_options["_source_file_filehandle"].readline().strip()
            )
            header_list = headerline.split()

        # Loop over lines in source filehandle
        for line in self.population_options["_source_file_filehandle"]:
            # Handle readout of lines
            if self.population_options["source_file_sampling_type"] == "command":
                system_dict = (
                    self._source_file_sampling_system_dict_from_line_command_style(
                        line=line
                    )
                )
            elif self.population_options["source_file_sampling_type"] == "column":
                system_dict = (
                    self._source_file_sampling_system_dict_from_line_header_style(
                        line=line, header_list=header_list
                    )
                )
            else:
                raise ValueError(
                    "Choice of source_file_sampling_type ({}) not supported. Please choose from ['command', 'column']".format(
                        self.population_options["source_file_sampling_type"]
                    )
                )

            yield system_dict

        # close filehandle when finished
        self.population_options["_source_file_filehandle"].close()

    def _source_file_sampling_get_generator(self):
        """
        Function to get the generator for the source_file sampling method. Called by _get_generator and used in the actual evolution loop.
        """

        # load source-file
        self._source_file_sampling_load_file()

        generator = self._source_file_sampling_generator()

        return generator
