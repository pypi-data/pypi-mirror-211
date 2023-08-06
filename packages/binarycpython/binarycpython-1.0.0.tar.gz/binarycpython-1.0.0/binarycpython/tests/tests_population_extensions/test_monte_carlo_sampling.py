"""
Test routines for the monte-carlo sampling
"""

import inspect
import unittest

from binarycpython import Population
from binarycpython.utils.functions import Capturing, temp_dir

TMP_DIR = temp_dir("tests", "test_monte_carlo_sampling")


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


class test_mass_treshold_functionality(unittest.TestCase):
    """
    Class for unit test for the mass-threshold terminator for monte-carlo sampling
    """

    def test_mass_treshold(self):
        with Capturing() as _:
            self._test_mass_treshold()

    def _test_mass_treshold(self):
        """
        Unittest for the function flat
        """

        resolution = {"M_1": 10, "q": 10}
        mass_threshold = 10

        class MC_Population(Population):
            def _monte_carlo_sampling_cleanup(self):
                """
                Override the cleanup function so some of the threshold information is still available
                """

                pass

        #
        monte_carlo_pop = MC_Population(tmp_dir=TMP_DIR, evolution_type="monte_carlo")

        # configure
        monte_carlo_pop.set(
            monte_carlo_mass_threshold=mass_threshold,
            _actually_evolve_system=False,
            num_cores=1,
        )

        # Set up sampling variable
        monte_carlo_pop.add_sampling_variable(
            # name="lnm1",
            name="M_1",
            longname="Primary mass",
            valuerange=[0.06, 300],
            samplerfunc="10**self.const_linear(np.log10(0.10001), np.log10(300), {})".format(
                resolution["M_1"]
            ),  # TODO: this one is not necessary for MC sampling
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 301, -1.3, -2.3, -2.3)",
            bottomcode="multiplicity = self._sample_multiplicity(system_dict); system_dict['multiplicity'] = multiplicity;",
            dphasevol="dlnm1",
            parameter_name="M_1",
            branchpoint=1,
            branchcode="multiplicity == 1",
        )

        # Add q sampling variable
        monte_carlo_pop.add_sampling_variable(
            name="q",
            longname="Mass ratio",
            valuerange=["0.1/M_1", 1],
            samplerfunc="self.const_linear(0.1/M_1, 1, {})".format(resolution["q"]),
            probdist="self.flatsections(q, [{'min': 0.1/M_1, 'max': 1.0, 'height': 1}])",
            dphasevol="dq",
            precode="M_2 = q * M_1",
            parameter_name="M_2",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
            dependency_variables=["M_1"],
            branchpoint=1,
            branchcode="multiplicity == 2",
        )

        # run MC sampling until threshold
        monte_carlo_pop.evolve()

        # Since we always stop AFTER hitting the threshold we should provide some margin (i.e. delta) to the check.
        self.assertAlmostEqual(
            monte_carlo_pop.grid_options["_monte_carlo_current_total_mass_evolved"],
            mass_threshold,
            delta=1,
        )


class test_monte_carlo_sampling_load_sampling_functions_file(unittest.TestCase):
    """
    Unit test for _monte_carlo_sampling_load_sampling_functions_file
    """

    def test_monte_carlo_sampling_load_sampling_functions_file(self):
        with Capturing() as _:
            self._test_monte_carlo_sampling_load_sampling_functions_file()

    def _test_monte_carlo_sampling_load_sampling_functions_file(self):
        """
        Unittest for the function _monte_carlo_sampling_load_sampling_functions_file
        """

        resolution = {"M_1": 10}
        mass_threshold = 1

        #
        monte_carlo_pop = Population(tmp_dir=TMP_DIR, evolution_type="monte_carlo")

        # configure
        monte_carlo_pop.set(
            monte_carlo_mass_threshold=mass_threshold,
            _actually_evolve_system=False,
            num_cores=1,
        )

        # Set up sampling variable
        monte_carlo_pop.add_sampling_variable(
            # name="lnm1",
            name="M_1",
            longname="Primary mass",
            valuerange=[0.06, 300],
            samplerfunc="10**self.const_linear(np.log10(0.10001), np.log10(300), {})".format(
                resolution["M_1"]
            ),  # TODO: this one is not necessary for MC sampling
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 301, -1.3, -2.3, -2.3)",
            bottomcode="multiplicity = self._sample_multiplicity(system_dict); system_dict['multiplicity'] = multiplicity;",
            dphasevol="dlnm1",
            parameter_name="M_1",
            branchpoint=1,
            branchcode="multiplicity == 1",
        )

        # Handle setup and get the generator
        monte_carlo_pop._setup()
        monte_carlo_pop._get_generator()

        # Check if functions exit
        self.assertTrue("calc_pdf_cdf_value_array_dict_M_1" in dir(monte_carlo_pop))
        self.assertTrue("calc_sampled_value_M_1" in dir(monte_carlo_pop))

        # Get a custom sample
        custom_sample = monte_carlo_pop.calc_sampled_value_M_1(monte_carlo_pop)
        self.assertTrue(isinstance(custom_sample, float))

        # inspect the pdf-cdf value array
        pdf_cdf_value_array_dict = monte_carlo_pop.calc_pdf_cdf_value_array_dict_M_1(
            monte_carlo_pop
        )
        self.assertIn("probability_array", pdf_cdf_value_array_dict)
        self.assertIn("cdf_array", pdf_cdf_value_array_dict)
        self.assertIn("value_array", pdf_cdf_value_array_dict)
        self.assertIn("parameter_value_array", pdf_cdf_value_array_dict)
        self.assertTrue(len(pdf_cdf_value_array_dict["probability_array"]) > 0)
        self.assertTrue(
            len(pdf_cdf_value_array_dict["probability_array"])
            == len(pdf_cdf_value_array_dict["value_array"])
        )
        self.assertTrue(
            len(pdf_cdf_value_array_dict["probability_array"])
            == len(pdf_cdf_value_array_dict["cdf_array"])
        )
        self.assertTrue(
            len(pdf_cdf_value_array_dict["probability_array"])
            == len(pdf_cdf_value_array_dict["parameter_value_array"])
        )


