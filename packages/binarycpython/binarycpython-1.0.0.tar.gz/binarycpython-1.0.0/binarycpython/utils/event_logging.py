"""
Functions to handle the event based logging output
"""

import os

import astropy.units as u

from binarycpython.utils.functions import get_numerical_value, output_lines

dimensionless_unit = u.m / u.m
EVENT_TYPE_INDEX = 3

########################
# event based logging header dictionary
event_based_logging_event_dict = {
    "SN_BINARY": {
        "name": "SN_BINARY",
        "longname": "binary star system SN event",
        "description": "SN_BINARY events are events that capture a supernova occuring in a binary system. The log contains information about the pre-supernova state of the system, the post-supernova state of the system, and the natal velocity kick.",
        "parameter_list": [
            "uuid",
            "probability",
            "event_number",
            "event_type",
            # ZAMS info
            "zams_mass_1",
            "zams_mass_2",
            "zams_orbital_period",
            "zams_separation",
            "zams_eccentricity",
            # common info
            "time",
            "metallicity",
            "random_seed",
            # Post SN info
            "SN_post_SN_mass",
            "SN_post_SN_stellar_type",
            "SN_type",
            "SN_fallback_fraction",
            "SN_fallback_mass",
            "SN_post_SN_ecc",
            "SN_post_SN_orbital_period",
            "SN_post_SN_separation",
            # Pre-SN
            "SN_pre_SN_mass",
            "SN_pre_SN_stellar_type",
            "SN_pre_SN_radius",
            "SN_pre_SN_core_mass",
            "SN_pre_SN_CO_core_mass",
            "SN_pre_SN_He_core_mass",
            "SN_pre_SN_fraction_omega_crit",
            "SN_pre_SN_ecc",
            "SN_pre_SN_orbital_period",
            "SN_pre_SN_separation",
            "SN_pre_SN_companion_mass",
            "SN_pre_SN_companion_radius",
            "SN_pre_SN_companion_stellar_type",
            # Some system stuff
            "SN_starnum",
            "SN_counter",
            # kick stuff
            "SN_kick_v",
            "SN_kick_omega",
            "SN_kick_phi",
        ],
    },
    "SN_SINGLE": {
        "name": "SN_SINGLE",
        "longname": "single star system SN event",
        "description": "SN_SINGLE events are events that capture a supernova occuring in a single system. The log contains information about the pre-supernova state of the system, the post-supernova state of the system, and the natal velocity kick.",
        "parameter_list": [
            "uuid",
            "probability",
            "event_number",
            "event_type",
            # ZAMS info
            "zams_mass_1",
            # common info
            "time",
            "metallicity",
            "random_seed",
            # Post SN info
            "SN_post_SN_mass",
            "SN_post_SN_stellar_type",
            "SN_type",
            "SN_fallback_fraction",
            "SN_fallback_mass",
            # Pre-SN
            "SN_pre_SN_mass",
            "SN_pre_SN_stellar_type",
            "SN_pre_SN_radius",
            "SN_pre_SN_core_mass",
            "SN_pre_SN_CO_core_mass",
            "SN_pre_SN_He_core_mass",
            "SN_pre_SN_fraction_omega_crit",
            # Some system stuff
            "SN_starnum",
            "SN_counter",
            # kick stuff
            "SN_kick_v",
            "SN_kick_omega",
            "SN_kick_phi",
        ],
    },
    "RLOF": {
        "name": "RLOF",
        "longname": "RLOF event",
        "description": "RLOF events are events that capture RLOF episode in a binary system. The log contains information about the pre-RLOF state of the system, the post-RLOF state of the system, and some cumulative properties recorded during the RLOF.",
        "parameter_list": [
            "uuid",
            "probability",
            "event_number",
            "event_type",
            # ZAMS info
            "zams_mass_1",
            "zams_mass_2",
            "zams_orbital_period",
            "zams_separation",
            "zams_eccentricity",
            # common info
            "time",
            "metallicity",
            "random_seed",
            # Initial properties
            "RLOF_initial_mass_accretor",
            "RLOF_initial_mass_donor",
            "RLOF_initial_radius_accretor",
            "RLOF_initial_radius_donor",
            "RLOF_initial_separation",
            "RLOF_initial_orbital_period",
            "RLOF_initial_stellar_type_accretor",
            "RLOF_initial_stellar_type_donor",
            "RLOF_initial_orbital_angular_momentum",
            "RLOF_initial_stability",
            "RLOF_initial_starnum_accretor",
            "RLOF_initial_starnum_donor",
            "RLOF_initial_time",
            "RLOF_initial_disk",
            # Final properties
            "RLOF_final_mass_accretor",
            "RLOF_final_mass_donor",
            "RLOF_final_radius_accretor",
            "RLOF_final_radius_donor",
            "RLOF_final_separation",
            "RLOF_final_orbital_period",
            "RLOF_final_stellar_type_accretor",
            "RLOF_final_stellar_type_donor",
            "RLOF_final_orbital_angular_momentum",
            "RLOF_final_stability",
            "RLOF_final_starnum_accretor",
            "RLOF_final_starnum_donor",
            "RLOF_final_time",
            "RLOF_final_disk",
            # Cumulative properties
            "RLOF_total_mass_lost",
            "RLOF_total_mass_accreted",
            "RLOF_total_mass_transferred",
            "RLOF_total_mass_lost_from_accretor",
            "RLOF_total_mass_lost_from_common_envelope",
            "RLOF_total_time_spent_masstransfer",
            #
            "RLOF_episode_number",
        ],
    },
    "DCO_formation": {
        "name": "DCO_formation",
        "longname": "DCO formation event",
        "description": "DCO formation events are events capture the formation of a double compact object. If both stars are of stellar type between HeWD and BH the system logs the first step of that formation. The log contains information about the system upon DCO formation, the step before the DCO formation and the relevant GW times.",
        "parameter_list": [
            "uuid",
            "probability",
            "event_number",
            "event_type",
            # ZAMS info
            "zams_mass_1",
            "zams_mass_2",
            "zams_orbital_period",
            "zams_separation",
            "zams_eccentricity",
            # common info
            "time",
            "metallicity",
            "random_seed",
            # DCO formation properties
            "DCO_stellar_type_1",
            "DCO_stellar_type_2",
            "DCO_mass_1",
            "DCO_mass_2",
            #
            "DCO_separation",
            "DCO_eccentricity",
            "DCO_period",
            #
            "DCO_previous_separation",
            "DCO_previous_eccentricity",
            "DCO_previous_period",
            #
            "DCO_formation_time_in_years",
            "DCO_inspiral_time_in_years",
            "DCO_merger_time_in_years",
            #
            "DCO_total_rlof_episodes",
            "DCO_stable_rlof_episodes",
            "DCO_unstable_rlof_episodes",
        ],
    },
}

