"""
The class extension for the population object that contains analytics functionality
"""

# pylint: disable=E1101

import time


class analytics:
    """
    Extension for the Population class containing the functions for analytics
    """

    def __init__(self, **kwargs):
        """
        Init function for the analytics class
        """

        return

    #######################
    # time used functions
    #######################

    def make_analytics_dict(self):
        """
        Function to create the analytics dictionary
        """

        self.vb_info("Do analytics")

        analytics_dict = {}

        if self.population_options["do_analytics"]:
            # Put all interesting stuff in a variable and output that afterwards, as analytics of the run.
            analytics_dict = {
                "population_id": self.population_options["_population_id"],
                "evolution_type": self.population_options["evolution_type"],
                "failed_count": self.population_options["_failed_count"],
                "failed_prob": self.population_options["_failed_prob"],
                "failed_systems_error_codes": self.population_options[
                    "_failed_systems_error_codes"
                ].copy(),
                "errors_exceeded": self.population_options["_errors_exceeded"],
                "errors_found": self.population_options["_errors_found"],
                "total_probability": self.population_options["_probtot"],
                "total_count": self.population_options["_count"],
                "start_timestamp": self.population_options["_start_time_evolution"],
                "end_timestamp": self.population_options["_end_time_evolution"],
                "time_elapsed": self.time_elapsed(),
                "total_mass_run": self.population_options["_total_mass_run"],
                "total_probability_weighted_mass_run": self.population_options[
                    "_total_probability_weighted_mass_run"
                ],
                "zero_prob_stars_skipped": self.population_options[
                    "_zero_prob_stars_skipped"
                ],
            }

        if "metadata" in self.grid_ensemble_results:
            # Add analytics dict to the metadata too:
            self.grid_ensemble_results["metadata"].update(analytics_dict)
            self.vb_info("Added analytics to metadata")
            self.add_system_metadata()
        else:
            # use existing analytics dict
            analytics_dict = self.grid_ensemble_results.get("metadata", {})

        return analytics_dict

    def set_time(self, when):
        """
        Function to set the timestamp at when, where when is 'start' or 'end'.

        If when == end, we also calculate the time elapsed.
        """
        self.population_options["_" + when + "_time_evolution"] = time.time()
        if when == "end":
            self.population_options["_time_elapsed"] = self.time_elapsed(force=True)

    def time_elapsed(self, force=False):
        """
        Function to return how long a population object has been running.

        We return the cached value if it's available, and calculate
        the time elapsed if otherwise or if force is True
        """
        for x in ["_start_time_evolution", "_end_time_evolution"]:
            if not self.population_options[x]:
                self.population_options[x] = time.time()

        if force or "_time_elapsed" not in self.population_options:
            self.population_options["_time_elapsed"] = (
                self.population_options["_end_time_evolution"]
                - self.population_options["_start_time_evolution"]
            )

        return self.population_options["_time_elapsed"]

    def CPU_time(self):
        """
        Function to return how much CPU time we've used
        """

        dt = self.population_options["_time_elapsed"]

        ncpus = self.population_options.get("_num_processes", 1)

        return dt * ncpus