class test_monte_carlo_sampling_load_generator(unittest.TestCase):
    """
    Unit test for _monte_carlo_sampling_load_generator
    """

    def test_monte_carlo_sampling_load_generator(self):
        with Capturing() as _:
            self._test_monte_carlo_sampling_load_generator()

    def _test_monte_carlo_sampling_load_generator(self):
        """
        Unittest for the function _monte_carlo_sampling_load_sampling_functions_file
        """

        resolution = {"M_1": 10}
        mass_threshold = 1

        #
        monte_carlo_pop = Population(tmp_dir=TMP_DIR, evolution_type="monte_carlo")

        # configure
        monte_carlo_pop.set(
            monte_carlo_mass_threshold=mass_threshold,
            _actually_evolve_system=False,
            num_cores=1,
        )

        # Set up sampling variable
        monte_carlo_pop.add_sampling_variable(
            # name="lnm1",
            name="M_1",
            longname="Primary mass",
            valuerange=[0.06, 300],
            samplerfunc="10**self.const_linear(np.log10(0.10001), np.log10(300), {})".format(
                resolution["M_1"]
            ),  # TODO: this one is not necessary for MC sampling
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 301, -1.3, -2.3, -2.3)",
            bottomcode="multiplicity = self._sample_multiplicity(system_dict); system_dict['multiplicity'] = multiplicity;",
            dphasevol="dlnm1",
            parameter_name="M_1",
            branchpoint=1,
            branchcode="multiplicity == 1",
        )

        # Handle setup and get the generator
        monte_carlo_pop._setup()
        monte_carlo_pop._get_generator()

        # Check if functions exit
        self.assertTrue(
            "_monte_carlo_sampling_generator" in monte_carlo_pop.grid_options
        )
        self.assertTrue(
            inspect.isgeneratorfunction(
                monte_carlo_pop.grid_options["_monte_carlo_sampling_generator"]
            )
        )


