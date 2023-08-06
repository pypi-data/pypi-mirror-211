"""csvsheet - A simple CSV calculator.

This module and command line application allows to perform calculations on CSV files.
It is not intended to be a full spreadsheet replacement,
but rather a simple tool to perform basic math operations on CSV files.
The main reason is that CSV is far friendlier to version control systems
than binary formats like XLSX.

"""

import argparse
import csv
import logging
import math
import re
import sys

from csvsheet import __version__

ALLOWED_NAMES = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

__author__ = "Jesús Lázaro"
__copyright__ = "Jesús Lázaro"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from csvsheet.csvsheet import sanitize_cell`,
# when using this Python module as a library.


def sanitize_cell(cell: str, mathdelimiter: str = "=") -> str:
    """Sanitize a cell.

    Args:
    -----
        cell (str): string from CSV cell
        mathdelimiter (str, optional): delimiter to identify formulas. Defaults to "=".

    Raises:
    -------
        ValueError: cell contains invalid functions

    Returns:
    --------
        str: Sanitized string to be used in eval()
    """
    if cell.startswith(mathdelimiter):
        # formula!!!
        # remove the '='
        cell = cell[1:]
        # eliminate all spaces
        cell = cell.replace(" ", "")
        # eliminate everything after a comment (#)
        cell = cell.split("#")[0]
        # sanitize the input
        cell_copy = cell
        # delete all numbers using regex
        cell_copy = re.sub(r"\d*\.?\d+", "", cell_copy)
        # delete all math.xxx using regex
        cell_copy = re.sub(r"math\.\w+", "", cell_copy)
        # delete all castings using regex
        cell_copy = re.sub(r"int\(|float\(", "", cell_copy)
        # delete all operators using regex
        cell_copy = re.sub(r"\+|\-|\*|\/|\(|\)|\,", "", cell_copy)
        # if cell_copy is not empty, error
        if cell_copy != "":
            # error
            msg = f"Error: formula contains invalid characters: {cell_copy}"
            raise ValueError(msg)
        cell = eval(cell)

    else:
        # text
        pass
    return cell


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args: list[str]) -> argparse.Namespace:
    """Parse command line parameters.

    Args:
    -----
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
    --------
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    # add input file as positional argument
    parser.add_argument(
        "input",
        help="Input CSV file to read. '-' for stdin",
        type=argparse.FileType("r"),
        metavar="INPUT_FILE",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"csvsheet {__version__}",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Output file to write result, if none given, \
            it will be writen to stdout",
        default="-",
        type=argparse.FileType("w"),
        metavar="OUTPUT_FILE",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        dest="delimiter",
        help="CSV file delimiter, default is ','",
        type=str,
        default=",",
        metavar="DELIMITER",
    )
    parser.add_argument(
        "-q",
        "--quotechar",
        dest="quotechar",
        help="CSV file quote char, default is '\"'",
        type=str,
        default='"',
        metavar="QUOTECHAR",
    )
    parser.add_argument(
        "-m",
        "--math",
        dest="mathdelimiter",
        help="start char for formulas, default is '='",
        type=str,
        default="=",
        metavar="MATH_DELIMITER",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel: int):
    """Setup basic logging.

    Args:
    -----
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args: list[str]):
    """Deals with command line parameters and input/output.

    Args:
    -----
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args_parsed = parse_args(args)
    setup_logging(args_parsed.loglevel)

    _logger.info(f"Starting csvsheet calculation: {args_parsed}")

    # create delimiter and quotechar
    delimiter = args_parsed.delimiter
    quotechar = args_parsed.quotechar

    # open reader
    csvreader = csv.reader(args_parsed.input, delimiter=delimiter, quotechar=quotechar)
    # open writer
    fh = args_parsed.output
    csvwriter = csv.writer(fh, delimiter=delimiter, quotechar=quotechar)
    # loop
    for row_idx, row in enumerate(csvreader):
        # loop
        for (
            col_idx,
            cell,
        ) in enumerate(row):
            # sanitize cell
            _logger.debug(f" original cell: {cell}")
            try:
                cell = sanitize_cell(cell, args_parsed.mathdelimiter)
            except ValueError as e:
                _logger.info(f"row {row_idx} col {col_idx}: {cell}")
                _logger.error(e)
                sys.exit(1)
            except SyntaxError as e:
                _logger.info(f"row {row_idx} col {col_idx}: {cell}")
                _logger.error(e)
                sys.exit(1)

            _logger.debug(f"sanitized cell: {cell}")
            # update row
            row[col_idx] = cell
        # write row
        csvwriter.writerow(row)
    # close reader
    args_parsed.input.close()
    # close writer
    if args_parsed.output != sys.stdout:
        fh.close()

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`.

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m csvsheet.skeleton 42
    #
    run()
