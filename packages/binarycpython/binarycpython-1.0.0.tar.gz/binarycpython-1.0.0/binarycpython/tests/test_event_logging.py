"""
Tests for the event logging
"""

import os
import shutil
import unittest

from binarycpython import Population
from binarycpython.utils.event_logging import (
    event_based_logging_event_dict,
    event_based_logging_parameter_description_dict,
)
from binarycpython.utils.functions import Capturing, temp_dir

TMP_DIR = temp_dir("tests", "test_event_logging", clean_path=True)
EVENT_TYPE_INDEX = 3


def setup_data_dir(dirname):
    """
    Function to ensure that directory is deleted and created again
    """

    data_dir = os.path.join(TMP_DIR, dirname)
    if os.path.isdir(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir, exist_ok=True)

    return data_dir


def write_source_file_sampling_file(
    source_file_sampling_filename, system_dict_test_list
):
    """
    utility function to write the source file sampling file
    """

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


class test_event_types(unittest.TestCase):
    """
    Unittests for different event types
    """

    def test_SN_single(self):
        with Capturing() as _:
            self._test_SN_single()

    def _test_SN_single(self):
        """
        Function to test if single SN events are present in the binary_c output
        and whether the parameters contained in the list are the same as the expected parameters.
        """

        event_type = "SN_SINGLE"

        pop = Population(tmp_dir=TMP_DIR)

        pop.set(
            event_based_logging_SN=1,
            M_1=10,
        )

        # evolve single system
        single_evo = pop.evolve_single()

        # Check if "SN_SINGLE" is contained in the logstring
        self.assertTrue(event_type in single_evo)

        # Check if the length of the logstring matches the expected length
        for line in single_evo.split("\n"):
            if line.startswith("EVENT"):
                event_log_values = line.split()[1:]

                # select current event type
                if event_log_values[EVENT_TYPE_INDEX] == event_type:
                    self.assertTrue(
                        len(event_log_values)
                        == len(
                            pop.population_options[
                                "event_based_logging_parameter_list_dict"
                            ][event_type]
                        )
                    )

    def test_SN_binary(self):
        with Capturing() as _:
            self._test_SN_binary()

    def _test_SN_binary(self):
        """
        Function to test if binary SN events are present in the binary_c output
        and whether the parameters contained in the list are the same as the expected parameters.
        """

        event_type = "SN_BINARY"

        pop = Population(tmp_dir=TMP_DIR)

        pop.set(
            event_based_logging_SN=1,
            M_1=10,
            M_2=0.1,
            orbital_period=1000000000,
        )

        # evolve single system
        single_evo = pop.evolve_single()

        # Check if "SN_SINGLE" is contained in the logstring
        self.assertTrue(event_type in single_evo)

        # Check if the length of the logstring matches the expected length
        for line in single_evo.split("\n"):
            if line.startswith("EVENT"):
                event_log_values = line.split()[1:]

                # select current event type
                if event_log_values[EVENT_TYPE_INDEX] == event_type:
                    self.assertTrue(
                        len(event_log_values)
                        == len(
                            pop.population_options[
                                "event_based_logging_parameter_list_dict"
                            ][event_type]
                        )
                    )

    def test_RLOF(self):
        with Capturing() as _:
            self._test_RLOF()

    def _test_RLOF(self):
        """
        Function to test if RLOF events are present in the binary_c output
        and whether the parameters contained in the list are the same as the expected parameters.
        """

        event_type = "RLOF"

        pop = Population(tmp_dir=TMP_DIR)

        pop.set(
            event_based_logging_RLOF=1,
            M_1=1,
            M_2=0.5,
            orbital_period=100,
        )

        # evolve single system
        single_evo = pop.evolve_single()

        # Check if "SN_SINGLE" is contained in the logstring
        self.assertTrue(event_type in single_evo)

        # Check if the length of the logstring matches the expected length
        for line in single_evo.split("\n"):
            if line.startswith("EVENT"):
                event_log_values = line.split()[1:]

                # select current event type
                if event_log_values[EVENT_TYPE_INDEX] == event_type:
                    self.assertTrue(
                        len(event_log_values)
                        == len(
                            pop.population_options[
                                "event_based_logging_parameter_list_dict"
                            ][event_type]
                        )
                    )

    def test_DCO_formation(self):
        with Capturing() as _:
            self._test_DCO_formation()

    def _test_DCO_formation(self):
        """
        Function to test if DCO_formation events are present in the binary_c output
        and whether the parameters contained in the list are the same as the expected parameters.
        """

        event_type = "DCO_formation"

        pop = Population(tmp_dir=TMP_DIR)

        pop.set(
            event_based_logging_DCO=1,
            M_1=100,
            M_2=20,
            orbital_period=10000000,
        )

        # evolve single system
        single_evo = pop.evolve_single()

        # Check if "SN_SINGLE" is contained in the logstring
        self.assertTrue(event_type in single_evo)

        # Check if the length of the logstring matches the expected length
        for line in single_evo.split("\n"):
            if line.startswith("EVENT"):
                event_log_values = line.split()[1:]

                # select current event type
                if event_log_values[EVENT_TYPE_INDEX] == event_type:
                    self.assertTrue(
                        len(event_log_values)
                        == len(
                            pop.population_options[
                                "event_based_logging_parameter_list_dict"
                            ][event_type]
                        )
                    )


