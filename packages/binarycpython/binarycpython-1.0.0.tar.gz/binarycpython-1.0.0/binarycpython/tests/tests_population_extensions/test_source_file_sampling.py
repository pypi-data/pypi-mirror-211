"""
Unit test classes for the source_file_sampling module population extension
"""

import os
import unittest

from binarycpython.utils.functions import Capturing, temp_dir
from binarycpython.utils.population_class import Population

TMP_DIR = temp_dir("tests", "test_source_file_sampling")


class test_source_file_sampling_command_type(unittest.TestCase):
    """
    Class for unit test of flat
    """

    def test_source_file_sampling_command_type2(self):
        with Capturing() as _:
            self._test_source_file_sampling_command_type()

    def _test_source_file_sampling_command_type(self):
        """
        Unittest for source file sampling with a command type source file
        """

        system_dict_test_list = [
            {"M_1": 10.0, "M_2": 5.0, "BH_prescription": "BH_FRYER12_DELAYED"},
            {"M_1": 2, "M_2": 0.1, "orbital_period": 100.0},
        ]

        # Create file that contains the
        source_file_sampling_filename = os.path.join(
            TMP_DIR, "command_type_source_file_sampling_filename.txt"
        )

        # write system dicts to file appropriately
        with open(source_file_sampling_filename, "w") as f:
            # Loop over system dict
            for system_dict_test_entry in system_dict_test_list:
                argline = " ".join(
                    [
                        "{} {}".format(key, val)
                        for key, val in system_dict_test_entry.items()
                    ]
                )
                f.write(argline + "\n")

        # Set population object
        source_file_sampling_pop = Population(tmp_dir=TMP_DIR)
        source_file_sampling_pop.set(
            evolution_type="source_file",
            source_file_sampling_type="command",
            source_file_sampling_filename=source_file_sampling_filename,
            _actually_evolve_system=False,
        )

        # Setup and get the generator
        source_file_sampling_pop._setup()
        generator = source_file_sampling_pop._get_generator()

        # Loop over the system dicts
        for system_i, system_dict in enumerate(generator):
            self.assertEqual(system_dict, system_dict_test_list[system_i])

        # Delete test file and cleanup the population
        os.remove(source_file_sampling_filename)
        source_file_sampling_pop._cleanup()


class test_source_file_sampling_column_type(unittest.TestCase):
    """
    Class for unit test of flat
    """

    def test_source_file_sampling_column_type(self):
        with Capturing() as _:
            self._test_source_file_sampling_column_type()

    def _test_source_file_sampling_column_type(self):
        """
        Unittest for source file sampling with a column type source file
        """

        system_dict_test_list = [
            {
                "M_1": 10.0,
                "M_2": 5.0,
                "orbital_period": 1.0,
                "BH_prescription": "BH_FRYER12_DELAYED",
            },
            {
                "M_1": 2,
                "M_2": 0.1,
                "orbital_period": 100.0,
                "BH_prescription": "BH_FRYER12_DELAYED",
            },
        ]

        # Create file that contains the
        source_file_sampling_filename = os.path.join(
            TMP_DIR, "column_type_source_file_sampling_filename.txt"
        )

        # write system dicts to file appropriately
        with open(source_file_sampling_filename, "w") as f:

            # get header list and write
            header_list = list(system_dict_test_list[0].keys())
            header_line = " ".join(header_list)
            f.write(header_line + "\n")

            # Loop over system dict
            for system_dict_test_entry in system_dict_test_list:
                argline = " ".join(
                    ["{}".format(system_dict_test_entry[key]) for key in header_list]
                )
                f.write(argline + "\n")

        # Set population object
        source_file_sampling_pop = Population(tmp_dir=TMP_DIR)
        source_file_sampling_pop.set(
            evolution_type="source_file",
            source_file_sampling_type="column",
            source_file_sampling_filename=source_file_sampling_filename,
            _actually_evolve_system=False,
        )

        # Setup and get the generator
        source_file_sampling_pop._setup()
        generator = source_file_sampling_pop._get_generator()

        # Loop over the system dicts
        for system_i, system_dict in enumerate(generator):
            self.assertEqual(system_dict, system_dict_test_list[system_i])

        # Delete test file and cleanup the population
        os.remove(source_file_sampling_filename)
        source_file_sampling_pop._cleanup()


if __name__ == "__main__":
    unittest.main()
