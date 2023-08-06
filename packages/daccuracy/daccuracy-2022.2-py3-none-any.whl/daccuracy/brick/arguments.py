# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import re as rgex
import sys as sstm
from argparse import ArgumentParser as argument_parser_t
from argparse import Namespace as namespace_t
from argparse import RawDescriptionHelpFormatter
from pathlib import Path as path_t
from typing import Optional, Sequence, Tuple

import __main__ as main_package

import daccuracy.brick.csv_io as csio
import daccuracy.brick.measures as msrs
import daccuracy.brick.output as otpt
from daccuracy.brick.csv_io import row_transform_h
from daccuracy.brick.measures import measure_fct_h


USAGE_NOTICE = """
With 8-bit image formats, ground-truth and detection cannot contain more than 255 objects. If they do, they could be
saved using higher-depth formats. However, it is recommended to save them in NPY or NPZ Numpy formats instead.
"""

DACCURACY_DESCRIPTION = f"""3 modes:
    - one-to-one: one ground-truth (csv, image, or Numpy array) vs. one detection (image or Numpy array)
    - one-to-many: one ground-truth vs. several detections (folder of detections)
    - many-to-many: several ground-truths (folder of ground-truths) vs. corresponding detections (folder of detections)

In many-to-many mode, each detection file must have a counterpart ground-truth file with the same name, but not
necessarily the same extension.

{USAGE_NOTICE}
"""


def ProcessedArguments(
    arguments: Sequence[str], /
) -> Tuple[
    path_t,
    Optional[str],
    path_t,
    Optional[str],
    measure_fct_h,
    Optional[Sequence[int]],
    Optional[row_transform_h],
    namespace_t,
]:
    """"""
    parser = _ArgumentParser()
    std_args, other_args = parser.parse_known_args(arguments)

    ground_truth_path = path_t(std_args.ground_truth_path)
    detection_path = path_t(std_args.detection_path)
    if not (ground_truth_path.is_file() or ground_truth_path.is_dir()):
        print(f"{ground_truth_path}: Not a file or folder", file=sstm.stderr)
        sstm.exit(-1)
    if not (detection_path.is_file() or detection_path.is_dir()):
        print(f"{detection_path}: Not a file or folder", file=sstm.stderr)
        sstm.exit(-1)
    if detection_path.is_file() and not ground_truth_path.is_file():
        print(
            f"{ground_truth_path}: Not a file while detection is a file",
            file=sstm.stderr,
        )
        sstm.exit(-1)

    if (other_args.__len__() > 0) and (
        (other_args[0] == __file__)
        or (path_t(other_args[0]).resolve() == path_t(main_package.__file__).resolve())
    ):
        other_args = other_args[1:]

    if other_args.__len__() > 1:
        print("Too many arguments", file=sstm.stderr)
        parser.print_help()
        sstm.exit(-1)

    coordinate_idc = row_transform = None
    if other_args.__len__() > 0:
        in_mode = "csv"
        coordinate_idc, row_transform = _CoordinateIndices(other_args[0], parser)
    elif ground_truth_path.suffix.lower() == ".csv":
        in_mode = "csv"
        row_transform = lambda f_idx: f_idx
    else:
        in_mode = "map"

    if in_mode == "csv":
        measure_fct = msrs.StandardMeasures
    else:
        measure_fct = msrs.ExtendedMeasures

    return (
        ground_truth_path,
        std_args.relabel_gt,
        detection_path,
        std_args.relabel_dn,
        measure_fct,
        coordinate_idc,
        row_transform,
        std_args,
    )


