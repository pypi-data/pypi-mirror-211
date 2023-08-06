"""
Main script to provide the ensemble class extensions
"""

# pylint: disable=E1101
import os

from binarycpython import _binary_c_bindings
from binarycpython.utils.ensemble import extract_ensemble_json_from_string


class ensemble:
    """
    Extension for the Population class containing the code for ensemble-related class methods
    """

    def __init__(self, **kwargs):
        """
        Init function for the ensemble class
        """

        return

    def _ensemble_setup(self):
        """
        Function to prepare the class to include ensemble output
        """

        if not self.bse_options.get("ensemble_defer", 0) == 1:
            self.vb_error(
                "Error, if you want to run an ensemble in a population, the output needs to be deferred. Please set 'ensemble_defer' to 1",
            )
            raise ValueError

        if not any([key.startswith("ensemble_filter_") for key in self.bse_options]):
            self.vb_warning(
                "Warning: Running the ensemble without any filter requires a lot of available RAM",
            )

        if self.bse_options.get("ensemble_filters_off", 0) != 1:
            self.vb_warning(
                "Warning: Running the ensemble without any filter requires a lot of available RAM",
            )

        if not self.population_options["combine_ensemble_with_thread_joining"]:
            if not self.custom_options.get("data_dir", None):
                self.vb_error(
                    "Error: chosen to write the ensemble output directly to files but data_dir isn't set",
                )
                raise ValueError

    def _process_handle_ensemble_output(self, ID):
        """
        Function to handle the ensemble output of a worker process that is finishing
        """

        # if ensemble==1, then either directly write that data to a file, or combine everything into 1 file.
        ensemble_json = {}  # Make sure it exists already
        if self.bse_options.get("ensemble", 0) == 1:
            self.vb_info(
                "Process {}: is freeing ensemble output (using persistent_data memaddr {})".format(
                    ID, self.persistent_data_memory_dict[self.process_ID]
                ),
            )

            ensemble_raw_output = (
                _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
                    self.persistent_data_memory_dict[self.process_ID]
                )
            )

            if ensemble_raw_output is None:
                self.vb_warning(
                    "Process {}: Warning! Ensemble output is empty. ".format(ID),
                )
                ensemble_output = None
            else:
                # convert ensemble_raw_output to a dictionary
                ensemble_output = extract_ensemble_json_from_string(ensemble_raw_output)

            # save the ensemble chunk to a file
            if (
                self.population_options["save_ensemble_chunks"] is True
                or self.population_options["combine_ensemble_with_thread_joining"]
                is False
            ):

                output_file = os.path.join(
                    self.custom_options["data_dir"],
                    "ensemble_output_{}_{}.json".format(
                        self.population_options["_population_id"], self.process_ID
                    ),
                )
                self.vb_info(
                    "Writing process {} JSON ensemble chunk output to {} ".format(
                        ID, output_file
                    ),
                )

                ensemble_output = extract_ensemble_json_from_string(ensemble_raw_output)
                self.write_ensemble(output_file, ensemble_output)

            # combine ensemble chunks
            if self.population_options["combine_ensemble_with_thread_joining"] is True:
                self.vb_info(
                    "Process {}: Extracting ensemble info from raw string".format(ID),
                )
                ensemble_json["ensemble"] = ensemble_output

        return ensemble_json