event_based_logging_parameter_list_dict = {
    event_key: event_dict["parameter_list"]
    for event_key, event_dict in event_based_logging_event_dict.items()
}

########################
# event based logging parameter description dictionary
#   this dictionary contains descriptions and units for the parameters that are contained in the event based logging output

event_based_logging_parameter_description_dict = {
    "uuid": {
        "description": "unique token associated with the system",
    },
    "event_type": {
        "description": "event type",
    },
    "event_number": {
        "description": "event number to keep track of chronological order of events of this system. Count starts at 0.",
    },
    "zams_mass_1": {
        "description": "ZAMS mass of initially primary star",
        "unit": u.Msun,
    },
    "zams_mass_2": {
        "description": "ZAMS mass of initially secondary star",
        "unit": u.Msun,
    },
    "zams_orbital_period": {
        "description": "ZAMS period of the inner two binary stars",
        "unit": u.yr,
    },
    "zams_separation": {
        "description": "ZAMS separation of the inner two binary stars",
        "unit": u.Rsun,
    },
    "zams_eccentricity": {
        "description": "ZAMS eccentricity of the inner two binary stars",
    },
    "metallicity": {
        "description": "metallicity of the star system",
    },
    "probability": {
        "description": "probability of the star system",
    },
    "random_seed": {
        "description": "random seed of the star system",
    },
    "SN_post_SN_mass": {
        "description": "Post supernova mass of the star that went supernova",
        "unit": u.Msun,
    },
    "SN_post_SN_stellar_type": {
        "description": "Post supernova stellar type of the star that went supernova",
    },
    "time": {"description": "Time at which the event is logged", "unit": u.Myr},
    "SN_type": {
        "description": "Supernova type",
    },
    "SN_fallback_fraction": {
        "description": "Fallback of initial supernova ejecta mass that falls back onto the remnant. based on Fryer 2012.",
    },
    "SN_fallback_mass": {
        "description": "Mass of initial supernova ejecta mass that falls back onto the remnant. based on Fryer 2012.",
        "unit": u.Msun,
    },
    "SN_post_SN_ecc": {
        "description": "Post-supernova eccentricity of the system.",
    },
    "SN_post_SN_orbital_period": {
        "description": "Post-supernova orbital period of the system.",
        "unit": u.yr,
    },
    "SN_post_SN_separation": {
        "description": "Post-supernova separation of the system.",
        "unit": u.Rsun,
    },
    "SN_pre_SN_mass": {
        "description": "Pre-supernova mass of the star that went supernova.",
        "unit": u.Msun,
    },
    "SN_pre_SN_stellar_type": {
        "description": "Pre-supernova stellar type of the star that went supernova.",
        "unit": u.Msun,
    },
    "SN_pre_SN_radius": {
        "description": "Pre-supernova radius of the star that went supernova.",
        "unit": u.Rsun,
    },
    "SN_pre_SN_core_mass": {
        "description": "Pre-supernova core mass of the star that went supernova.",
        "unit": u.Msun,
    },
    "SN_pre_SN_CO_core_mass": {
        "description": "Pre-supernova CO core mass of the star that went supernova.",
        "unit": u.Msun,
    },
    "SN_pre_SN_He_core_mass": {
        "description": "Pre-supernova He core mass of the star that went supernova.",
        "unit": u.Msun,
    },
    "SN_pre_SN_fraction_omega_crit": {
        "description": "Pre-supernova fraction of critical rotation rate of the star that went supernova.",
    },
    "SN_pre_SN_ecc": {
        "description": "Pre-supernova eccentricity of the system.",
    },
    "SN_pre_SN_orbital_period": {
        "description": "Pre-supernova orbital period of the system.",
        "unit": u.yr,
    },
    "SN_pre_SN_separation": {
        "description": "Pre-supernova separation of the system.",
        "unit": u.Rsun,
    },
    "SN_pre_SN_companion_mass": {
        "description": "Pre-supernova mass of the companion of the star that went supernova.",
        "unit": u.Msun,
    },
    "SN_pre_SN_companion_radius": {
        "description": "Pre-supernova radius of the companion of the star that went supernova.",
        "unit": u.Rsun,
    },
    "SN_starnum": {
        "description": "Star number of the star that went supernova.",
    },
    "SN_pre_SN_companion_stellar_type": {
        "description": "Pre-supernova stellar type of the companion of the star that went supernova.",
    },
    "SN_counter": {
        "description": "Pre-supernova stellar type of the companion of the star that went supernova.",
    },
    "SN_kick_v": {"description": "Supernova natal kick velocity", "unit": u.km / u.s},
    "SN_kick_omega": {
        "description": "Supernova omega angle",  # TODO: provide citation or source
    },
    "SN_kick_phi": {
        "description": "Supernova phi angle",  # TODO: provide citation or source
    },
    "RLOF_initial_mass_accretor": {
        "description": "Mass of the initial accretor star at the onset of RLOF",
        "unit": u.Msun,
    },
    "RLOF_initial_mass_donor": {
        "description": "Mass of the initial donor star at the onset of RLOF",
        "unit": u.Msun,
    },
    "RLOF_initial_radius_accretor": {
        "description": "Radius of the initial accretor star at the onset of RLOF",
        "unit": u.Rsun,
    },
    "RLOF_initial_radius_donor": {
        "description": "Radius of the initial donor star at the onset of RLOF",
        "unit": u.Rsun,
    },
    "RLOF_initial_separation": {
        "description": "Separation of the binary system at the onset of RLOF",
        "unit": u.Rsun,
    },
    "RLOF_initial_orbital_period": {
        "description": "Orbital period of the binary system at the onset of RLOF",
        "unit": u.yr,
    },
    "RLOF_initial_stellar_type_accretor": {
        "description": "Stellar type of the initial accretor star at the onset of RLOF",
    },
    "RLOF_initial_stellar_type_donor": {
        "description": "Stellar type of the initial donor star at the onset of RLOF",
    },
    "RLOF_initial_orbital_angular_momentum": {
        "description": "Orbital angular momentum of the binary system at the onset of RLOF",
        "unit": u.m,  # TODO: get unit of angular momentum
    },
    "RLOF_initial_stability": {
        "description": "initial stability of the RLOF",
    },
    "RLOF_initial_starnum_accretor": {
        "description": "Star number of the initial accretor star at the onset of RLOF",
    },
    "RLOF_initial_starnum_donor": {
        "description": "Star number of the initial donor star at the onset of RLOF",
    },
    "RLOF_initial_time": {
        "description": "Time at the onset of RLOF",
        "unit": u.yr,
    },
    "RLOF_initial_disk": {
        "description": "Boolean of whether the mass transfer is through an accretion disk at the onset of RLOF",
    },
    "RLOF_final_mass_accretor": {
        "description": "Mass of the final accretor star at the end of RLOF",
        "unit": u.Msun,
    },
    "RLOF_final_mass_donor": {
        "description": "Mass of the final donor star at the end of RLOF",
        "unit": u.Msun,
    },
    "RLOF_final_radius_accretor": {
        "description": "Radius of the final accretor star at the end of RLOF",
        "unit": u.Rsun,
    },
    "RLOF_final_radius_donor": {
        "description": "Radius of the final donor star at the end of RLOF",
        "unit": u.Rsun,
    },
    "RLOF_final_separation": {
        "description": "Separation of the binary system at the end of RLOF",
        "unit": u.Rsun,
    },
    "RLOF_final_orbital_period": {
        "description": "Orbital period of the binary system at the end of RLOF",
        "unit": u.yr,
    },
    "RLOF_final_stellar_type_accretor": {
        "description": "Stellar type of the final accretor star at the end of RLOF",
    },
    "RLOF_final_stellar_type_donor": {
        "description": "Stellar type of the final donor star at the end of RLOF",
    },
    "RLOF_final_orbital_angular_momentum": {
        "description": "Orbital angular momentum of the binary system at the end of RLOF",
        "unit": u.m,  # TODO: get unit of angular momentum
    },
    "RLOF_final_stability": {
        "description": "final stability of the RLOF",
    },
    "RLOF_final_starnum_accretor": {
        "description": "Star number of the final accretor star at the end of RLOF",
    },
    "RLOF_final_starnum_donor": {
        "description": "Star number of the final donor star at the end of RLOF",
    },
    "RLOF_final_time": {
        "description": "Time at the end of RLOF",
        "unit": u.yr,
    },
    "RLOF_final_disk": {
        "description": "Boolean of whether the mass transfer is through an accretion disk at the end of RLOF",
    },
    "RLOF_total_mass_lost": {
        "description": "Total mass lost from the system during the RLOF episode",
        "unit": u.Msun,
    },
    "RLOF_total_mass_accreted": {
        "description": "Total mass accreted onto the accretor during the RLOF episode",
        "unit": u.Msun,
    },
    "RLOF_total_mass_transferred": {
        "description": "Total mass transferred by the donor during the RLOF episode",
        "unit": u.Msun,
    },
    "RLOF_total_mass_lost_from_accretor": {
        "description": "Total mass lost from the accretor during the RLOF episode",
        "unit": u.Msun,
    },
    "RLOF_total_mass_lost_from_common_envelope": {
        "description": "Total mass lost from the system through common envelope ejection",
        "unit": u.Msun,
    },
    "RLOF_total_time_spent_masstransfer": {
        "description": "Duration of the RLOF episode",
        "unit": u.yr,
    },
    "RLOF_episode_number": {
        "description": "RLOF episode number",
    },
    "DCO_stellar_type_1": {
        "description": "Stellar type of the initially most massive star",
    },
    "DCO_stellar_type_2": {
        "description": "Stellar type of the initially second-most massive star",
    },
    "DCO_mass_1": {
        "description": "Mass of the initially most massive star",
        "unit": u.Msun,
    },
    "DCO_mass_2": {
        "description": "Mass of the initially second-most massive star",
        "unit": u.yr,
    },
    "DCO_separation": {
        "description": "Separation of the binary system",
        "unit": u.Rsun,
    },
    "DCO_eccentricity": {
        "description": "Eccentricity of the binary system",
    },
    "DCO_period": {
        "description": "Period of the binary system",
        "unit": u.yr,
    },
    "DCO_previous_separation": {
        "description": "Separation of the binary system in the previous timestep",
        "unit": u.Rsun,
    },
    "DCO_previous_eccentricity": {
        "description": "Eccentricity of the binary system in the previous timestep",
    },
    "DCO_previous_period": {
        "description": "Period of the binary system in the previous timestep",
        "unit": u.yr,
    },
    "DCO_formation_time_in_years": {
        "description": "Time from birth until the formation of the DCO",
        "unit": u.yr,
    },
    "DCO_inspiral_time_in_years": {
        "description": "Gravitational wave inspiral time of the DCO",
        "unit": u.yr,
    },
    "DCO_merger_time_in_years": {
        "description": "Total time from birth to merging of the DCO",
        "unit": u.yr,
    },
    "DCO_total_rlof_episodes": {
        "description": "Total number of RLOF episodes preceding the formation of the DCO",
    },
    "DCO_stable_rlof_episodes": {
        "description": "Total number of stable RLOF episodes preceding the formation of the DCO",
    },
    "DCO_unstable_rlof_episodes": {
        "description": "Total number of unstable RLOF episodes preceding the formation of the DCO",
    },
}