def _CoordinateIndices(
    option: str, parser: argument_parser_t, /
) -> Tuple[Sequence[int], Optional[row_transform_h]]:
    """"""
    match = rgex.match("--([rx])([A-Z]+)([cy])([A-Z]+)", option)

    if match is None:
        print(f"{option}: Invalid option", file=sstm.stderr)
        parser.print_help()
        sstm.exit(-1)

    if match.group(1) == "r":
        if match.group(3) != "c":
            print(f'{option}: "r"/"y" mixing', file=sstm.stderr)
            sstm.exit(-1)

        row_idx = csio.ColLabelToIdx(match.group(2))
        col_idx = csio.ColLabelToIdx(match.group(4))
        row_transform = lambda f_idx: f_idx
    #
    else:
        if match.group(3) != "y":
            print(f'{option}: "x"/"c" mixing', file=sstm.stderr)
            sstm.exit(-1)

        row_idx = csio.ColLabelToIdx(match.group(4))
        col_idx = csio.ColLabelToIdx(match.group(2))
        # This will later be changed into a symmetrization transform for each image
        row_transform = None

    remaining = option[match.end() :]
    matches = rgex.findall("\+[A-Z]+", remaining)
    if "".join(matches) != remaining:
        print(f"{option}: Invalid option", file=sstm.stderr)
        parser.print_help()
        sstm.exit(-1)

    coordinate_idc = [row_idx, col_idx]
    for match in matches:
        coordinate_idc.append(csio.ColLabelToIdx(match[1:]))

    return coordinate_idc, row_transform


def _ArgumentParser() -> argument_parser_t:
    """"""
    output = argument_parser_t(
        prog=path_t(main_package.__file__).stem,
        description=DACCURACY_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )

    output.add_argument(
        "--gt",
        type=str,
        required=True,
        dest="ground_truth_path",
        metavar="ground_truth",
        help="Ground-truth CSV file of centers or labeled image or labeled Numpy array, or ground-truth folder; "
        "If CSV, --rAcB (or --xAyB) can be passed additionally "
        "to indicate that columns A and B contain the centers' "
        "rows and cols, respectively (or x's and y's in x/y mode). "
        'Columns must be specified as (possibly "words" of) uppercase letters, '
        'as is usual in spreadsheet applications. For ground-truths of dimension "n" higher than 2, '
        'the symbol "+" must be used for the remaining "n-2" dimensions. For example, --rAcB+C+D in dimension 4.',
    )
    output.add_argument(
        "--relabel-gt",
        type=str,
        choices=("seq", "full"),
        default=None,
        dest="relabel_gt",
        help="If present, this option instructs to relabel the ground-truth sequentially.",
    )
    output.add_argument(
        "--dn",
        type=str,
        required=True,
        dest="detection_path",
        metavar="detection",
        help="Detection labeled image or labeled Numpy array, or detection folder.",
    )
    output.add_argument(
        "--relabel-dn",
        type=str,
        choices=("seq", "full"),
        default=None,
        dest="relabel_dn",
        help="If present, this option instructs to relabel the detection sequentially.",
    )
    output.add_argument(
        "--shifts",
        type=int,
        nargs="+",
        action="extend",
        default=None,
        dest="dn_shifts",
        metavar="Dn_shift",
        help="Vertical (row), horizontal (col), and higher dimension shifts to apply to detection. "
        "Default: all zeroes.",
    )
    output.add_argument(
        "-e",
        "--exclude-border",
        action="store_true",
        dest="should_exclude_border",
        help="If present, this option instructs to discard objects touching image border, "
        "both in ground-truth and detection.",
    )
    output.add_argument(
        "-t",
        "--tol",
        "--tolerance",
        type=int,
        default=0,
        dest="tolerance",
        help="Max ground-truth-to-detection distance to count as a hit "
        "(meant to be used when ground-truth is a CSV file of centers). Default: zero.",
    )
    output.add_argument(
        "-f",
        "--format",
        type=str,
        choices=("csv", "nev"),
        default="nev",
        dest="output_format",
        help='nev: one "Name = Value"-row per measure; '
        'csv: one CSV-row per ground-truth/detection pairs. Default: "nev".',
    )
    output.add_argument(
        "-o",
        type=otpt.OutputStream,  # Do not use the same approach with gt and dn since they can be folders
        default=sstm.stdout,
        dest="output_accessor",
        metavar="Output file",
        help='CSV file to store the computed measures or "-" for console output. Default: console output.',
    )
    output.add_argument(
        "-s",
        "--show-image",
        action="store_true",
        dest="should_show_image",
        help="If present, this option instructs to show an image "
        "superimposing ground-truth onto detection. It is actually done only for 2-dimensional images.",
    )
    output.add_argument(
        "--no-usage-notice",
        action="store_false",
        dest="should_show_usage_notice",
        help="Silences usage notice about maximum number of objects.",
    )

    return output
