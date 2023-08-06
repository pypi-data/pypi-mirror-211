"""
Module that contains the default options for the population grid code along with the description for these options, in the form of dictionaries:
    - population_options_defaults_dict: dictionary containing the default values for all the options
    - population_options_descriptions: dictionary containing the description for these options.

There are several other functions in this module, mostly to generate help texts or documents:
    - population_options_help: interactive function for the user to get descriptions for options
    - write_population_options_to_rst_file: function to generate the .rst document for the docs

With this its also possible to automatically generate a document containing all the setting names + descriptions.

All the options starting with _ should not be changed by the user except when you really know what you're doing (which is probably hacking the code :P)
"""

# pylint: disable=E1101

import copy
import os
import shutil
import sys
from typing import Callable

import astropy.units as u
import voluptuous as vol

from binarycpython.utils.custom_logging_functions import temp_dir
from binarycpython.utils.event_logging import (
    event_based_logging_output_parser,
    event_based_logging_parameter_list_dict,
)
from binarycpython.utils.functions import command_string_from_list, now

_MOE2017_VERBOSITY_LEVEL = 5
_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL = 6
_MOE2017_VERBOSITY_INTERPOLATOR_EXTRA_LEVEL = 7

secs_per_day = 86400  # probably needs to go somewhere more sensible
dimensionless_unit = u.m / u.m


def str_or_none_validation(value):
    if isinstance(value, str):
        pass
    elif value is None:
        pass
    else:
        raise ValueError("Input has to be str or None")


def callable_validation(value):
    if not isinstance(value, Callable):
        raise ValueError("Input has to be a callable")


def capsule_validation(value):
    t = type(value)
    return t.__module__ == "builtins" and t.__name__ == "PyCapsule"


def iterator_validation(value):
    try:
        iter(value)
    except:
        raise ValueError()


boolean_int_validation = vol.All(vol.Range(max=1), vol.Boolean())
float_or_int = vol.Or(float, int)