########################
# Functions for the event based logging


def event_based_logging_parse_values(string_value):
    """
    Function to parse values for the source file sampling
    """

    try:
        value = get_numerical_value(string_value)
    except ValueError:
        value = str(string_value)

    return value


def event_based_logging_output_parser(
    self, events_parameters_list_dict, output_dir, output, separator="\t"
):
    """
    Function to handle parsing the events output
    """

    ###############
    # Set event outfile name
    event_outfilename = os.path.join(
        output_dir, "events-{}.dat".format(self.process_ID)
    )

    # Touch the event output file
    if not os.path.exists(event_outfilename):
        with open(event_outfilename, "w") as _:
            pass

    ###############
    # Loop over the output
    with open(event_outfilename, "a") as events_f:
        for line in output_lines(output):
            # Handle the events line
            if line.startswith("EVENT"):
                events_values = line.split()[1:]
                # Check for correct length
                event_type = events_values[EVENT_TYPE_INDEX]
                if not len(events_values) == len(
                    events_parameters_list_dict[event_type]
                ):
                    print(
                        "Length of readout values ({}) is not equal to length of parameters ({}) for event type: {}".format(
                            len(events_values),
                            len(events_parameters_list_dict[event_type]),
                            event_type,
                        )
                    )
                    raise ValueError

                # write values
                events_f.write(separator.join(events_values[:]) + "\n")


