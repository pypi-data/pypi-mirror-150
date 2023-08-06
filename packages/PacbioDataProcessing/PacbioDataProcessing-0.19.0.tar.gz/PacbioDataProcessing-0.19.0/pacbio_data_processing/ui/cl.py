#######################################################################
#
# Copyright (C) 2021 David Palao
#
# This file is part of PacBio data processing.
#
#  PacBioDataProcessing is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PacBio data processing is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PacBioDataProcessing. If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

"""This module defines the functions to collect user input from the
command line."""

import argparse

from .options import SM_ANALYSIS_OPTS, BAM_FILTER_OPTS
from .common import parse_user_input
from ..constants import (
    SM_ANALYSIS_EXE, SM_ANALYSIS_DESC, BAM_FILTER_EXE, BAM_FILTER_DESC,
)

# import gooey

# def old_parse_cl():
#     parser.add_argument(
#         "-r", "--restart-from-old-dir", metavar="DIR", type=Path,
#         help=(
#             "continue analysis from a previous (unfinished) one; "
#             "%(metavar)s must be the temporary directory remaining from "
#             "the old run."
#         )
#     )


# @gooey.Gooey(menu=[
#     {
#         "name": "about",
#         "items": [
#             {
#                 'type': 'AboutDialog',
#                 'menuTitle': 'About',
#                 'name': 'sm-analysis (Pacbio Data Processing)',
#                 'description': 'Single Molecule Analysis of PacBio BAM files',
#                 'version': '0.16.0',
#                 'copyright': '2021',
#                 'website': 'https://gitlab.com/dvelazquez/pacbio-data-processing',
#                 'developer': 'Pancho viviente',
#                 'license': 'MOT'
#             }
#         ]
#     }],
#     default_size=(1024, 1024)
# )

def parse_cl_sm_analysis():
    return parse_user_input(
        argparse.ArgumentParser,
        SM_ANALYSIS_EXE, SM_ANALYSIS_DESC, SM_ANALYSIS_OPTS
    )


def parse_cl_bam_filter():
    return parse_user_input(
        argparse.ArgumentParser,
        BAM_FILTER_EXE, BAM_FILTER_DESC, BAM_FILTER_OPTS
    )
