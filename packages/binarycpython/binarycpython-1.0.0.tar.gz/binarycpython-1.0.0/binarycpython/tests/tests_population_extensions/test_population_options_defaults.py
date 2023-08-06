"""
Unittests for population_options_defaults module

TODO: get_population_options_defaults_dict
TODO: get_population_options_descriptions
TODO: print_option_descriptions
TODO: default_cache_dir
"""
import os
import unittest

import voluptuous as vol

from binarycpython import Population
from binarycpython.utils.functions import Capturing, temp_dir

TMP_DIR = temp_dir("tests", "test_population_options_defaults")


class test_population_options_validation(unittest.TestCase):
    """
    Unit tests for the population_options validation of input
    """

    def test_population_options_validation(self):
        with Capturing() as _:
            self._test_population_options_validation()

    def _test_population_options_validation(self):
        """
        Unit tests for the population_options validation of input
        """

        population_options_defaults_pop = Population()

        # Check if the validation works
        with self.assertRaises(vol.error.MultipleInvalid):
            population_options_defaults_pop.set(num_cores=[])

        with self.assertRaises(vol.error.MultipleInvalid):
            population_options_defaults_pop.set(_binary_c_dir=1)


class test_population_options_description_checker(unittest.TestCase):
    """
    Unit tests for the population_options_description_checker function
    """

    def test_population_options_description_checker(self):
        with Capturing() as _:
            self._test_population_options_description_checker()

    def _test_population_options_description_checker(self):
        """
        Unit tests for the population_options_description_checker function
        """

        #
        population_options_defaults_pop = Population()
        population_options_defaults_dict = (
            population_options_defaults_pop.population_options_defaults_dict
        )

        # loop over all entries and check if they have descriptions
        for key, value in population_options_defaults_dict.items():
            self.assertTrue(
                "description" in value, msg="{} entry has no description.".format(key)
            )

    def test_moedistefano_options_description_checker(self):
        with Capturing() as _:
            self._test_moedistefano_options_description_checker()

    def _test_moedistefano_options_description_checker(self):
        """
        Tests to check the moedistefano option descriptions
        """

        population_options_defaults_pop = Population()
        moe_di_stefano_default_dict = (
            population_options_defaults_pop.moe_distefano_options_defaults_dict
        )

        # loop over all entries and check if they have descriptions
        for key, value in moe_di_stefano_default_dict.items():
            self.assertTrue(
                "description" in value, msg="{} entry has no description.".format(key)
            )


class test_write_population_options_to_rst_file(unittest.TestCase):
    """
    Unit tests for the write_population_options_to_rst_file function
    """

    def test_write_population_options_to_rst_file(self):
        with Capturing() as _:
            self._test_write_population_options_to_rst_file()

    def _test_write_population_options_to_rst_file(self):
        """
        Unit tests for the population_options_description_checker function
        """

        population_options_defaults_pop = Population()

        input_1 = os.path.join(
            TMP_DIR, "test_write_population_options_to_rst_file_1.txt"
        )
        self.assertRaises(
            ValueError,
            population_options_defaults_pop.write_population_options_to_rst_file,
            input_1,
        )

        input_2 = os.path.join(
            TMP_DIR, "test_write_population_options_to_rst_file_2.rst"
        )
        _ = population_options_defaults_pop.write_population_options_to_rst_file(
            input_2
        )

        self.assertTrue(os.path.isfile(input_2))


if __name__ == "__main__":
    unittest.main()