def event_based_logging_split_event_types_to_files(
    input_file, events_parameters_list_dict, remove_original_file=False
):
    """
    Function to split the event types to file per event type
    """

    # Set separator
    separator = "\t"

    # Get dirname
    dirname = os.path.dirname(input_file)

    ####################
    # Loop over the events file to find the unique event names
    unique_events_list = []
    with open(input_file, "r") as f:
        for line in f:
            values = line.strip().split()
            event_type = values[EVENT_TYPE_INDEX]

            if event_type not in unique_events_list:
                unique_events_list.append(event_type)

    ####################
    # Construct output filenames
    unique_events_filename_dict = {}
    for unique_event in unique_events_list:
        unique_event_filename = os.path.join(
            dirname, "total_{}_events.dat".format(unique_event)
        )
        unique_events_filename_dict[unique_event] = unique_event_filename

    ####################
    # Create files
    for unique_event, unique_event_filename in unique_events_filename_dict.items():
        with open(unique_event_filename, "w") as unique_event_f:
            unique_event_f.write(
                separator.join(events_parameters_list_dict[unique_event]) + "\n"
            )

    ####################
    # Loop over the total file again and write the events to each of the events files
    for unique_event, unique_event_filename in unique_events_filename_dict.items():
        with open(unique_event_filename, "a") as event_f:
            with open(input_file, "r") as source_f:
                for line in source_f:
                    events_values = line.strip().split()
                    event_type = events_values[EVENT_TYPE_INDEX]

                    if event_type == unique_event:
                        # Check if we have the same length of values as to what we expect based on the parameter list
                        if not len(events_values) == len(
                            events_parameters_list_dict[event_type]
                        ):
                            print(
                                "Length of readout values ({}) is not equal to length of parameters ({})".format(
                                    len(events_values),
                                    len(events_parameters_list_dict[event_type]),
                                )
                            )
                            raise ValueError

                        # Write line
                        event_f.write(separator.join(events_values[:]) + "\n")

    ####################
    # Remove original file
    if remove_original_file:
        os.remove(input_file)


