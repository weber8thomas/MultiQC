#!/usr/bin/env python

""" MultiQC module to parse output from Samblaster """

from __future__ import print_function
import os
from collections import OrderedDict
import logging
import re
from multiqc import config, BaseMultiqcModule

# Initialise the logger
log = logging.getLogger(__name__)


class MultiqcModule(BaseMultiqcModule):
    """ Samblaster """

    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='Samblaster', anchor='samblaster',
                                            href="https://github.com/GregoryFaust/samblaster",
                                            info="is a tool to mark duplicates and extract discordant and split reads from sam files.")

        self.sections = list()
        self.samblaster_data = dict()
        for f in self.find_log_files(config.sp['samblaster'], filehandles=True):
            self.parse_samblaster(f)
        if len(self.samblaster_data) == 0:
            log.debug("Could not find any data in {}".format(config.analysis_dir))
            raise UserWarning

        headers = OrderedDict()
        headers['pct_dups'] = {
            'title': '% Dups',
            'description': 'Percent Duplication',
            'max': 100,
            'min': 0,
            'scale': 'OrRd',
            'format': '{:.1f}%'
        }

        self.general_stats_addcols(self.samblaster_data, headers)

        # Write parsed report data to a file
        self.write_data_file(self.samblaster_data, 'multiqc_samblaster')

        log.info("Found {} reports".format(len(self.samblaster_data)))

        self.add_barplot()

    def add_barplot(self):
        cats = OrderedDict()
        cats['n_nondups'] = {'name': 'Non-duplicates'}
        cats['n_dups'] = {'name': 'Duplicates'}

        pconfig = {
            'title': 'Number of duplicate reads',
        }
        # Only one section, so add to the intro
        self.intro += self.plot_bargraph(self.samblaster_data, cats, pconfig)

    def parse_samblaster(self, f):
        """ Go through log file looking for samblaster output.
        If the
        Grab the name from the RG tag of the preceding bwa command """
        dups_regex = "samblaster: (Removed|Marked) (\d+) of (\d+) \((\d+.\d+)%\) read ids as duplicates"
        input_file_regex = "samblaster: Opening (\S+) for read."
        rgtag_name_regex = "\\\\tSM:(\S*?)\\\\t"
        data = {}
        s_name = None
        fh = f['f']
        for l in fh:
            # try to find name from RG-tag. If bwa mem is used upstream samblaster with pipes, then the bwa mem command
            # including the read group will be written in the log
            match = re.search(rgtag_name_regex, l)
            if match:
                s_name = match.group(1)

            # try to find name from the input file name, if used
            match = re.search(input_file_regex, l)
            if match:
                basefn = os.path.basename(match.group(1))
                fname, ext = os.path.splitext(basefn)
                # if it's stdin, then try bwa RG-tag instead
                if fname != 'stdin':
                    s_name = fname

            match = re.search(dups_regex, l)
            if match:
                data['n_dups'] = int(match.group(2))
                data['n_tot'] = int(match.group(3))
                data['n_nondups'] = data['n_tot'] - data['n_dups']
                data['pct_dups'] = float(match.group(4))

        if s_name is not None:
            self.add_data_source(f, s_name)
            self.samblaster_data[s_name] = data
