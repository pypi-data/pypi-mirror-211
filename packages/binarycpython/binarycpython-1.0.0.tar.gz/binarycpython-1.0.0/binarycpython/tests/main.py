# /usr/bin/env python
"""
Main file for the tests. This file imports all the unit test functions from all modules except for the notebooks and for the HPC functions
"""

# pylint: disable=W0611

import unittest

from binarycpython.tests.test_c_bindings import (
    test_ensemble_functions,
    test_return_store_memaddr,
    test_run_system,
)
from binarycpython.tests.test_custom_logging import (
    test_autogen_C_logging_code,
    test_binary_c_log_code,
    test_binary_c_write_code,
    test_create_and_load_logging_function,
    test_from_binary_c_config,
    test_return_compilation_dict,
)
from binarycpython.tests.test_dicts import (
    test__nested_get,
    test_AutoVivicationDict,
    test_count_keys_recursive,
    test_custom_sort_dict,
    test_filter_dict,
    test_filter_dict_through_values,
    test_inspect_dict,
    test_keys_to_floats,
    test_merge_dicts,
    test_multiply_float_values,
    test_multiply_values_dict,
    test_normalize_dict,
    test_prepare_dict,
    test_recursive_change_key_to_float,
    test_recursive_change_key_to_string,
    test_setopts,
    test_subtract_dicts,
    test_update_dicts,
)
from binarycpython.tests.test_ensemble import (
    test_binaryc_json_serializer,
    test_BinarycDecoder,
    test_BinarycEncoder,
    test_ensemble_file_type,
    test_extract_ensemble_json_from_string,
    test_handle_ensemble_string_to_json,
    test_load_ensemble,
    test_open_ensemble,
)
from binarycpython.tests.test_event_logging import (
    test_event_file_processing,
    test_event_parameter_descriptions,
    test_event_types,
)
from binarycpython.tests.test_functions import (
    test_bin_data,
    test_create_arg_string,
    test_create_hdf5,
    test_example_parse_output,
    test_get_arg_keys,
    test_get_defaults,
    test_get_help,
    test_get_help_all,
    test_get_help_super,
    test_make_build_text,
    test_output_lines,
    test_remove_file,
    test_temp_dir,
    test_verbose_print,
    test_write_binary_c_parameter_descriptions_to_rst_file,
)
from binarycpython.tests.test_grid import (
    test__cleanup_defaults,
    test__increment_count,
    test__increment_probtot,
    test__return_argline,
    test__setup,
    test__source_file_sampling_system_dict_from_line_command_style,
    test_cmdline,
    test_evolve_single,
    test_export_all_info,
    test_grid_evolve,
    test_resultdict,
    test_return_all_info,
    test_return_binary_c_defaults,
    test_return_population_settings,
    test_set,
)
from binarycpython.tests.test_plot_functions import (
    test_color_by_index,
    test_plot_system,
)
from binarycpython.tests.test_run_system_wrapper import *
from binarycpython.tests.test_stellar_types import *
from binarycpython.tests.test_useful_funcs import (
    test_calc_period_from_sep,
    test_calc_sep_from_period,
    test_ragb,
    test_roche_lobe,
    test_rzams,
    test_zams_collission,
)
from binarycpython.tests.tests_population_extensions.test_condor import (
    test_condor_check_requirements,
    test_condor_dirs,
    test_condor_outfile,
    test_condorID,
    test_get_condor_status,
    test_make_condor_dirs,
    test_set_condor_status,
)
from binarycpython.tests.tests_population_extensions.test_distribution_functions import (
    test__get_multiplicity_dict,
    test_Arenou2010_binary_fraction,
    test_const_distribution,
    test_duquennoy1991,
    test_flat,
    test_flatsections,
    test_gaussian,
    test_get_max_multiplicity,
    test_imf_chabrier2003,
    test_imf_scalo1986,
    test_imf_scalo1998,
    test_imf_tinsley1980,
    test_Izzard2012_period_distribution,
    test_Kroupa2001,
    test_ktg93,
    test_number,
    test_powerlaw,
    test_raghavan2010_binary_fraction,
    test_sana12,
    test_three_part_power_law,
)
from binarycpython.tests.tests_population_extensions.test_HPC import (
    test_HPC_check_requirements,
    test_HPC_dir,
    test_HPC_dirs,
    test_HPC_get_status,
    test_HPC_id_filename,
    test_HPC_id_from_dir,
    test_HPC_job,
    test_HPC_job_task,
    test_HPC_job_type,
    test_HPC_jobID,
    test_HPC_jobID_tuple,
    test_HPC_njobs,
    test_HPC_set_status,
)
from binarycpython.tests.tests_population_extensions.test_population_options_defaults import (
    test_population_options_description_checker,
    test_population_options_validation,
    test_write_population_options_to_rst_file,
)
from binarycpython.tests.tests_population_extensions.test_sampling_variables import (  # test_add_grid_variable,
    test_add_sampling_variable,
)
from binarycpython.tests.tests_population_extensions.test_slurm import (
    test_get_slurm_status,
    test_make_slurm_dirs,
    test_set_slurm_status,
    test_slurm_check_requirements,
    test_slurm_dirs,
    test_slurm_outfile,
    test_slurmID,
)
from binarycpython.tests.tests_population_extensions.test_source_file_sampling import (
    test_source_file_sampling_column_type,
    test_source_file_sampling_command_type,
)
from binarycpython.tests.tests_population_extensions.test_spacing_functions import (
    test_const,
)
from binarycpython.tests.tests_population_extensions.test_version_info import (
    test_parse_binary_c_version_info,
    test_return_binary_c_version_info,
)

if __name__ == "__main__":
    unittest.main()