def event_based_logging_combine_individual_event_files(
    output_dir,
    basename,
    combined_name,
    check_duplicates_and_all_present=False,
    remove_individual_files=False,
):
    """
    Function to combine the individual result files
    """

    ############
    # Get all the individual files
    full_path_individual_list = []
    for file in os.listdir(output_dir):
        if file.startswith(basename):
            full_path_individual_list.append(os.path.join(output_dir, file))

    ####################
    # handle the combined file
    full_path_combined = os.path.join(output_dir, combined_name)
    if os.path.exists(full_path_combined):
        os.remove(full_path_combined)
    # Check if the file doesnt exist yet. If not them write the headerline.
    if not os.path.exists(full_path_combined):
        with open(full_path_combined, "w") as _:
            pass

    ############
    # Handle writing the contents of the individual files to the combined file
    # loop over the individual files and write to
    with open(full_path_combined, "a") as output_f:
        for full_path_individual in full_path_individual_list:
            # Loop over file and add lines together
            with open(full_path_individual) as f:
                for line in f:
                    output_f.write(line)

    ####################
    # Check whether we have duplicates
    if check_duplicates_and_all_present:
        already_found = []

        # Check duplicates
        with open(full_path_combined, "r") as f:
            line = f.readline()

            for line in f:
                if line not in already_found:
                    already_found.append(line)
                else:
                    print("FOUND DUPLICATE!")

        # Check if they're all present:
        for full_path_individual in full_path_individual_list:
            with open(full_path_individual, "r") as indiv_f:
                line = indiv_f.readline()

                for line in indiv_f:
                    if line not in already_found:
                        print("CANT FIND MY LINE")

    ####################
    # Remove files
    if remove_individual_files:
        for full_path_individual in full_path_individual_list:
            os.remove(full_path_individual)