class test_monte_carlo_use_pre_calculated_distributions(unittest.TestCase):
    """
    Unit test for _monte_carlo_sampling_load_sampling_functions_file
    """

    def test_monte_carlo_use_pre_calculated_distributions(self):
        with Capturing() as _:
            self._test_monte_carlo_use_pre_calculated_distributions()

    def _test_monte_carlo_use_pre_calculated_distributions(self):
        """
        Unittest for the function _monte_carlo_sampling_load_sampling_functions_file
        """

        resolution = {"M_1": 10, "q": 10}
        mass_threshold = 1

        #
        monte_carlo_pop = Population(tmp_dir=TMP_DIR, evolution_type="monte_carlo")

        # configure
        monte_carlo_pop.set(
            monte_carlo_mass_threshold=mass_threshold,
            _actually_evolve_system=False,
            num_cores=1,
            monte_carlo_use_pre_calculated_distributions=True,
        )

        # Set up sampling variable
        monte_carlo_pop.add_sampling_variable(
            # name="lnm1",
            name="M_1",
            longname="Primary mass",
            valuerange=[0.06, 300],
            samplerfunc="10**self.const_linear(np.log10(0.10001), np.log10(300), {})".format(
                resolution["M_1"]
            ),  # TODO: this one is not necessary for MC sampling
            probdist="self.three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 301, -1.3, -2.3, -2.3)",
            bottomcode="multiplicity = self._sample_multiplicity(system_dict); system_dict['multiplicity'] = multiplicity;",
            dphasevol="dlnm1",
            parameter_name="M_1",
            branchpoint=1,
            branchcode="multiplicity == 1",
        )

        # Add q sampling variable
        monte_carlo_pop.add_sampling_variable(
            name="q",
            longname="Mass ratio",
            valuerange=["0.1/M_1", 1],
            samplerfunc="self.const_linear(0.1/M_1, 1, {})".format(resolution["q"]),
            probdist="self.flatsections(q, [{'min': 0.1/M_1, 'max': 1.0, 'height': 1}])",
            dphasevol="dq",
            precode="M_2 = q * M_1",
            parameter_name="M_2",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
            dependency_variables=["M_1"],
            branchpoint=1,
            branchcode="multiplicity == 2",
        )

        # Handle setup and get the generator
        monte_carlo_pop._setup()
        monte_carlo_pop._get_generator()

        # Check if functions exists
        self.assertTrue("handle_pre_calc" in dir(monte_carlo_pop))

        # Call function to do the pre-calculation of the pdf-cdf value arrays. These can be nested when sampling variables depend on other sampling variables
        monte_carlo_pop.handle_pre_calc(monte_carlo_pop)

        # Check components of the pre_calculate_pdf_cdf_value_array_dict
        self.assertTrue(
            "pre_calculated_pdf_cdf_value_array_dicts" in dir(monte_carlo_pop)
        )
        pre_calculated_pdf_cdf_value_array_dicts = (
            monte_carlo_pop.pre_calculated_pdf_cdf_value_array_dicts
        )

        #############
        # M_1 checks

        # Check if the M_1 is in the pre_calculated dict
        self.assertIn("M_1", pre_calculated_pdf_cdf_value_array_dicts)

        # Check if it has the correct components
        self.assertIn(
            "probability_array", pre_calculated_pdf_cdf_value_array_dicts["M_1"]
        )
        self.assertIn("cdf_array", pre_calculated_pdf_cdf_value_array_dicts["M_1"])
        self.assertIn("value_array", pre_calculated_pdf_cdf_value_array_dicts["M_1"])
        self.assertIn(
            "parameter_value_array", pre_calculated_pdf_cdf_value_array_dicts["M_1"]
        )

        # check if the components have the correct length
        self.assertTrue(
            len(pre_calculated_pdf_cdf_value_array_dicts["M_1"]["probability_array"])
            > 0
        )
        self.assertTrue(
            len(pre_calculated_pdf_cdf_value_array_dicts["M_1"]["probability_array"])
            == len(pre_calculated_pdf_cdf_value_array_dicts["M_1"]["value_array"])
        )
        self.assertTrue(
            len(pre_calculated_pdf_cdf_value_array_dicts["M_1"]["probability_array"])
            == len(pre_calculated_pdf_cdf_value_array_dicts["M_1"]["cdf_array"])
        )
        self.assertTrue(
            len(pre_calculated_pdf_cdf_value_array_dicts["M_1"]["probability_array"])
            == len(
                pre_calculated_pdf_cdf_value_array_dicts["M_1"]["parameter_value_array"]
            )
        )

        ##########
        # M_2 checks
        self.assertIn("M_2", pre_calculated_pdf_cdf_value_array_dicts)

        # check if all keys for M_2 are float-strings
        M_2_keys = pre_calculated_pdf_cdf_value_array_dicts["M_2"].keys()
        for key in M_2_keys:
            self.assertTrue(isfloat(key))

        # Check if the structure of the first is good
        first_M_2_entry = pre_calculated_pdf_cdf_value_array_dicts["M_2"][
            list(M_2_keys)[0]
        ]

        # Check if it has the correct components
        self.assertIn("probability_array", first_M_2_entry)
        self.assertIn("cdf_array", first_M_2_entry)
        self.assertIn("value_array", first_M_2_entry)
        self.assertIn("parameter_value_array", first_M_2_entry)

        # check if the components have the correct length
        self.assertTrue(len(first_M_2_entry["probability_array"]) > 0)
        self.assertTrue(
            len(first_M_2_entry["probability_array"])
            == len(first_M_2_entry["value_array"])
        )
        self.assertTrue(
            len(first_M_2_entry["probability_array"])
            == len(first_M_2_entry["cdf_array"])
        )
        self.assertTrue(
            len(first_M_2_entry["probability_array"])
            == len(first_M_2_entry["parameter_value_array"])
        )


if __name__ == "__main__":
    # test = test_mass_treshold_functionality()
    # test._test_mass_treshold()

    # test = test_monte_carlo_sampling_load_sampling_functions_file()
    # test.test_monte_carlo_sampling_load_sampling_functions_file()

    # test = test_monte_carlo_sampling_load_generator()
    # test.test_monte_carlo_sampling_load_generator()

    # test = test_monte_carlo_use_pre_calculated_distributions()
    # test._test_monte_carlo_use_pre_calculated_distributions()

    unittest.main()