class population_options_defaults:
    """
    Class extension to Population grid containing all the functionality for the options and defaults
    """

    def __init__(self, **kwargs):
        """
        Init function for the population_options_defaults class
        """

        self.population_options_defaults_dict = {
            ##########################
            # general (or unordered..)
            ##########################
            "pre_evolve_function_hook": {
                "value": None,
                "description": "Function hook that gets used before the system is passed to binary_c. The function arguments should be (self, system_dict). If you return something from this function, the system_dict will be updated with that value.",
                "validation": callable_validation,
            },
            "using_result_queue": {
                "value": False,
                "description": "Flag to enable using the result_queue that passes the results of binary_c (or those of the user-defined parse_function). This is a temporary parameter",
                "validation": boolean_int_validation,
            },
            "num_cores": {
                "value": 1,
                "description": "The number of cores that the population grid will use. You can set this manually by entering an integer great than 0. When 0 uses all logical cores. When -1 uses all physical cores.",
                "validation": vol.Or(str, int, dict),
            },
            "_num_processes": {
                "value": 1,
                "description": "Number of processes launched by multiprocessing. This should be set automatically by binary_c-python, not by the user.",
                "validation": int,
            },
            "parse_function": {
                "value": None,
                "description": "Function that the user can provide to handle the output the binary_c. This function has to take the arguments (self, output). Its best not to return anything in this function, and just store stuff in the self.population_results dictionary, or just output results to a file",
                "validation": callable_validation,
            },
            "multiplicity_fraction_function": {
                "value": 0,
                "description": "Which multiplicity fraction function to use. 0: None, 1: Arenou 2010, 2: Rhagavan 2010, 3: Moe and di Stefano (2017) 2017",
                "validation": vol.Or(str, int),
            },
            "tmp_dir": {
                "value": temp_dir(),
                "description": "Directory where certain types of output are stored. The grid code is stored in that directory, as well as the custom logging libraries. Log files and other diagnostics will usually be written to this location, unless specified otherwise",
                "validation": str,
            },
            "cache_dir": {
                "value": self.default_cache_dir(),
                "description": "Directory where the chacheing files are stored.",
                "validation": str,
            },
            "status_dir": {
                "value": None,
                "description": "Directory where grid status is stored",
                "validation": str,
            },
            "_main_pid": {
                "value": -1,
                "description": "Main process ID of the master process. Used and set by the population object.",
                "validation": int,
            },
            "save_ensemble_chunks": {
                "value": True,
                "description": "Force the ensemble chunk to be saved even if we are joining a thread (just in case the joining fails)",
                "validation": boolean_int_validation,
            },
            "combine_ensemble_with_thread_joining": {
                "value": True,
                "description": "Boolean flag on whether to combine everything and return it to the user or if false: write it to data_dir/ensemble_output_{population_id}_{thread_id}.json",
                "validation": boolean_int_validation,
            },
            "_commandline_input": {
                "value": "",
                "description": "String containing the arguments passed to the population object via the command line. Set and used by the population object.",
                "validation": str,
            },
            "log_runtime_systems": {
                "value": False,
                "description": "Whether to log the runtime of the systems . Each systems run by the thread is logged to a file and is stored in the tmp_dir. (1 file per thread). Don't use this if you are planning to run a lot of systems. This is mostly for debugging and finding systems that take long to run. Integer, default = 0. if value is 1 then the systems are logged",
                "validation": boolean_int_validation,
            },
            "_actually_evolve_system": {
                "value": True,
                "description": "Whether to actually evolve the systems of just act as if. for testing. used in _process_run_population_grid",
                "validation": boolean_int_validation,
            },
            "max_queue_size": {
                "value": 1000,
                "description": "Maximum size of the queue that is used to feed the processes. Don't make this too big!",
                "validation": int,
            },
            "run_zero_probability_system": {
                "value": True,
                "description": "Whether to run the zero probability systems.",
                "validation": boolean_int_validation,
            },
            "_zero_prob_stars_skipped": {
                "value": 0,
                "description": "Internal counter to track how many systems are skipped because they have 0 probability",
                "validation": int,
            },
            "ensemble_factor_in_probability_weighted_mass": {
                "value": False,
                "description": "Flag to multiply all the ensemble results with 1/probability_weighted_mass",
                "validation": boolean_int_validation,
            },
            "do_dry_run": {
                "value": True,
                "description": "Whether to do a dry run to calculate the total probability for this run",
                "validation": boolean_int_validation,
            },
            "dry_run_num_cores": {
                "value": 1,
                "description": "number of parallel processes for the dry run (outer loop)",
                "validation": int,
            },
            "dry_run_hook": {
                "value": None,
                "description": "Function hook to be called for every system in a dry run. The function is passed a dict of the system parameters. Does nothing if None (the default).",
                "validation": callable_validation,
            },
            "return_after_dry_run": {
                "value": False,
                "description": "If True, return immediately after a dry run (and don't run actual stars). Default is False.",
                "validation": boolean_int_validation,
            },
            "exit_after_dry_run": {
                "value": False,
                "description": "If True, exits after a dry run. Default is False.",
                "validation": boolean_int_validation,
            },
            "print_stack_on_exit": {
                "value": False,
                "description": "If True, prints a stack trace when the population's exit method is called.",
                "validation": boolean_int_validation,
            },
            #####################
            # System information
            #####################
            "command_line": {
                "value": command_string_from_list(sys.argv),
                "description": "Place where the extra command line arguments are stored in.",
                "validation": str,
            },
            "original_command_line": {
                "value": os.getenv("BINARY_C_PYTHON_ORIGINAL_CMD_LINE"),
                "description": "The original command line command.",
                "validation": str,
            },
            "working_directory": {
                "value": os.getcwd(),
                "description": "Working directory of the script that invoked the population code.",
                "validation": str,
            },
            "original_working_directory": {
                "value": os.getenv("BINARY_C_PYTHON_ORIGINAL_WD"),
                "description": "Original working directory of the script that invoked the population code.",
                "validation": str,
            },
            "start_time": {
                "value": now(),
                "description": "Time the script that invoked the Population code started",
                "validation": str,
            },
            "original_submission_time": {
                "value": os.getenv("BINARY_C_PYTHON_ORIGINAL_SUBMISSION_TIME"),
                "description": "Sumission time of the script that invoked the Population code.",
                "validation": str,
            },
            ##########################
            # Execution log:
            ##########################
            "verbosity": {
                "value": 1,
                "description": "Verbosity of the population code. Default is 1, by which only errors will be handled by the logging object. Higher values will show more output. The verbosity levels correspond to the following logging levels: 0: CRITICAL, 1: ERROR, 2: WARNING, 3: INFO, 4: DEBUG",
                "validation": int,
            },
            "log_file": {
                "value": os.path.join(temp_dir(), "population.log"),
                "description": "Log file for the population object.",
                "validation": str,
            },
            "log_config_file": {
                "value": None,
                "description": "Configuration file file the logging module.",
                "validation": str_or_none_validation,
            },
            "log_dt": {
                "value": 5,
                "description": "Time between verbose logging output.",
                "validation": vol.Or(float, int),
            },
            "n_logging_stats": {
                "value": 50,
                "description": "Number of logging statistics used to calculate time remaining (etc.). E.g., if you set this to 10 the previous 10 calls to the verbose log will be used to construct an estimate of the time remaining.",
                "validation": int,
            },
            "log_newline": {
                "value": "\n",
                "description": "Newline character used at the end of verbose logging statements. This is \\n (newline) by default, but \\x0d (carriage return) might also be what you want.",
                "validation": str,
            },
            ##########################
            # binary_c files
            ##########################
            "_binary_c_executable": {
                "value": os.path.join(os.environ["BINARY_C"], "binary_c"),
                "description": "Full path to the binary_c executable. This options is not used in the population object.",
                "validation": str,
            },
            "_binary_c_shared_library": {
                "value": os.path.join(os.environ["BINARY_C"], "src", "libbinary_c.so"),
                "description": "Full path to the libbinary_c file. This options is not used in the population object",
                "validation": str,
            },
            "_binary_c_config_executable": {
                "value": os.path.join(os.environ["BINARY_C"], "binary_c-config"),
                "description": "Full path of the binary_c-config executable. This options is not used in the population object.",
                "validation": str,
            },
            "_binary_c_dir": {
                "value": os.environ["BINARY_C"],
                "description": "Directory where binary_c is stored. This options are not really used",
                "validation": str,
            },
            ##########################
            # Moe and di Stefano (2017) distributions (internal) settings
            ##########################
            "_loaded_Moe2017_data": {
                "value": False,
                "description": "Internal variable storing whether the Moe and di Stefano (2017) data has been loaded into memory",
                "validation": boolean_int_validation,
            },
            "_set_Moe2017_grid": {
                "value": False,
                "description": "Internal flag whether the Moe and di Stefano (2017) grid has been loaded",
                "validation": boolean_int_validation,
            },
            "Moe2017_options": {
                "value": None,  # Holds the Moe and di Stefano (2017) options.
                "description": "Set of options for the Moe & diStefano initial distribution interpolation table functionality",
                "validation": dict,
            },
            "_Moe2017_JSON_data": {
                "value": None,
                "description": "Parameter to store the loaded Moe&diStefano2017 dataset",  # Stores the data
                "validation": dict,
            },
            ##########################
            # Custom logging
            ##########################
            "C_auto_logging": {
                "value": None,
                "description": "Dictionary containing parameters to be logged by binary_c. The structure of this dictionary is as follows: the key is used as the headline which the user can then catch. The value at that key is a list of binary_c system parameters (like star[0].mass)",
                "validation": dict,
            },
            "C_logging_code": {
                "value": None,
                "description": "Variable to store the exact code that is used for the custom_logging. In this way the user can do more complex logging, as well as putting these logging strings in files.",
                "validation": str,
            },
            "custom_logging_func_memaddr": {
                "value": -1,
                "description": "Memory address where the custom_logging_function is stored.",
                "validation": vol.Or(int, capsule_validation),
            },
            "_custom_logging_shared_library_file": {
                "value": None,
                "description": "filename for the custom_logging shared library. Used and set by the population object",
                "validation": str,
            },
            ##########################
            # Store pre-loading:
            ##########################
            "_store_memaddr": {
                "value": -1,
                "description": "Memory address of the store object for binary_c.",
                "validation": vol.Or(int, capsule_validation),
            },
            ##########################
            # Log args: logging of arguments
            ##########################
            "log_args": {
                "value": 0,
                "description": "Boolean to log the arguments.",
                "validation": boolean_int_validation,
            },
            "log_args_dir": {
                "value": temp_dir("log_args"),
                "description": "Directory to log the arguments to.",
                "validation": str,
            },
            ##########################
            # Population evolution
            ##########################
            "evolution_type": {
                "value": "grid",
                "description": "Variable containing the type of evolution used of the grid. Multiprocessing, linear processing or possibly something else (e.g. for Slurm or Condor).",
                "validation": vol.All(
                    str,
                    vol.In(["grid", "monte_carlo", "custom_generator", "source_file"]),
                ),
            },
            "_evolution_type_options": {  # TODO: perhaps deprecate this since we use a better validation
                "value": [
                    "grid",
                    "custom_generator",
                    "source_file",
                    "monte_carlo",
                ],
                "description": "List containing the evolution type options.",
                "validation": list,
            },
            "_system_generator": {
                "value": None,
                "description": "Function object that contains the system generator function. This can be from a grid, or a source file, or a Monte Carlo grid.",
                "validation": iterator_validation,
            },
            "_count": {
                "value": 0,
                "description": "Counter tracking which system the generator is on.",
                "validation": int,
            },
            "_total_starcount": {
                "value": 0,
                "description": "Variable storing the total number of systems in the generator. Used and set by the population object.",
                "validation": int,
            },
            "_probtot": {
                "value": 0,
                "description": "Total probability of the population.",
                "validation": float,
            },
            "weight": {
                "value": 1.0,
                "description": "Weight factor for each system. The calculated probability is multiplied by this. If the user wants each system to be repeated several times, then this variable should not be changed, rather change the _repeat variable instead, as that handles the reduction in probability per system. This is useful for systems that have a process with some random element in it.",  # TODO: add more info here, regarding the evolution splitting.
                "validation": float,
            },
            "repeat": {
                "value": 1,
                "description": "Factor of how many times a system should be repeated. Consider the evolution splitting binary_c argument for supernovae kick repeating.",
                "validation": int,
            },
            "_start_time_evolution": {
                "value": 0,
                "description": "Variable storing the start timestamp of the population evolution. Set by the object itself.",
                "validation": vol.All(float, int),
            },
            "_end_time_evolution": {
                "value": 0,
                "description": "Variable storing the end timestamp of the population evolution. Set by the object itself",
                "validation": vol.All(float, int),
            },
            "_errors_found": {
                "value": False,
                "description": "Variable storing a Boolean flag whether errors by binary_c are encountered.",
                "validation": boolean_int_validation,
            },
            "_errors_exceeded": {
                "value": False,
                "description": "Variable storing a Boolean flag whether the number of errors was higher than the set threshold (failed_systems_threshold). If True, then the command line arguments of the failing systems will not be stored in the failed_system_log files.",
                "validation": boolean_int_validation,
            },
            "_failed_count": {
                "value": 0,
                "description": "Variable storing the number of failed systems.",
                "validation": int,
            },
            "_failed_prob": {
                "value": 0,
                "description": "Variable storing the total probability of all the failed systems",
                "validation": float,
            },
            "failed_systems_threshold": {
                "value": 20,
                "description": "Variable storing the maximum number of systems that are allowed to fail before logging their command line arguments to failed_systems log files",
                "validation": int,
            },
            "_failed_systems_error_codes": {
                "value": [],
                "description": "List storing the unique error codes raised by binary_c of the failed systems",
                "validation": list,
            },
            "log_failed_systems": {
                "value": False,  # Flag to enable logging of failed systems
                "description": "Flag to enable logging of failed systems",
                "validation": boolean_int_validation,
            },
            "log_failed_systems_dir": {
                "value": temp_dir(
                    "failed_systems"
                ),  # directory the failed system are logged to
                "description": "Directory the failed system information is logged to",
                "validation": str,
            },
            "_population_id": {
                "value": 0,
                "description": "Unique 32-char hex string ID of the population",
                "validation": str,
            },
            "_total_mass_run": {
                "value": 0,
                "description": "To count the total mass that thread/process has ran",
                "validation": float_or_int,
            },
            "_total_probability_weighted_mass_run": {
                "value": 0,
                "description": "To count the total mass * probability for each system that thread/process has ran",
                "validation": float_or_int,
            },
            "modulo": {
                "value": 1,
                "description": "the modulus of the population evolution. This is used if a population is evolved through several different machines.",
                "validation": int,
            },
            "start_at": {
                "value": 0,
                "description": "The first system (number) that is allowed to run.",
                "validation": int,
            },
            "skip_before": {
                "value": 0,
                "description": "The system number before which the systems are skipped.",
                "validation": int,
            },
            "_sampling_variables": {
                "value": {},
                "description": "Dictionary storing the sampling_variables. These contain properties which are accessed by the _generate_grid_code function",
                "validation": dict,
            },
            "gridcode_filename": {
                "value": None,
                "description": "Filename for the grid code. Set and used by the population object. TODO: allow the user to provide their own function, rather than only a generated function.",
                "validation": str,
            },
            "symlink_latest_gridcode": {
                "value": True,
                "description": "Symlink to latest gridcode.",
                "validation": str,
            },
            "save_population_object": {
                "value": None,
                "description": "filename to which we should save a pickled grid object as the final thing we do.",
                "validation": str,
            },
            "joinlist": {
                "value": None,
                "description": "Files that are to be joined by the HPC.",
                "validation": list,
            },
            "do_analytics": {
                "value": True,
                "description": "Flag whether to calculate some details about the performance of the population evolution.",
                "validation": boolean_int_validation,
            },
            "save_snapshots": {
                "value": False,
                "description": "Flag whether to save snapshots of the population when terminated by a SIGINT.",
                "validation": boolean_int_validation,
            },
            "save_snapshot": {
                "value": False,
                "description": "TODO: not sure what the difference is with save_snapshots",
                "validation": boolean_int_validation,
            },
            "restore_from_snapshot_file": {
                "value": None,
                "description": "File of the snapshot to restore the population from.",
                "validation": str,
            },
            "restore_from_snapshot_dir": {
                "value": None,
                "description": "Directory that contains the snapshots.",
                "validation": str,
            },
            "exit_code": {
                "value": 0,
                "description": "exit code of the population.",
                "validation": int,
            },
            "stop_queue": {
                "value": False,
                "description": "Flag whether to stop the queue.",
                "validation": boolean_int_validation,
            },
            "_killed": {
                "value": False,
                "description": "parameter that stores whether the evolution was killed.",
                "validation": boolean_int_validation,
            },
            "_queue_done": {
                "value": False,
                "description": "parameter that stores whether the queue is finished.",
                "validation": boolean_int_validation,
            },
            ########################################
            # Monte-Carlo sampling options
            ########################################
            "monte_carlo_count_threshold": {
                "value": -1,
                "description": "Monte-Carlo system count threshold.",
                "validation": int,
            },
            "_monte_carlo_current_total_count_evolved": {
                "value": 0,
                "description": "total number of systems evolved up until now",
                "validation": int,
            },
            "monte_carlo_mass_threshold": {
                "value": -1,
                "description": "Monte-Carlo mass threshold.",
                "validation": float_or_int,
            },
            "_monte_carlo_current_total_mass_evolved": {
                "value": 0,
                "description": "total mass evolved up until now",
                "validation": float_or_int,
            },
            "monte_carlo_custom_threshold_function": {
                "value": None,
                "description": "Custom threshold function for the monte-carlo sampling. This function needs to accept the arguments (self, result_queue)",
                "validation": callable_validation,  # TODO: perhaps we should also analyse the args available in this function.
            },
            "_monte_carlo_threshold_reached": {
                "value": False,
                "description": "Flag whether the threshold has been reached",
                "validation": boolean_int_validation,
            },
            "_monte_carlo_generator_filename": {
                "value": None,
                "description": "System generator filename",
                "validation": str,
            },
            "monte_carlo_use_pre_calculated_distributions": {
                "value": True,
                "description": "Flag whether to pre-calculate the value arrays and pdf/cdf arrays and use those as interpolation tables during the sampling. This takes into account the dependency on other variables for each sampling variable.",
                "validation": boolean_int_validation,
            },
            ########################################
            # Source file sampling options
            ########################################
            "source_file_sampling_filename": {
                "value": None,
                "description": "Variable containing the source file containing lines of binary_c command line calls. These all have to start with binary_c.",
                "validation": str,
            },
            "source_file_sampling_type": {
                "value": "commands",
                "description": "Type of formatting of the source-file sampling file contents. Allowed options: 'commands': formatted like the commandline command for binary_c, i.e. <key> <value> etc. 'column': column-based formatting. The first line of the file should contain the keys. The rest of the lines should contain the values in the correct columns.",
                "validation": str,
            },
            "_source_file_filehandle": {
                "value": None,
                "description": "Filehandle for the source file.",
                "validation": str,
            },
            ########################################
            # Custom generator sampling options
            ########################################
            "custom_generator": {
                "value": None,  # Place for the custom system generator
                "description": "Custom system generator. The user can provide a custom system generator that generates the systems that will be evolved. This has to be of an iterable type, like list or generator.",
                "validation": iterator_validation,
            },
            ########################################
            # function caching options
            ########################################
            "function_cache": {
                "value": True,
                "description": "If True, we use a cache for certain function calls.",
                "validation": boolean_int_validation,
            },
            "function_cache_default_maxsize": {
                "value": 256,
                "description": "The default maxsize of the cache. Should be a power of 2.",
                "validation": int,
            },
            "function_cache_default_type": {
                "value": "NullCache",
                "description": "One of the following types: LRUCache, LFUCache, FIFOCache, MRUCache, RRCache, TTLCache, NullCache, NoCache. You can find details of what these mean in the Python cachetools manual, except fo NoCache which means no cache is used at all, and NullCache is a dummy cache that never matches, used for testing overheads.",
                "validation": str,
            },
            "function_cache_TTL": {
                "value": 30,
                "description": "Time-to-live for the cacheing",
                "validation": float_or_int,
            },
            "function_cache_functions": {
                "value": {
                    # key=function_name : value=(cache_size, cache_type, test_args (string))
                    #
                    # if cache_size is 0, use function_cache_default_maxsize
                    # set above
                    #
                    # if cache_type is None, use function_cache_default_type
                    # set above
                    #
                    # if n is None, no cache is set up
                    "distribution_functions.powerlaw_constant": (
                        0,
                        "NoCache",
                        "1,100,-2",
                    ),
                    "distribution_functions.calculate_constants_three_part_powerlaw": (
                        16,
                        "FIFOCache",
                        "0.1,0.5,1,100,-1.3,-2.3,-2.3",
                    ),
                    "distribution_functions.gaussian_normalizing_const": (
                        16,
                        "FIFOCache",
                        "1.0,1.0,-10.0,+10.0",
                    ),
                    "spacing_functions.const_linear": (16, "FIFOCache", "1,10,9"),
                    "spacing_functions.const_int": (0, None, "1,10,9"),
                    "spacing_functions.const_ranges": (
                        16,
                        "FIFOCache",
                        "((0.1,0.65,10),(0.65,0.85,20),(0.85,10.0,10))",
                    ),
                    "spacing_functions.gaussian_zoom": (
                        16,
                        "FIFOCache",
                        "1.0,10.0,5.0,2.0,0.9,100",
                    ),
                },
                "description": "Functions that are included int he function-caching, including a configuration for the caching.",
                "validation": dict,
            },
            ########################################
            # HPC variables
            ########################################
            "HPC_force_join": {
                "value": 0,
                "description": 'Flag to enforce the joining of the results and skip checking our own job. Only used when HPC variable ("slurm" or "condor") is 3.',
                "validation": boolean_int_validation,
            },
            "HPC_rebuild_joinlist": {
                "value": 0,
                "description": "Flag to ignore the joinlist we would usually use and rebuild it automatically",
                "validation": boolean_int_validation,
            },
            ########################################
            # Slurm stuff
            ########################################
            "slurm": {
                "value": 0,
                "description": "Flag used to control Slurm jobs. Default is 0 which means no Slurm. 1 means launch Slurm jobs. Do not manually set this to 2 (run Slurm jobs) or 3 (join Slurm job data) unless you know what you are doing, this is usually done for you.",
                "validation": boolean_int_validation,
            },
            "slurm_ntasks": {
                "value": 1,
                "description": "Number of CPUs required per array job: usually only need this to be 1 (the default).",
                "validation": int,
            },
            "slurm_dir": {
                "value": "",
                "description": "Working directory containing e.g. scripts, output, logs (e.g. should be NFS available to all jobs). This directory should not exist when you launch the Slurm jobs.",
                "validation": str,
            },
            "slurm_jobid": {
                "value": "",
                "description": "Slurm job id. Each job is numbered <slurm_jobid>.<slurm_jobarrayindex>.",
                # TODO: write validation
            },
            "slurm_memory": {
                "value": "512MB",
                "description": 'Memory required for the job. Should be in megabytes in a format that Slurm understands, e.g. "512MB" (the default).',
                "validation": str,
            },
            "slurm_warn_max_memory": {
                "value": "1024MB",
                "description": 'If we set slurm_memory in excess of this, warn the user because this is usually a mistake. Default "1024MB".',
                "validation": str,
            },
            "slurm_postpone_join": {
                "value": 0,
                "description": "Flag to postpone the join of the job results. If activated then you have to do it later manually.",
                "validation": boolean_int_validation,
            },
            "slurm_jobarrayindex": {
                "value": None,
                "description": "Slurm job array index. Each job is numbered <slurm_jobid>.<slurm_jobarrayindex>.",
                # TODO: write validation
            },
            "slurm_jobname": {
                "value": "binary_c-python",
                "description": 'base names of the Slurm jobs, default "binary_c-python".',
                "validation": str,
            },
            "slurm_partition": {
                "value": None,
                "description": "Slurm partition name. You should check your local Slurm installation to find out partition information, e.g. using the sview command.",
                "validation": str,
            },
            "slurm_time": {
                "value": "0",
                "description": "The time a Slurm job is allowed to take. Default is 0 which means no limit. Please check the Slurm documentation for required format of this option.",
                "validation": float_or_int,
            },
            "slurm_postpone_sbatch": {
                "value": 0,
                "description": "Flag to postpone launching the slurm jobs with sbatch. Just make the scripts that would have.",
                "validation": boolean_int_validation,
            },
            "slurm_array": {
                "value": None,
                "description": "Override for Slurm's --array option, useful for rerunning jobs manually.",
                # TODO: write validation
            },
            "slurm_array_max_jobs": {
                "value": None,
                "description": "Override for the max number of concurrent Slurm array jobs.",
                "validation": int,
            },
            "slurm_extra_settings": {
                "value": {},
                "description": "Dictionary of extra settings for Slurm to put in its launch script. Please see the Slurm documentation for the many options that are available to you.",
                "validation": dict,
            },
            "slurm_sbatch": {
                "value": shutil.which("sbatch"),
                "description": 'The Slurm "sbatch" submission command, usually "/usr/bin/sbatch" but will depend on your Slurm installation. By default is set automatically.',
                "validation": str,
            },
            "slurm_env": {
                "value": shutil.which("env"),
                "description": 'Points the location of the "env" command, e.g. /usr/bin/env or /bin/env, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            "slurm_bash": {
                "value": shutil.which("bash"),
                "description": 'Points the location of the "bash" command, e.g. /bin/bash, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            "slurm_pwd": {
                "value": shutil.which("pwd"),
                "description": 'Points the location of the "pwd" command, e.g. /bin/pwd, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            "slurm_date": {
                "value": shutil.which("date"),
                "description": 'Points the location of the "date" command, e.g. /usr/bin/date, that is used in Slurm scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            ########################################
            # Condor stuff
            ########################################
            "condor": {
                "value": 0,
                "description": "Flag to enable running HTCondor (referred to as Condor here) jobs. Default is 0 which means no Condor. 1 means launch Condor jobs. Do not manually set this to 2 (run Condor jobs) or 3 (join Condor job data) unless you know what you are doing, this is usually done for you.",
                "validation": boolean_int_validation,
            },
            "condor_dir": {
                "value": "",
                "description": "Working directory containing e.g. scripts, output, logs (e.g. should be NFS available to all jobs). This directory should not exist when you launch the Condor jobs.",
                "validation": str,
            },
            "condor_njobs": {
                "value": 0,
                "description": "Number of jobs that Condor will run",
                "validation": int,
            },
            "condor_ClusterID": {
                "value": None,
                "description": "Condor ClusterID variable, equivalent to Slurm's jobid. Jobs are numbered <ClusterID>.<Process>",
            },
            "condor_Process": {
                "value": None,
                "description": "Condor Process variable, equivalent to Slurm's jobarrayindex. Jobs are numbered <ClusterID>.<Process>",
            },
            "condor_postpone_submit": {
                "value": 0,
                "description": "Debugging tool. If 1, the condor script is not submitted (useful for debugging). Default 0.",
                "validation": boolean_int_validation,
            },
            "condor_postpone_join": {
                "value": 0,
                "description": "Use to delay the joining of Condor grid data. If 1, data is not joined, e.g. if you want to do it off the condor grid (e.g. with more RAM). Default 0.",
                "validation": boolean_int_validation,
            },
            "condor_memory": {
                "value": 512,
                "description": "In MB, the memory use (ImageSize) of the job.",
                "validation": float_or_int,
            },
            "condor_warn_max_memory": {
                "value": 1024,
                "description": "In MB, the memory use (ImageSize) of the job.",
                "validation": float_or_int,
            },
            "condor_universe": {
                "value": "vanilla",
                "description": 'The HTCondor "universe": this is "vanilla" by default.',
                "validation": str,
            },
            "condor_extra_settings": {
                "value": {},
                "description": "Place to put extra configuration for the CONDOR submit file. The key and value of the dict will become the key and value of the line in te slurm batch file. Will be put in after all the other settings (and before the command). Take care not to overwrite something without really meaning to do so.",
                "validation": dict,
            },
            "condor_snapshot_on_kill": {
                "value": 0,
                "description": "If 1 we save a snapshot on SIGKILL before exit.",
                "validation": boolean_int_validation,
            },
            "condor_stream_output": {
                "value": True,
                "description": "Flag to activate Condor's stdout stream. If False, this data is copied at the end of the job.",
                "validation": boolean_int_validation,
            },
            "condor_stream_error": {
                "value": True,
                "description": "Flag to activate Condor's stderr stream. If False, this data is copied at the end of the job.",
                "validation": boolean_int_validation,
            },
            "condor_should_transfer_files": {
                "value": "YES",
                "description": 'Condor\'s option to transfer files at the end of the job. You should set this to "YES"',
                "validation": str,
            },
            "condor_when_to_transfer_output": {
                "value": "ON_EXIT_OR_EVICT",
                "description": 'Condor\'s option to decide when output files are transferred. You should usually set this to "ON_EXIT_OR_EVICT"',
                "validation": str,
            },
            "condor_requirements": {
                "value": "",
                "description": "Condor job requirements. These are passed to Condor directly, you should read the HTCondor manual to learn about this. If no requirements exist, leave as an string.",
                "validation": str,
            },
            "condor_env": {
                "value": shutil.which("env"),
                "description": 'Points the location of the "env" command, e.g. /usr/bin/env or /bin/env, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            "condor_bash": {
                "value": shutil.which("bash"),
                "description": 'Points the location of the "bash" command, e.g. /bin/bash, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            "condor_pwd": {
                "value": shutil.which("pwd"),
                "description": 'Points the location of the "pwd" command, e.g. /bin/pwd, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            "condor_date": {
                "value": shutil.which("date"),
                "description": 'Points the location of the "date" command, e.g. /usr/bin/date, that is used in Condor launch scripts. This is set automatically on the submit machine, so if it is different on the nodes, you should set it manually.',
                "validation": str,
            },
            "condor_initial_dir": {
                "value": None,
                "description": "Directory from which condor scripts are run. If set to the default, None, this is the directory from which your script is run.",
                "validation": str,
            },
            "condor_submit": {
                "value": shutil.which("condor_submit"),
                "description": 'The Condor_submit command, usually "/usr/bin/condor_submit" but will depend on your HTCondor installation.',
                "validation": str,
            },
            "condor_q": {
                "value": shutil.which("condor_q"),
                "description": 'The Condor_q command, usually "/usr/bin/condor_q" but will depend on your HTCondor installation.',
                "validation": str,
            },
            "condor_getenv": {
                "value": True,
                "description": "Flag to copy and use the environment at submission. You almost certainly want this to be True.",
                "validation": boolean_int_validation,
            },
            "condor_batchname": {
                "value": "binary_c-condor",
                "description": "Condor batchname option: this is what appears in condor_q.",
                "validation": str,
            },
            "condor_kill_sig": {
                "value": "SIGINT",
                "description": 'Signal Condor should use to stop a process. Note that grid.py expects this to be "SIGINT" which is the default.',
                "validation": str,
            },
            #########################
            # Event based logging
            #########################
            "event_based_logging_handle_output": {
                "value": False,
                "description": "Flag to enable the processing of the event-based logging output from binary_c.",
                "validation": boolean_int_validation,
            },
            "event_based_logging_output_directory": {
                "value": None,
                "description": "Path to output directory for the event logs",
                "validation": str,
            },
            "event_based_logging_combine_individual_event_files": {
                "value": False,
                "description": 'Flag to enable enable combining the process-specific event output files into a single file. See "event_based_logging_combined_events_filename"',
                "validation": boolean_int_validation,
            },
            "event_based_logging_combined_events_filename": {
                "value": "all_events.dat",
                "description": 'Filename for the combined events file. See "event_based_logging_combine_individual_event_files"',
                "validation": str,
            },
            "event_based_logging_remove_individual_event_files_after_combining": {
                "value": False,
                "description": "Flag to enable the removal of the process-specific event files after combining into one file",
                "validation": boolean_int_validation,
            },
            "event_based_logging_split_events_file_to_each_type": {
                "value": False,
                "description": 'Flag to enable splitting the combined event file into event-specific files like RLOF_events, SN_events etc. See "event_based_logging_combine_individual_event_files"',
                "validation": boolean_int_validation,
            },
            "event_based_logging_remove_original_combined_events_file_after_splitting": {
                "value": False,
                "description": 'Flag to enable the removal of the combined events file after splitting into event-specific files. See "event_based_logging_split_events_file_to_each_type"',
                "validation": boolean_int_validation,
            },
            "event_based_logging_output_separator": {
                "value": "\t",
                "description": "Separator used during the processing of the event output",
                "validation": str,
            },
            "event_based_logging_output_parser": {
                "value": event_based_logging_output_parser,
                "description": "Function that handles the processing of the event-based logging output. Note: this function needs to have the following arguments: self, events_parameters_list_dict, data_dir, output, separator.",
                "validation": callable_validation,
            },
            "event_based_logging_parameter_list_dict": {
                "value": event_based_logging_parameter_list_dict,
                "description": 'Dictionary that contains the lists of parameters per event type. Looks like {"<event type>": [<event parameter list>}.',
                "validation": dict,
            },
            #########################
            # email notification
            #########################
            "email_notifications_enabled": {
                "value": False,
                "description": "Flag to enable or disable email notifications about the outcome of the population evolution. This currently only works for gmail, and on an account that has the application specific password authentication enabled. See https://support.google.com/accounts/answer/185833?hl=en",
                "validation": boolean_int_validation,
            },
            "email_notifications_APP_password": {
                "value": os.getenv("BCP_EMAIL_NOTIFICATION_APP_PW", ""),
                "description": 'app password for the email notifications. On default the content of the "BCP_EMAIL_NOTIFICATION_APP_PW" environment variable is used.',
                "validation": str,
            },
            "email_notifications_recipients": {
                "value": [],
                "description": "List of recipients for the email notifications. The email will also be sent to the corresponding email, regardless of the recipients.",
                "validation": [str],
            },
            "email_notifications_corresponding_email": {
                "value": "",
                "description": 'Corresponding email address for the email notifications. Note that this has to be a gmail-based account with app-password authentication enabled. The content of "email_notifications_APP_password" will be used to authenticate.',
                "validation": str,
            },
            "email_notification_extra_info_function_hook": {
                "value": None,
                "description": "Function hook to allow extra information to be sent with the emails. This function currently can only accept the `population_object` parameter, which gives the user access to the population object that sends the email. This function should return a string that contains the additional information.",
                "validation": callable_validation,
            },
        }

    def set_validation_schema(self):
        """
        Function to set the validation schema of the population_options
        """

        # from the main dictionary, create a validation scheme
        validation_dict = {
            key: value["validation"]
            for key, value in self.population_options_defaults_dict.items()
            if "validation" in value
        }
        self.validation_schema = vol.Schema(validation_dict, extra=vol.ALLOW_EXTRA)

    def set_default_population_options(self):
        """
        Function to load the population_options with the default values
        """

        # Grid options
        self.population_options = {
            key: value["value"]
            for key, value in self.population_options_defaults_dict.items()
        }

    def population_options_help(self, option: str) -> dict:
        """
        Function that prints out the description of a grid option. Useful function for the user.

        Args:
            option: which option you want to have the description of.

        returns:
            dict containing the option, the description if its there, otherwise empty string. And if the key doesnt exist, the dict is empty
        """

        # construct descriptions dict
        descriptions_dict = {
            key: value["description"]
            for key, value in self.population_options_defaults_dict.items()
        }
        descriptions_keys = descriptions_dict.keys()

        # If the option is unknown
        if option not in descriptions_keys:
            print(
                "Error: This is an invalid entry. Option does not exist, please choose from the following options:\n\t{}".format(
                    ", ".join(sorted(descriptions_keys))
                )
            )
            return {}

        # If its known and described:
        print(descriptions_dict[option])

        return {option: descriptions_dict[option]}

    def build_description_table(self, table_name, parameter_list, description_dict):
        """
        Function to create a table containing the description of the options
        """

        #
        indent = "   "

        # Get parameter list and parse descriptions
        parameter_list_with_descriptions = [
            [
                parameter,
                self.parse_description(description_dict=description_dict[parameter]),
            ]
            for parameter in parameter_list
        ]

        # Construct parameter list
        rst_table = """
.. list-table:: {}
{}:widths: 25, 75
{}:header-rows: 1
""".format(
            table_name, indent, indent
        )

        #
        rst_table += "\n"
        rst_table += indent + "* - Option\n"
        rst_table += indent + "  - Description\n"

        for parameter_el in parameter_list_with_descriptions:
            rst_table += indent + "* - {}\n".format(parameter_el[0])
            rst_table += indent + "  - {}\n".format(parameter_el[1])

        return rst_table

    def parse_description(self, description_dict):
        """
        Function to parse the description for a given parameter
        """

        # Make a local copy
        description_dict = copy.copy(description_dict)

        ############
        # Add description
        description_string = "Description:\n   "

        # Clean description text
        description_text = description_dict["description"].strip()
        description_text = description_text[0].capitalize() + description_text[1:]
        if description_text[-1] != ".":
            description_text = description_text + "."
        description_string += description_text

        ##############
        # Add unit (in latex)
        if "unit" in description_dict:
            if description_dict["unit"] != dimensionless_unit:
                description_string = description_string + "\n\nUnit: [{}].".format(
                    description_dict["unit"].to_string("latex_inline")
                )

        ##############
        # Add default value
        if "value" in description_dict:
            # Clean
            if isinstance(description_dict["value"], str) and (
                "/home" in description_dict["value"]
            ):
                description_dict["value"] = "example path"

            # Write
            description_string = (
                description_string
                + "\n\nDefault value:\n   {}".format(description_dict["value"])
            )

        ##############
        # Add validation
        if "validation" in description_dict:
            # Write
            description_string = description_string + "\n\nValidation:\n   {}".format(
                description_dict["validation"]
            )

        # Check if there are newlines, and replace them by newlines with indent
        description_string = description_string.replace("\n", "\n       ")

        return description_string

    def write_population_options_to_rst_file(self, output_file: str) -> None:
        """
        Function that writes the descriptions of the grid options to an rst file

        Args:
            output_file: target file where the grid options descriptions are written to
        """

        ###############
        # Check input
        if not output_file.endswith(".rst"):
            msg = "Filename doesn't end with .rst, please provide a proper filename"
            raise ValueError(msg)

        ###############
        # construct descriptions dict
        descriptions_dict = {}
        for key, value in self.population_options_defaults_dict.items():
            descriptions_dict[key] = {}
            descriptions_dict[key]["description"] = value["description"]
            descriptions_dict[key]["value"] = value["value"]

            if "validation" in value:
                descriptions_dict[key]["validation"] = value["validation"]

        # separate public and private options
        public_options = [key for key in descriptions_dict if not key.startswith("_")]
        private_options = [key for key in descriptions_dict if key.startswith("_")]

        # M&S options
        moe_di_stefano_default_options_descriptions_dict = {
            key: {"description": value["description"], "value": value["value"]}
            for key, value in self.moe_distefano_options_defaults_dict.items()
        }
        moe_di_stefano_default_options = list(
            moe_di_stefano_default_options_descriptions_dict.keys()
        )

        ###############
        # Build description page text

        # Set up intro
        description_page_text = ""
        title = "Population options"
        description_page_text += title + "\n"
        description_page_text += "=" * len(title) + "\n\n"
        description_page_text += "The following chapter contains all Population code options, along with their descriptions."
        description_page_text += "\n\n"

        # Set up description table for the public options
        public_options_description_title = "Public options"
        public_options_description_text = public_options_description_title + "\n"
        public_options_description_text += (
            "-" * len(public_options_description_title) + "\n\n"
        )
        public_options_description_text += "In this section we list the public options for the population code. These are meant to be changed by the user.\n"
        public_options_description_text += self.build_description_table(
            table_name="Public options",
            parameter_list=sorted(public_options),
            description_dict=descriptions_dict,
        )
        description_page_text += public_options_description_text
        description_page_text += "\n\n"

        # Set up description table for the M&S options
        MS_options_description_title = (
            "Moe&diStefano distribution interpolation options"
        )
        MS_options_description_text = MS_options_description_title + "\n"
        MS_options_description_text += "-" * len(MS_options_description_title) + "\n\n"
        MS_options_description_text += "In this section we list the options that are available for the Moe&diStefano distribution interpolation. These are meant to be changed by the user.\n"
        MS_options_description_text += self.build_description_table(
            table_name="Public options",
            parameter_list=sorted(moe_di_stefano_default_options),
            description_dict=moe_di_stefano_default_options_descriptions_dict,
        )
        description_page_text += MS_options_description_text
        description_page_text += "\n\n"

        # Set up description table for the private options
        private_options_description_title = "Private internal variables"
        private_options_description_text = private_options_description_title + "\n"
        private_options_description_text += (
            "-" * len(private_options_description_title) + "\n\n"
        )
        private_options_description_text += "In this section we list the private internal parameters for the population code. These are not meant to be changed by the user.\n"
        private_options_description_text += self.build_description_table(
            table_name="Private internal variables",
            parameter_list=sorted(private_options),
            description_dict=descriptions_dict,
        )
        description_page_text += private_options_description_text
        description_page_text += "\n\n"

        ###############
        # write to file
        with self.open(output_file, "w") as f:
            f.write(description_page_text)