def event_based_logging_parse_description(description_dict):
    """
    Function to parse the description_string
    """

    description_string = description_dict["description"]

    # Capitalise first letter
    description_string = description_string[0].capitalize() + description_string[1:]

    # Add period
    if description_string[-1] != ".":
        description_string = description_string + "."

    # Add unit (in latex)
    if "unit" in description_dict:
        if description_dict["unit"] != dimensionless_unit:
            description_string = description_string + "\n\n\n\nUnit: [{}].".format(
                description_dict["unit"].to_string("latex_inline")
            )

    ##############
    # Check if there are newlines, and replace them by newlines with indent
    description_string = description_string.replace("\n", "\n       ")

    return description_string


def event_based_logging_build_event_description_table(event_dict):
    """
    Function to create a table containing the description of the parameters in the event log
    """

    #
    indent = "   "

    # Get parameter list and parse descriptions
    parameter_list = event_dict["parameter_list"]
    parameter_list_with_descriptions = [
        [
            parameter,
            event_based_logging_parse_description(
                description_dict=event_based_logging_parameter_description_dict[
                    parameter
                ]
            ),
        ]
        for parameter in parameter_list
    ]

    # Construct parameter list
    rst_event_table = """
.. list-table:: {}
{}:widths: 25, 75
{}:header-rows: 1

""".format(
        event_dict["name"] + " event output log contents", indent, indent
    )

    #
    rst_event_table += indent + "* - Parameter\n"
    rst_event_table += indent + "  - Description\n"

    for parameter_el in parameter_list_with_descriptions:
        rst_event_table += indent + "* - {}\n".format(parameter_el[0])
        rst_event_table += indent + "  - {}\n".format(parameter_el[1])

    return rst_event_table


