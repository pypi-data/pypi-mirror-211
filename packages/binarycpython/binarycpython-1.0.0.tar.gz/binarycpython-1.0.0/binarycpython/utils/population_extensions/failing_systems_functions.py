"""
Main script to provide the failing systems functions class extension
"""

# pylint: disable=E1101

import datetime
import os


class failing_systems_functions:
    """
    Extension for the Population class containing the code for failing systems functionality
    """

    def __init__(self, **kwargs):
        """
        Init function for the spacing_functions class
        """

        return

    def _log_failure(
        self, system_dict=None, system_number=None, process=None, exitcode=None
    ):
        """
        Log failing or crashed system to file in log_failed_systems_dir
        """

        if (
            self.population_options["log_failed_systems"]
            and self.population_options["log_failed_systems_dir"] is not None
        ):
            path = os.path.join(self.population_options["log_failed_systems_dir"])
            os.makedirs(path, exist_ok=True)
            if self.dir_ok(path):
                failed_systems_file = os.path.join(
                    self.population_options["log_failed_systems_dir"],
                    "process_{}.txt".format(self.jobID()),
                )
                with self.open(
                    failed_systems_file, "a", encoding="utf-8"  # append
                ) as f:
                    now = datetime.datetime.now()
                    now = now.strftime("%d/%m/%Y %H:%M:%S\n")
                    if system_dict:
                        binary_c_cmdline_string = (
                            f"system {system_number} at {now} "
                            + self._return_argline(system_dict)
                            + "\n"
                        )
                        f.write(binary_c_cmdline_string)
                    if process:
                        self.vb_warning(
                            f"logged crashed process to {failed_systems_file}"
                        )
                        f.write(
                            f"Process {process} crashed at {now} with exit code {exitcode}."
                        )
        return

    def _check_binary_c_error(self, system_number, binary_c_output, system_dict):
        """
        Function to check whether binary_c throws an error and handle accordingly.
        """

        if binary_c_output:
            if (binary_c_output.splitlines()[0].startswith("SYSTEM_ERROR")) or (
                binary_c_output.splitlines()[-1].startswith("SYSTEM_ERROR")
            ):
                self.vb_warning(
                    "FAILING SYSTEM FOUND",
                )

                # Keep track of the amount of failed systems and their error codes
                self.population_options["_failed_prob"] += system_dict.get(
                    "probability", 1
                )
                self.population_options["_failed_count"] += 1
                self.population_options["_errors_found"] = True

                try:
                    error_code = int(
                        binary_c_output.splitlines()[0]
                        .split("with error code")[-1]
                        .split(":")[0]
                        .strip()
                    )
                    self.vb_warning(
                        f"Have error code {error_code}",
                    )
                except:
                    self.vb_warning(
                        "Failed to extract error code",
                    )
                    pass

                # Try catching the error code and keep track of the unique ones.
                try:
                    error_code = int(
                        binary_c_output.splitlines()[0]
                        .split("with error code")[-1]
                        .split(":")[0]
                        .strip()
                    )

                    if (
                        error_code
                        not in self.population_options["_failed_systems_error_codes"]
                    ):
                        self.vb_info(f"Caught errr code {error_code}")
                        self.population_options["_failed_systems_error_codes"].append(
                            error_code
                        )
                except ValueError:
                    error_code = None
                    self.vb_warning(
                        "Failed to extract the error-code",
                    )

                # log failing args?
                self._log_failure(system_dict=system_dict, system_number=system_number)

                # Check if we have exceeded the number of errors
                self.vb_info(
                    f"Check failed count {self.population_options['_failed_count']} vs max {self.population_options['failed_systems_threshold']}"
                )
                if (
                    self.population_options["_failed_count"]
                    > self.population_options["failed_systems_threshold"]
                ):

                    # stop evolving systems
                    self.population_options["stop_queue"]

                    # warn the user the first time we exceed failed_systems_threshold
                    if not self.population_options["_errors_exceeded"]:
                        self.vb_error(
                            "\n"
                            + self._boxed(
                                "Process {} exceeded the maximum ({}) number of failing systems. Stopped logging them to files now".format(
                                    self.process_ID,
                                    self.population_options["failed_systems_threshold"],
                                )
                            ),
                        )
                        self.population_options["_errors_exceeded"] = True

        else:
            self.vb_warning(
                "binary_c output nothing - this is strange. If there is ensemble output being generated then this is fine.",
            )
