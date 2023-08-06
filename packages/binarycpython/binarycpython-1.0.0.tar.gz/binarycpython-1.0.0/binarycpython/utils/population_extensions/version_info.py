"""
File containing the class object containing the functions to handle binary_c version info.

This class will be used to extend the population object

NOTE: could these functions not just be normal functions rather than class methods? I see hardly any use of the self
"""

# pylint: disable=E0203

import copy
import os
from typing import Union

from binarycpython import _binary_c_bindings
from binarycpython.utils.functions import isfloat


class version_info:
    """
    Class object containing the functions to handle binary_c version info.

    This class will be used to extend the population object
    """

    def __init__(self, **kwargs):
        """
        Init function for the version_info class
        """

        return

    ########################################################
    # version_info functions
    ########################################################
    def return_binary_c_version_info(self, parsed: bool = True) -> Union[str, dict]:
        """
        Function that returns the version information of binary_c. This function calls the function
        _binary_c_bindings.return_version_info()

        Args:
            parsed: Boolean flag whether to parse the version_info output of binary_c. default = False

        Returns:
            Either the raw string of binary_c or a parsed version of this in the form of a nested
            dictionary
        """

        #####
        # Check if the headers were previously defined
        found_prev_MACRO_HEADER = False
        if "BINARY_C_MACRO_HEADER" in os.environ:
            # the env var is already present. lets save that and put that back later
            found_prev_MACRO_HEADER = True
            prev_value_MACRO_HEADER = os.environ["BINARY_C_MACRO_HEADER"]

        found_prev_DEFLIST_HEADER = False
        if "BINARY_C_DEFLIST_HEADER" in os.environ:
            # the env var is already present. lets save that and put that back later
            found_prev_DEFLIST_HEADER = True
            prev_value_DEFLIST_HEADER = os.environ["BINARY_C_DEFLIST_HEADER"]

        #############
        # set new headers
        os.environ["BINARY_C_MACRO_HEADER"] = "macroxyz"
        os.environ["BINARY_C_DEFLIST_HEADER"] = "deflist "

        #############
        # Get version_info
        raw_version_info = _binary_c_bindings.return_version_info().strip()

        #############
        # delete current headers
        del os.environ["BINARY_C_MACRO_HEADER"]
        del os.environ["BINARY_C_DEFLIST_HEADER"]

        #############
        # put back previous headers
        if found_prev_MACRO_HEADER:
            os.environ["BINARY_C_MACRO_HEADER"] = prev_value_MACRO_HEADER

        if found_prev_DEFLIST_HEADER:
            os.environ["BINARY_C_DEFLIST_HEADER"] = prev_value_DEFLIST_HEADER

        ##############
        # return (parsed) version info
        if parsed:
            parsed_version_info = self.parse_binary_c_version_info(raw_version_info)
            return parsed_version_info

        return raw_version_info

    def _parse_binary_c_version_info_networks(self, networks):
        """
        Function to parse the networks info
        """

        networks_dict = {}
        for el in networks:
            network_dict = {}
            split_info = el.split("Network ")[-1].strip().split("==")

            network_number = int(split_info[0])
            network_dict["network_number"] = network_number

            network_info_split = split_info[1].split(" is ")

            shortname = network_info_split[0].strip()
            network_dict["shortname"] = shortname

            if not network_info_split[1].strip().startswith(":"):
                network_split_info_extra = network_info_split[1].strip().split(":")

                longname = network_split_info_extra[0].strip()
                network_dict["longname"] = longname

                implementation = (
                    network_split_info_extra[1].strip().replace("implemented in", "")
                )
                if implementation:
                    network_dict["implemented_in"] = [
                        i.strip("()") for i in implementation.strip().split()
                    ]

            networks_dict[network_number] = copy.deepcopy(network_dict)

        return networks_dict if networks_dict else None

    def _parse_binary_c_version_info_isotopes(self, isotopes):
        """
        Function to parse the isotopes info
        """

        isotope_dict = {}
        for el in isotopes:
            split_info = el.split("Isotope ")[-1].strip().split(" is ")

            isotope_info = split_info[-1]
            name = isotope_info.split(" ")[0].strip()

            # Get details
            mass_g = float(
                isotope_info.split(",")[0].split("(")[1].split("=")[-1][:-2].strip()
            )
            mass_amu = float(
                isotope_info.split(",")[0].split("(")[-1].split("=")[-1].strip()
            )
            mass_mev = float(
                isotope_info.split(",")[-3].split("=")[-1].replace(")", "").strip()
            )
            A = int(isotope_info.split(",")[-1].strip().split("=")[-1].replace(")", ""))
            Z = int(isotope_info.split(",")[-2].strip().split("=")[-1])

            #
            isotope_dict[int(split_info[0])] = {
                "name": name,
                "Z": Z,
                "A": A,
                "mass_mev": mass_mev,
                "mass_g": mass_g,
                "mass_amu": mass_amu,
            }

        return isotope_dict if isotope_dict else None

    def _parse_binary_c_version_info_argpairs(self, argpairs):
        """
        Function to parse the argpairs info
        """

        argpair_dict = {}
        for el in sorted(argpairs):
            split_info = el.split("ArgPair ")[-1].split(" ")

            if not argpair_dict.get(split_info[0], None):
                argpair_dict[split_info[0]] = {split_info[1]: split_info[2]}
            else:
                argpair_dict[split_info[0]][split_info[1]] = split_info[2]

        return argpair_dict if argpair_dict else None

    def _parse_binary_c_version_info_ensembles(self, ensembles):
        """
        Function to parse the ensembles info
        """

        ensemble_dict = {}
        ensemble_filter_dict = {}
        for el in ensembles:
            split_info = el.split("Ensemble ")[-1].split(" is ")

            if len(split_info) > 1:
                if not split_info[0].startswith("filter"):
                    ensemble_dict[int(split_info[0])] = split_info[-1]
                else:
                    filter_no = int(split_info[0].replace("filter ", ""))
                    ensemble_filter_dict[filter_no] = split_info[-1]

        return ensemble_dict, ensemble_filter_dict

    def _parse_binary_c_version_info_macros(self, macros):
        """
        Function to parse the macros info
        """

        param_type_dict = {
            "STRING": str,
            "FLOAT": float,
            "MACRO": str,
            "INT": int,
            "LONG_INT": int,
            "UINT": int,
        }

        macros_dict = {}
        for el in macros:
            split_info = el.split("macroxyz ")[-1].split(" : ")
            param_type = split_info[0]

            new_split = "".join(split_info[1:]).split(" is ")
            param_name = new_split[0].strip()
            param_value = " is ".join(new_split[1:])
            param_value = param_value.strip()

            # If we're trying to set the value to "on", check that
            # it doesn't already exist. If it does, do nothing, as the
            # extra information is better than just "on"
            if param_name in macros_dict:
                if macros_dict[param_name] == "on":
                    # update with better value
                    store = True
                elif (
                    isfloat(macros_dict[param_name]) is False
                    and isfloat(param_value) is True
                ):
                    # store the number we now have to replace the non-number we had
                    store = True
                else:
                    # don't override existing number
                    store = False

            else:
                store = True

            if store:
                # Sometimes the macros have extra information behind it.
                # Needs an update in outputting by binary_c (RGI: what does this mean David???)
                try:
                    macros_dict[param_name] = param_type_dict[param_type](param_value)
                except ValueError:
                    macros_dict[param_name] = str(param_value)

        return macros_dict if macros_dict else None

    def _parse_binary_c_version_info_elements(self, elements):
        """
        Function to parse the elements info
        """

        # Fill dict:
        elements_dict = {}
        for el in elements:
            split_info = el.split("Element ")[-1].split(" : ")
            name_info = split_info[0].split(" is ")

            # get isotope info
            isotopes = {}
            if not split_info[-1][0] == "0":
                isotope_string = split_info[-1].split(" = ")[-1]
                isotopes = {
                    int(split_isotope.split("=")[0]): split_isotope.split("=")[1]
                    for split_isotope in isotope_string.split(" ")
                }

            elements_dict[int(name_info[0])] = {
                "name": name_info[-1],
                "atomic_number": int(name_info[0]),
                "amt_isotopes": len(isotopes),
                "isotopes": isotopes,
            }

        return elements_dict if elements_dict else None

    def _parse_binary_c_version_info_dt_limits(self, dt_limits):
        """
        Function to parse the dt_limits info
        """

        # Fill dict
        dt_limits_dict = {}
        for el in dt_limits:
            split_info = el.split("DTlimit ")[-1].split(" : ")
            dt_limits_dict[split_info[1].strip()] = {
                "index": int(split_info[0]),
                "value": float(split_info[-1]),
            }

        return dt_limits_dict if dt_limits_dict else None

    def _parse_binary_c_version_info_units(self, unit, units):
        """
        Function to parse the units info

        TODO: i'm not sure that this parsing is correct
        """

        units_dict = {}
        for el in unit:
            split_info = el.split("Unit ")[-1].split(",")
            s = split_info[0].split(" is ")

            if len(s) == 2:
                long, short = [i.strip().strip('"') for i in s]
            elif len(s) == 1:
                long, short = None, s[0]
            else:
                self.vb_warning("Warning: Failed to split unit string {}".format(el))

            to_cgs = (split_info[1].split())[3].strip().strip('"')
            code_units = split_info[2].split()
            code_unit_type_num = int(code_units[3].strip().strip('"'))
            code_unit_type = code_units[4].strip().strip('"')
            code_unit_cgs_value = code_units[9].strip().strip('"').strip(")")
            units_dict[long] = {
                "long": long,
                "short": short,
                "to_cgs": to_cgs,
                "code_unit_type_num": code_unit_type_num,
                "code_unit_type": code_unit_type,
                "code_unit_cgs_value": code_unit_cgs_value,
            }

        # Add the list of units
        for el in units:
            el = el[7:]  # removes "Units: "
            units_dict["units list"] = el.strip("Units:")

        return units_dict if units_dict else None

    def _parse_binary_c_version_nucsyn_sources(self, nucsyn_sources):
        """
        Function to parse the nucsyn_sources info
        """

        # Fill dict
        nucsyn_sources_dict = {}
        for el in nucsyn_sources:
            split_info = el.split("Nucleosynthesis source")[-1].strip().split(" is ")
            nucsyn_sources_dict[int(split_info[0])] = split_info[-1]

        return nucsyn_sources_dict if nucsyn_sources_dict else None

    def _parse_binary_c_version_binary_c_error_codes(self, binary_c_error_codes):
        """
        Function to parse the binary_c_error_codes info
        """

        binary_c_error_codes_dict = {}
        for el in binary_c_error_codes:
            split_info = el.split("Error code")[-1].strip().split(" = ")

            # extract info
            number = int(split_info[1].split()[0])
            name = str(split_info[0])
            description = str(split_info[1].split()[1].replace('"', ""))

            binary_c_error_codes_dict[number] = {
                "number": number,
                "name": name,
                "description": description,
            }

        return binary_c_error_codes_dict if binary_c_error_codes_dict else None

    def _parse_binary_c_version_deflists(self, deflists):
        """
        Function to parse the deflists info
        """

        deflist_dict = {}
        for el in deflists:
            split_info = el.split("deflist")[-1].strip().split()

            # Extract data
            deflist_type = split_info[0]
            deflist_data = " ".join(split_info[1:])

            # Check if current type is already known
            if deflist_type not in deflist_dict:
                deflist_dict[deflist_type] = {}

            # store data in current type dict
            deflist_data_split = deflist_data.split(" is ")
            deflist_data_number = int(deflist_data_split[0])
            deflist_data_name = str(deflist_data_split[1])

            deflist_dict[deflist_type][deflist_data_number] = deflist_data_name

        return deflist_dict if deflist_dict else None

    def parse_binary_c_version_info(self, version_info_string: str) -> dict:
        """
        Function that parses the binary_c version info. Long function with a lot of branches

        Args:
            version_info_string: raw output of version_info call to binary_c

        Returns:
            Parsed version of the version info, which is a dictionary containing the keys: 'isotopes' for isotope info, 'argpairs' for argument pair info (TODO: explain), 'ensembles' for ensemble settings/info, 'macros' for macros, 'elements' for atomic element info, 'DTlimit' for (TODO: explain), 'nucleosynthesis_sources' for nucleosynthesis sources, and 'miscellaneous' for all those that were not caught by the previous groups. 'git_branch', 'git_build', 'revision' and 'email' are also keys, but its clear what those contain.
        """

        version_info_dict = {}

        # Clean data and put in correct shape
        splitted = version_info_string.strip().splitlines()
        cleaned = {el.strip() for el in splitted if not el == ""}

        ##########################
        # Network:

        # Split off all the networks
        networks = {el for el in cleaned if el.startswith("Network ")}
        cleaned = cleaned - networks

        # and parse the info
        version_info_dict["networks"] = self._parse_binary_c_version_info_networks(
            networks
        )

        ##########################
        # Isotopes:

        # Split off all the isotopes
        isotopes = {el for el in cleaned if el.startswith("Isotope ")}
        cleaned -= isotopes

        # and parse the info
        version_info_dict["isotopes"] = self._parse_binary_c_version_info_isotopes(
            isotopes
        )

        ##########################
        # Arg pairs:

        # Split off all the argpairs
        argpairs = {el for el in cleaned if el.startswith("ArgPair")}
        cleaned -= argpairs

        # and parse the info
        version_info_dict["argpairs"] = self._parse_binary_c_version_info_argpairs(
            argpairs
        )

        ##########################
        # ensembles:

        # Split off all the ensembles
        ensembles = {el for el in cleaned if el.startswith("Ensemble")}
        cleaned -= ensembles

        # and parse the info
        (
            ensemble_dict,
            ensemble_filter_dict,
        ) = self._parse_binary_c_version_info_ensembles(ensembles)

        version_info_dict["ensembles"] = ensemble_dict if ensemble_dict else None
        version_info_dict["ensemble_filters"] = (
            ensemble_filter_dict if ensemble_filter_dict else None
        )

        ##########################
        # macros:

        # Split off of all the macros
        macros = {el for el in cleaned if el.startswith("macroxyz")}
        cleaned -= macros

        # and parse the info
        version_info_dict["macros"] = self._parse_binary_c_version_info_macros(macros)

        ##########################
        # Elements:

        # Split off all the elements
        elements = {el for el in cleaned if el.startswith("Element")}
        cleaned -= elements

        # and parse the info
        version_info_dict["elements"] = self._parse_binary_c_version_info_elements(
            elements
        )

        ##########################
        # dt_limits:

        # split off all the dt_limits
        dt_limits = {el for el in cleaned if el.startswith("DTlimit")}
        cleaned -= dt_limits

        # and parse the info
        version_info_dict["dt_limits"] = self._parse_binary_c_version_info_dt_limits(
            dt_limits
        )

        ##############################
        # Units

        # split off all the units
        unit = {el for el in cleaned if el.startswith("Unit ")}
        cleaned -= unit

        units = {el for el in cleaned if el.startswith("Units: ")}
        cleaned -= units

        # and parse the info
        version_info_dict["units"] = self._parse_binary_c_version_info_units(
            unit, units
        )

        ##########################
        # Nucleosynthesis sources:

        # Split off all the nucsyn sources
        nucsyn_sources = {el for el in cleaned if el.startswith("Nucleosynthesis")}
        cleaned -= nucsyn_sources

        # and parse the info
        version_info_dict[
            "nucleosynthesis_sources"
        ] = self._parse_binary_c_version_nucsyn_sources(nucsyn_sources)

        ##########################
        # binary_c_errors:

        # Split off all the nucsyn sources
        binary_c_error_codes = {el for el in cleaned if el.startswith("Error code")}
        cleaned -= binary_c_error_codes

        # and parse the info
        version_info_dict[
            "binary_c_error_codes"
        ] = self._parse_binary_c_version_binary_c_error_codes(binary_c_error_codes)

        ##########################
        # deflist:

        # Split off all the deflists
        deflists = {el for el in cleaned if el.startswith("deflist")}
        cleaned -= deflists

        # and parse the info
        version_info_dict["deflists"] = self._parse_binary_c_version_deflists(deflists)

        ##########################
        # miscellaneous:
        # All those that I didn't catch with the above filters. Could try to get some more out though.

        misc_dict = {}

        # Filter out git revision
        git_revision = [el for el in cleaned if el.startswith("git revision")]
        misc_dict["git_revision"] = (
            git_revision[0].split("git revision ")[-1].replace('"', "")
        )
        cleaned -= set(git_revision)

        # filter out git url
        git_url = [el for el in cleaned if el.startswith("git URL")]
        misc_dict["git_url"] = git_url[0].split("git URL ")[-1].replace('"', "")
        cleaned -= set(git_url)

        # filter out version
        version = [el for el in cleaned if el.startswith("Version")]
        misc_dict["version"] = str(version[0].split("Version ")[-1])
        cleaned -= set(version)

        git_branch = [el for el in cleaned if el.startswith("git branch")]
        misc_dict["git_branch"] = (
            git_branch[0].split("git branch ")[-1].replace('"', "")
        )
        cleaned -= set(git_branch)

        build = [el for el in cleaned if el.startswith("Build")]
        misc_dict["build"] = build[0].split("Build: ")[-1].replace('"', "")
        cleaned -= set(build)

        email = [el for el in cleaned if el.startswith("Email")]
        misc_dict["email"] = email[0].split("Email ")[-1].split(",")
        cleaned -= set(email)

        other_items = {el for el in cleaned if " is " in el}
        cleaned -= other_items

        for el in other_items:
            split = el.split(" is ")
            key = split[0].strip()
            val = " is ".join(split[1:]).strip()
            if key in misc_dict:
                misc_dict[key + " (alt)"] = val
            else:
                misc_dict[key] = val

        misc_dict["uncaught"] = list(cleaned)

        version_info_dict["miscellaneous"] = misc_dict if misc_dict else None
        return version_info_dict

    def minimum_stellar_mass(self):
        """
        Function to return the minimum stellar mass (in Msun) from binary_c.
        """

        if not hasattr(self, "_minimum_stellar_mass"):
            self._minimum_stellar_mass = self.return_binary_c_version_info(parsed=True)[
                "macros"
            ]["BINARY_C_MINIMUM_STELLAR_MASS"]
        return self._minimum_stellar_mass