class test_event_parameter_descriptions(unittest.TestCase):
    """
    Unittests to check if the descriptions are present
    """

    def test_event_descriptions(self):
        with Capturing() as _:
            self._test_event_descriptions()

    def _test_event_descriptions(self):
        """
        Function to test if all the descriptions are present
        """

        # Loop over known events
        for _, event_dict in event_based_logging_event_dict.items():
            # check if event dict contains a description
            self.assertTrue("description" in event_dict.keys())
            self.assertTrue(isinstance(event_dict["description"], str))
            self.assertTrue(len(event_dict["description"]) > 0)

    def test_parameter_descriptions(self):
        with Capturing() as _:
            self._test_parameter_descriptions()

    def _test_parameter_descriptions(self):
        """
        Function to test if all the descriptions are present
        """

        # Loop over known events
        for _, event_dict in event_based_logging_event_dict.items():

            # check if event dict contains a description
            self.assertIn("parameter_list", event_dict.keys())
            self.assertTrue(isinstance(event_dict["parameter_list"], list))
            self.assertTrue(len(event_dict["parameter_list"]) > 0)

            # Loop over parameters and check if they have descriptions
            for parameter in event_dict["parameter_list"]:
                self.assertIn(parameter, event_based_logging_parameter_description_dict)
                self.assertIn(
                    "description",
                    event_based_logging_parameter_description_dict[parameter],
                )
                self.assertTrue(
                    isinstance(
                        event_based_logging_parameter_description_dict[parameter][
                            "description"
                        ],
                        str,
                    )
                )