def event_based_logging_build_event_description_section(event_dict):
    """
    Function to create the section for the event log
    """

    # Set up event section rst
    rst_event_section = ""

    # Construct section name

    longname = event_dict["longname"]
    longname = longname[0].capitalize() + longname[1:]

    rst_event_section_name = "{} ({}) section\n".format(longname, event_dict["name"])
    rst_event_section += rst_event_section_name
    rst_event_section += "-" * len(rst_event_section_name.strip()) + "\n"
    rst_event_section += "\n"

    # Construct description of event
    rst_event_section += event_dict["description"] + "\n\n"

    # Construct the table of the section
    rst_event_table = event_based_logging_build_event_description_table(event_dict)
    rst_event_section += rst_event_table

    return rst_event_section


def event_based_logging_build_event_descriptions_rst(event_based_logging_event_dict):
    """
    Main function to build the event descriptions rst string
    """

    rst_string = """Event based logging\n===================

We can configure binary_c to output information about certain events. See [Notebook for events based logging](https://binary_c.gitlab.io/binary_c-python/examples/notebook_event_based_logging.html)

In the following subsections we describe the content of each of these event output logs.\n\n
"""

    # construct event sections
    for _, event_dict in event_based_logging_event_dict.items():
        rst_event_section = event_based_logging_build_event_description_section(
            event_dict
        )
        rst_event_section += "\n"

        rst_string += rst_event_section

    return rst_string


def event_based_logging_write_event_descriptions_to_rst_file(rst_filename):
    """
    Function to write the event based logging descriptions to rst file
    """

    # Check filename
    if not rst_filename.endswith(".rst"):
        raise ValueError("filename is not an rst filename")

    # build rst string
    rst_string = event_based_logging_build_event_descriptions_rst(
        event_based_logging_event_dict
    )

    # write to file
    with open(rst_filename, "w") as f:
        f.write(rst_string)


if __name__ == "__main__":

    rst_string = event_based_logging_build_event_descriptions_rst(
        event_based_logging_event_dict
    )
    print(rst_string)
    # event_based_logging_build_event_description_section(
    #     event_based_logging_event_dict["SN_BINARY"]
    # )

    # for key in event_based_logging_headers_dict:
    #     for parameter in event_based_logging_headers_dict[key]:
    #         description_dict = event_based_header_parameter_description_dict[parameter]

    #         # get description string
    #         description_string = event_based_header_parse_description(
    #             description_dict=description_dict
    #         )
    #         print(description_string)
