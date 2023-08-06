"""
The class extension for the population object that contains logging functionality

TODO: move these functions to the grid sampling subclass
"""

# pylint: disable=E1101

import time

import strip_ansi

from binarycpython.utils.functions import format_number, trem
from binarycpython.utils.population_extensions.population_options_defaults import (
    secs_per_day,
)


class grid_logging:
    """
    The class extension for the population object that contains logging functionality
    """

    def __init__(self, **kwargs):
        """
        Init function for the grid_logging class
        """

        return

    def _print_info(self, run_number, total_systems, full_system_dict):
        """
        Function to print info about the current system and the progress of the grid.

        # color info tricks from https://ozzmaker.com/add-colour-to-text-in-python/
        https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
        """

        # Define frequency
        if self.population_options["verbosity"] == 1:
            print_freq = 1
        else:
            print_freq = 10

        if run_number % print_freq == 0:
            binary_cmdline_string = self._return_argline(full_system_dict)
            info_string = "{color_part_1} \
            {text_part_1}{end_part_1}{color_part_2} \
            {text_part_2}{end_part_2}".format(
                color_part_1="\033[1;32;41m",
                text_part_1="{}/{}".format(run_number, total_systems),
                end_part_1="\033[0m",
                color_part_2="\033[1;32;42m",
                text_part_2="{}".format(binary_cmdline_string),
                end_part_2="\033[0m",
            )
            self.vb_info(info_string)

    ######################
    # Status logging

    def vb1print(self, ID, now, system_number, system_dict):
        """
        Verbosity-level 1 printing, to keep an eye on a grid.

        Input:
            ID: thread ID for debugging (int): TODO fix this
            now: the time now as a UNIX-style epoch in seconds (float)
            system_number: the system number
        """

        # calculate estimated time of arrive (eta and eta_secs), time per run (tpr)
        localtime = time.localtime(now)

        # calculate stats
        n = self.shared_memory["n_saved_log_stats"].value
        if n < 2:
            # simple 1-system calculation: inaccurate
            # but best for small n
            dt = now - self.shared_memory["prev_log_time"][0]
            dn = system_number - self.shared_memory["prev_log_system_number"][0]
        else:
            # average over n_saved_log_stats
            dt = (
                self.shared_memory["prev_log_time"][0]
                - self.shared_memory["prev_log_time"][n - 1]
            )
            dn = (
                self.shared_memory["prev_log_system_number"][0]
                - self.shared_memory["prev_log_system_number"][n - 1]
            )

        eta, units, tpr, eta_secs = trem(
            dt, system_number, dn, self.population_options["_total_starcount"]
        )

        # compensate for multithreading and modulo
        tpr *= (
            self.population_options["_num_processes"]
            * self.population_options["modulo"]
        )

        if eta_secs < secs_per_day:
            fintime = time.localtime(now + eta_secs)
            etf = "{hours:02d}:{minutes:02d}:{seconds:02d}".format(
                hours=fintime.tm_hour, minutes=fintime.tm_min, seconds=fintime.tm_sec
            )
        else:
            d = int(eta_secs / secs_per_day)
            if d == 1:
                etf = "Tomorrow"
            else:
                etf = "In {} days".format(d)

        # modulo information
        if self.population_options["modulo"] == 1:
            modulo = ""  # usual case
        else:
            modulo = "%" + str(self.population_options["modulo"])

        # add up memory use from each thread
        total_mem_use = sum(self.shared_memory["memory_use_per_thread"])

        # make a string to describe the system e.g. M1, M2, etc.
        system_string = ""

        # use the multiplicity if given
        if "multiplicity" in system_dict:
            nmult = int(system_dict["multiplicity"])
        else:
            nmult = 4

        # masses
        for i in range(nmult):
            i1 = str(i + 1)
            if "M_" + i1 in system_dict:
                system_string += (
                    "M{}=".format(i1) + format_number(system_dict["M_" + i1]) + " "
                )

        # separation and orbital period
        if "separation" in system_dict:
            system_string += "a=" + format_number(system_dict["separation"])
        if "orbital_period" in system_dict:
            system_string += "P=" + format_number(system_dict["orbital_period"])

        # do the print
        if self.population_options["_total_starcount"] > 0:
            self.vb_critical(
                "\n{opening_colour}{system_number}/{total_starcount}{modulo} {pc_colour}{pc_complete:5.1f}% complete {time_colour}{hours:02d}:{minutes:02d}:{seconds:02d} {ETA_colour}ETA={ETA:7.1f}{units} tpr={tpr:2.2e} {ETF_colour}ETF={ETF} {mem_use_colour}mem:{mem_use:.1f}MB {system_string_colour}{system_string}{closing_colour}".format(
                    opening_colour=self.ANSI_colours["reset"]
                    + self.ANSI_colours["yellow on black"],
                    system_number=system_number,
                    total_starcount=self.population_options["_total_starcount"],
                    modulo=modulo,
                    pc_colour=self.ANSI_colours["blue on black"],
                    pc_complete=(100.0 * system_number)
                    / (1.0 * self.population_options["_total_starcount"])
                    if self.population_options["_total_starcount"]
                    else -1,
                    time_colour=self.ANSI_colours["green on black"],
                    hours=localtime.tm_hour,
                    minutes=localtime.tm_min,
                    seconds=localtime.tm_sec,
                    ETA_colour=self.ANSI_colours["red on black"],
                    ETA=eta,
                    units=units,
                    tpr=tpr,
                    ETF_colour=self.ANSI_colours["blue"],
                    ETF=etf,
                    mem_use_colour=self.ANSI_colours["magenta"],
                    mem_use=total_mem_use,
                    system_string_colour=self.ANSI_colours["yellow"],
                    system_string=system_string,
                    closing_colour=self.ANSI_colours["reset"],
                ),
            )
        else:
            self.vb_critical(
                "\n{opening_colour}{system_number}{modulo} {time_colour}{hours:02d}:{minutes:02d}:{seconds:02d} tpr={tpr:2.2e} {mem_use_colour}mem:{mem_use:.1f}MB {system_string_colour}{system_string}{closing_colour}".format(
                    opening_colour=self.ANSI_colours["reset"]
                    + self.ANSI_colours["yellow on black"],
                    system_number=system_number,
                    modulo=modulo,
                    time_colour=self.ANSI_colours["green on black"],
                    hours=localtime.tm_hour,
                    minutes=localtime.tm_min,
                    seconds=localtime.tm_sec,
                    tpr=tpr,
                    mem_use_colour=self.ANSI_colours["magenta"],
                    mem_use=total_mem_use,
                    system_string_colour=self.ANSI_colours["yellow"],
                    system_string=system_string,
                    closing_colour=self.ANSI_colours["reset"],
                ),
            )

    def vb2print(self, system_dict, cmdline_string):
        """
        Extra function for verbose printing
        """

        self.vb_info(
            "Running this system now on thread {ID}\n{blue}{cmdline}{reset}:\n\t{system_dict}\n".format(
                ID=self.process_ID,
                blue=self.ANSI_colours["blue"],
                cmdline=cmdline_string,
                reset=self.ANSI_colours["reset"],
                system_dict=system_dict,
            )
        )

    def _boxed(
        self, *stringlist, colour="yellow on black", boxchar="*", separator="\n"
    ):
        """
        Function to output a list of strings in a single box.

        Args:
            list = a list of strings to be output. If these contain the separator
                   (see below) these strings are split by it.
            separator = strings are split on this, default "\n"
            colour = the colour to be used, usually this is 'yellow on black'
                     as set in the ANSI_colours dict
            boxchar = the character used to make the box, '*' by default

        Note: handles tabs (\t) badly, do not use them!
        """
        strlen = 0
        strings = []
        lengths = []

        # make a list of strings
        if separator:
            for string in stringlist:
                strings += string.split(sep=separator)
        else:
            strings = stringlist

        # get lengths without ANSI codes
        for string in strings:
            lengths.append(len(strip_ansi.strip_ansi(string)))

        # hence the max length
        strlen = max(lengths)
        strlen += strlen % 2
        header = boxchar * (4 + strlen)

        # start output
        out = self.ANSI_colours[colour] + header + "\n"

        # loop over strings to output, padding as required
        for n, string in enumerate(strings):
            if lengths[n] % 2 == 1:
                string = " " + string
            pad = " " * int((strlen - lengths[n]) / 2)
            out = out + boxchar + " " + pad + string + pad + " " + boxchar + "\n"

        # close output and return
        out = out + header + "\n" + self.ANSI_colours["reset"]
        return out