class test_event_file_processing(unittest.TestCase):
    """
    Unittests to check if the files are processed correctly
    """

    def test_individual_event_file_processing(self):
        with Capturing() as _:
            self._test_individual_event_file_processing()

    def _test_individual_event_file_processing(self):
        """
        Function to test if the event files are processed correctly
        """

        # configure data dir
        data_dir = setup_data_dir("data_dir")

        #
        system_dict_test_list = [
            {"M_1": 10},
            {"M_1": 10.0, "M_2": 0.1, "orbital_period": 1000000000},
            {"M_1": 1, "M_2": 0.5, "orbital_period": 100.0},
        ]

        # Create file that contains the
        source_file_sampling_filename = os.path.join(
            TMP_DIR, "source_file_sampling_filename.txt"
        )

        write_source_file_sampling_file(
            source_file_sampling_filename, system_dict_test_list
        )

        # Set population object
        source_file_sampling_pop = Population(tmp_dir=TMP_DIR)
        source_file_sampling_pop.set(
            num_cores=2,
            data_dir=data_dir,
            evolution_type="source_file",
            source_file_sampling_type="command",
            source_file_sampling_filename=source_file_sampling_filename,
            event_based_logging_SN=1,
            event_based_logging_RLOF=1,
            event_based_logging_handle_output=True,
            event_based_logging_output_directory=os.path.join(TMP_DIR, "events"),
            event_based_logging_combine_individual_event_files=False,
            event_based_logging_remove_individual_event_files_after_combining=False,
            event_based_logging_split_events_file_to_each_type=False,
            event_based_logging_remove_original_combined_events_file_after_splitting=False,
        )

        source_file_sampling_pop.evolve()

        # Test if there are 2 files
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    source_file_sampling_pop.population_options[
                        "event_based_logging_output_directory"
                    ],
                    "events-0.dat",
                )
            )
        )
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    source_file_sampling_pop.population_options[
                        "event_based_logging_output_directory"
                    ],
                    "events-1.dat",
                )
            )
        )

        # Test if neither of them is empty
        with open(
            os.path.join(
                source_file_sampling_pop.population_options[
                    "event_based_logging_output_directory"
                ],
                "events-0.dat",
            )
        ) as f:
            content = f.read()
            self.assertTrue(len(content) > 0)

        with open(
            os.path.join(
                source_file_sampling_pop.population_options[
                    "event_based_logging_output_directory"
                ],
                "events-1.dat",
            )
        ) as f:
            content = f.read()
            self.assertTrue(len(content) > 0)

        #######
        # Test if in the files there are 3 unique events but individually only 1.
        all_events_list = []
        for file in ["events-0.dat", "events-1.dat"]:
            with open(
                os.path.join(
                    source_file_sampling_pop.population_options[
                        "event_based_logging_output_directory"
                    ],
                    file,
                )
            ) as f:
                for line in f:
                    all_events_list.append(line.strip())

        # extract event types
        all_event_types = []
        for event in all_events_list:
            all_event_types.append(event.split()[EVENT_TYPE_INDEX])

        # check unique events equals the number that we expect, and also that they only occur once
        self.assertTrue(len(set(all_event_types)) == 3)
        self.assertTrue(len(all_event_types) == 3)

    def test_combined_event_file_processing(self):
        with Capturing() as _:
            self._test_combined_event_file_processing()

    def _test_combined_event_file_processing(self):
        """
        Function to test if the event files are processed correctly
        """

        # configure data dir
        data_dir = setup_data_dir("data_dir")

        #
        system_dict_test_list = [
            {"M_1": 10},
            {"M_1": 10.0, "M_2": 0.1, "orbital_period": 1000000000},
            {"M_1": 1, "M_2": 0.5, "orbital_period": 100.0},
        ]

        # Create file that contains the
        source_file_sampling_filename = os.path.join(
            TMP_DIR, "source_file_sampling_filename.txt"
        )

        write_source_file_sampling_file(
            source_file_sampling_filename, system_dict_test_list
        )

        # Set population object
        source_file_sampling_pop = Population(tmp_dir=TMP_DIR)
        source_file_sampling_pop.set(
            num_cores=2,
            data_dir=data_dir,
            evolution_type="source_file",
            source_file_sampling_type="command",
            source_file_sampling_filename=source_file_sampling_filename,
            event_based_logging_SN=1,
            event_based_logging_RLOF=1,
            event_based_logging_handle_output=True,
            event_based_logging_output_directory=os.path.join(TMP_DIR, "events"),
            event_based_logging_combine_individual_event_files=True,
            event_based_logging_remove_individual_event_files_after_combining=True,
            event_based_logging_split_events_file_to_each_type=False,
            event_based_logging_remove_original_combined_events_file_after_splitting=False,
        )

        source_file_sampling_pop.evolve()

        combined_event_file_name = os.path.join(
            source_file_sampling_pop.population_options[
                "event_based_logging_output_directory"
            ],
            source_file_sampling_pop.population_options[
                "event_based_logging_combined_events_filename"
            ],
        )

        # Test if there is a combined event file
        self.assertTrue(os.path.isfile(combined_event_file_name))

        # Test that the individual files are not there
        self.assertFalse(
            os.path.isfile(
                os.path.join(
                    source_file_sampling_pop.population_options[
                        "event_based_logging_output_directory"
                    ],
                    "events-0.dat",
                )
            )
        )
        self.assertFalse(
            os.path.isfile(
                os.path.join(
                    source_file_sampling_pop.population_options[
                        "event_based_logging_output_directory"
                    ],
                    "events-1.dat",
                )
            )
        )

        # Test if neither of them is empty
        with open(combined_event_file_name) as f:
            content = f.read()
            self.assertTrue(len(content) > 0)

        #######
        # Test if in the files there are 3 unique events but individually only 1.
        all_events_list = []
        with open(combined_event_file_name) as f:
            for line in f:
                all_events_list.append(line.strip())

        # extract event types
        all_event_types = []
        for event in all_events_list:
            all_event_types.append(event.split()[EVENT_TYPE_INDEX])

        # check unique events equals the number that we expect, and also that they only occur once
        self.assertTrue(len(set(all_event_types)) == 3)
        self.assertTrue(len(all_event_types) == 3)

    def test_splitting_to_event_type(self):
        with Capturing() as _:
            self._test_splitting_to_event_type()

    def _test_splitting_to_event_type(self):
        """
        Function to test splitting the combined file to each unique event type
        """

        # configure data dir
        data_dir = setup_data_dir("data_dir")

        #
        system_dict_test_list = [
            {"M_1": 10},
            {"M_1": 10.0, "M_2": 0.1, "orbital_period": 1000000000},
            {"M_1": 1, "M_2": 0.5, "orbital_period": 100.0},
        ]

        # Create file that contains the
        source_file_sampling_filename = os.path.join(
            TMP_DIR, "source_file_sampling_filename.txt"
        )

        write_source_file_sampling_file(
            source_file_sampling_filename, system_dict_test_list
        )

        # Set population object
        source_file_sampling_pop = Population(tmp_dir=TMP_DIR)
        source_file_sampling_pop.set(
            num_cores=2,
            data_dir=data_dir,
            evolution_type="source_file",
            source_file_sampling_type="command",
            source_file_sampling_filename=source_file_sampling_filename,
            event_based_logging_SN=1,
            event_based_logging_RLOF=1,
            event_based_logging_handle_output=True,
            event_based_logging_output_directory=os.path.join(TMP_DIR, "events"),
            event_based_logging_combine_individual_event_files=True,
            event_based_logging_remove_individual_event_files_after_combining=True,
            event_based_logging_split_events_file_to_each_type=True,
            event_based_logging_remove_original_combined_events_file_after_splitting=True,
        )

        source_file_sampling_pop.evolve()
        combined_event_file_name = os.path.join(
            source_file_sampling_pop.population_options[
                "event_based_logging_output_directory"
            ],
            source_file_sampling_pop.population_options[
                "event_based_logging_combined_events_filename"
            ],
        )

        # Test that the individual files are not there
        self.assertFalse(
            os.path.isfile(
                os.path.join(
                    source_file_sampling_pop.population_options[
                        "event_based_logging_output_directory"
                    ],
                    "events-0.dat",
                )
            )
        )
        self.assertFalse(
            os.path.isfile(
                os.path.join(
                    source_file_sampling_pop.population_options[
                        "event_based_logging_output_directory"
                    ],
                    "events-1.dat",
                )
            )
        )
        self.assertFalse(os.path.isfile(combined_event_file_name))

        # Test that the per-event-type files exist:
        content_event_dir = os.listdir(
            source_file_sampling_pop.population_options[
                "event_based_logging_output_directory"
            ]
        )
        event_type_files = [
            filename for filename in content_event_dir if filename.startswith("total_")
        ]
        self.assertTrue(len(event_type_files) == 3)

        # test the content of each of the files:
        for event_type_file in event_type_files:
            full_path_event_type_file = os.path.join(
                source_file_sampling_pop.population_options[
                    "event_based_logging_output_directory"
                ],
                event_type_file,
            )

            # open file and check contents
            with open(full_path_event_type_file) as f:

                headerline = f.readline()
                self.assertTrue(headerline.strip().split()[0] == "uuid")

                #
                contentline = f.readline()
                self.assertTrue(len(contentline.strip().split()) > 0)

        # # Test if neither of them is empty
        # with open(combined_event_file_name) as f:
        #     content = f.read()
        #     self.assertTrue(len(content)>0)

        # #######
        # # Test if in the files there are 3 unique events but individually only 1.
        # all_events_list = []
        # with open(combined_event_file_name) as f:
        #     for line in f:
        #         all_events_list.append(line.strip())


if __name__ == "__main__":
    unittest.main()

    # test_event_file_processing_obj = test_event_file_processing()
    # test_event_file_processing_obj._test_individual_event_file_processing()
