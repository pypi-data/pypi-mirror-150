#!/usr/bin/env python

import os, sys
import shlex
import argparse
import logging
from typing import Dict, List, Union

logger = logging.getLogger(__name__)

__version__ = "v2.2"


# Infix class based on https://code.activestate.com/recipes/384122/
# Originally licensed under the PSF License
class Infix:
    def __init__(self, function):
        self.function = function

    def __or__(self, other):
        return self.function(other)

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __truediv__(self, other):
        return self.function(other)

    def __rtruediv__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __call__(self, value1, value2):
        return self.function(value1, value2)


# functions for implementing VHDL operators in python for evaluating statements
# relational
r_eq = Infix(lambda x, y: x == y)
r_neq = Infix(lambda x, y: x != y)
r_lt = Infix(lambda x, y: x < y)
r_leq = Infix(lambda x, y: x <= y)
r_gt = Infix(lambda x, y: x > y)
r_geq = Infix(lambda x, y: x >= y)
# logical
l_and = Infix(lambda x, y: x and y)
l_or = Infix(lambda x, y: x or y)
l_nand = Infix(lambda x, y: not (x and y))
l_nor = Infix(lambda x, y: not (x or y))
l_xor = Infix(lambda x, y: x != y)
l_xnor = Infix(lambda x, y: x == y)


class VHDLproc:
    _tool_name = "VHDLproc"
    _version = __version__
    _directives = [
        "`warning",
        "`error",
        "`if",
        "`elsif",
        "`else",
        "`end",
        "`include",
        "`define",
    ]
    _comment_char = "-- "

    def _eval(self, statement: str, identifiers: Dict[str, str]):

        statement = statement.lower()

        operators = (
            "=",
            "/=",
            "<",
            "<=",
            ">",
            ">=",
            "and",
            "or",
            "nand",
            "nor",
            "xor",
            "xnor",
        )

        for name in statement.replace("(", " ").replace(")", " ").split(" "):
            if (
                name not in identifiers
                and name not in operators
                and "'" not in name
                and '"' not in name
            ):
                logger.warning(f"Setting empty identifier {name}")
                identifiers[name] = ""

        # replacing VHDL operators with Python ones to preserve VHDL
        # operator precedence, / has higher precedence than |
        statement = statement.replace(" = ", " /r_eq/ ")
        statement = statement.replace(" /= ", " /r_neq/ ")
        statement = statement.replace(" < ", " /r_lt/ ")
        statement = statement.replace(" <= ", " /r_leq/ ")
        statement = statement.replace(" > ", " /r_gt/ ")
        statement = statement.replace(" >= ", " /r_geq/ ")

        statement = statement.replace(" and ", " |l_and| ")
        statement = statement.replace(" or ", " |l_or| ")
        statement = statement.replace(" nand ", " |l_nand| ")
        statement = statement.replace(" nor ", " |l_nor| ")
        statement = statement.replace(" xor ", " |l_xor| ")
        statement = statement.replace(" xnor ", " |l_xnor| ")

        for id in identifiers:
            locals()[id] = identifiers[id]

        logger.debug(f"Evaluating statement {statement}: {eval(statement)}")

        return eval(statement)

    def parse_file(self, file: str, identifiers: Dict[str, str] = {}) -> str:
        """Reads and parses a file

        Args:
            file (str): Path to file to parse
            identifiers (Dict[str, str], optional): Identifiers to use. Defaults to {}.

        Returns:
            str: Parsed code from file
        """

        with open(file) as f:
            code = f.read().splitlines()

        include_path = "/".join(file.split("/")[:-1]) + "/"

        return self.parse(code, identifiers, include_path=include_path)

    def parse(
        self,
        code: Union[List[str], str],
        identifiers: Dict[str, str] = {},
        include_path: str = "./",
    ) -> str:
        """Steps through each line of the code, finds, and executes preprocessing statements, commenting them out once finished

        Args:
            code (Union[List[str], str]): Source code as a string or list of strings split by line
            identifiers (Dict[str, str], optional): Identifiers. Defaults to {}.
            include_path (str, optional): Path to pull include files from. Defaults to "./".

        Raises:
            Exception: Unknown directive
            Exception: `warning directive requires a message
            Exception: `error directive requires a message
            Exception: `define directive requires a label and value
            Exception: `if directive requires a then
            Exception: `elsif directive requires a then
            Exception: Missing `end [ if ]

        Returns:
            str: Parsed code
        """
        if isinstance(code, str):
            code = code.splitlines()

        identifiers["TOOL_NAME"] = self._tool_name
        identifiers["TOOL_VERSION"] = self._version
        if "VHDL_VERSION" not in identifiers:
            identifiers["VHDL_VERSION"] = ""
        if "TOOL_TYPE" not in identifiers:
            identifiers["TOOL_TYPE"] = ""
        if "TOOL_VENDOR" not in identifiers:
            identifiers["TOOL_VENDOR"] = ""
        if "TOOL_EDITION" not in identifiers:
            identifiers["TOOL_EDITION"] = ""

        identifiers = {
            key.lower(): value.lower() for (key, value) in identifiers.items()
        }

        ifstack = [[True, False]]
        line_i = -1

        while line_i < len(code) - 1:
            line_i = line_i + 1
            line = code[line_i].split("--")[0]  # ignore comments

            if len(line.strip()) == 0:  # skip empty lines
                continue

            if "`" == line.strip()[0]:  # if this line is a directive

                # https://stackoverflow.com/a/79985
                # remove blank space and split words into a list
                # don't separate quotes
                directive = shlex.split(line.strip(), posix=False)
                code[line_i] = self._comment_char + code[line_i]

                directive[0] = directive[0].lower()

                if ifstack[-1][0]:
                    # if it's not a supported directive
                    if directive[0] not in self._directives:
                        raise Exception(
                            f"Line {line_i+1}: Unknown directive: {line.strip().split(' ')[0]}"
                        )

                    # print warning messages if not commented out
                    elif directive[0] == "`warning":
                        if len(directive) < 2:
                            raise Exception(
                                f"Line {line_i+1}: `warning directive requires a message"
                            )
                        warning_message = directive[1][1:-1]
                        logger.warning(f"Line {line_i+1}: {warning_message}")

                    # print error messages if not commented out
                    elif directive[0] == "`error":
                        if len(directive) < 2:
                            raise Exception(
                                f"Line {line_i+1}: `error directive requires a message"
                            )
                        error_message = directive[1][1:-1]
                        logger.error(f"Line {line_i+1}: Error: {error_message}")
                        exit(1)

                    # open file and append source code at this location
                    elif directive[0] == "`include":
                        filename = include_path + " ".join(directive[1:])[1:-1]
                        include = []
                        for incl_line in open(filename):
                            include.append(incl_line.rstrip("\n"))
                        code = code[: line_i + 1] + include + code[line_i + 1 :]

                    elif directive[0] == "`define":
                        if len(directive) != 3:
                            raise Exception(
                                f"Line {line_i+1}: `define directive requires a label and value"
                            )
                        identifiers[directive[1].lower()] = directive[2].lower()[1:-1]

                if directive[0] == "`if":
                    if directive[-1] != "then":
                        raise Exception(
                            f"Line {line_i+1}: `if directive requires a then"
                        )
                    if ifstack[-1][0]:
                        resp = self._eval(" ".join(directive[1:-1]), identifiers)
                        ifstack.append([resp, resp])
                    else:
                        ifstack.append([False, True])

                elif directive[0] == "`elsif":
                    if directive[-1] != "then":
                        raise Exception(
                            f"Line {line_i+1}: `elsif directive requires a then"
                        )
                    resp = self._eval(" ".join(directive[1:-1]), identifiers)
                    ifstack[-1][0] = not ifstack[-1][1] and resp
                    ifstack[-1][1] = ifstack[-1][1] or resp

                elif directive[0] == "`else":
                    if ifstack[-2][0]:
                        ifstack[-1][0] = not ifstack[-1][1]

                elif directive[0] == "`end":
                    ifstack.pop()

            # don't comment out lines that are already commented out
            if not ifstack[-1][0] and code[line_i].strip()[:2] != "--":
                code[line_i] = self._comment_char + code[line_i]

            # logging.debug(f'ifstack: {ifstack}')

        if len(ifstack) > 1:
            raise Exception(f"Line {line_i+1}: Missing `end [ if ]")

        return "\n".join(code)


def test_file(name: str, identifiers: Dict[str, str] = {}) -> bool:
    """Runs a built-in test to verify functionality

    Args:
        name (str): Name of the test
        identifiers (Dict[str,str], optional): Identifiers to pass into the files. Defaults to {}.

    Returns:
        bool: Whether the test passed or failed
    """
    logging.info(f"\n== Testing {name} ==")
    proc = VHDLproc()
    filename = os.path.dirname(__file__) + f"/tests/{name}.vhdl"
    passed = True

    try:
        proc.parse_file(filename, identifiers=identifiers)
    except Exception as e:
        logging.error(e)
        logging.error("Test Failed")
        passed = passed and False

    if passed:
        logging.info("== Passed ==")
    else:
        logging.info("== Failed ==")

    return passed


def test_all(identifiers: Dict[str, str]):
    """Runs the 'include', 'and', and 'nest' tests

    Returns:
        bool: Whether the tests passed or failed
    """
    return not (
        test_file("include", identifiers)
        and test_file("and", identifiers)
        and test_file("nest", identifiers)
    )


def _cli():
    parser = argparse.ArgumentParser(
        description=f"VHDLproc {__version__} - VHDL Preprocessor"
    )
    parser.add_argument(
        "input",
        nargs="*",
        help="Input files (will skip over files with the output extension)",
    )
    parser.add_argument(
        "-D",
        action="append",
        metavar="IDENTIFIER=value",
        help="Specify identifiers for conditional compilation, ex. DEBUG_LEVEL=2",
    )
    parser.add_argument(
        "-o",
        metavar="DIRECTORY",
        help="Directory to store parsed files",
    )
    parser.add_argument(
        "-e",
        metavar="EXTENSION",
        default=".proc.vhdl",
        help="Output extension for processed files (defaults to '.proc.vhdl')",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run a self-test to ensure functionality",
    )
    parser.add_argument(
        "--log-level",
        metavar="LEVEL",
        default=logging.INFO,
        type=(lambda x: getattr(logging, x)),
        help="Configure the logging level",
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level, format="%(levelname)s: %(message)s")

    identifiers = (
        {id.split("=")[0]: str(id.split("=")[1]) for id in args.D} if args.D else {}
    )

    if args.self_test:
        test_all(identifiers)
        return

    if not os.path.exists(args.temp_dir):
        os.makedirs(args.temp_dir)

    proc = VHDLproc()
    for file in args.input:
        if file.endswith(args.extension):
            logging.debug(f"Skipping file {file}")
            continue

        if args.out_dir is not None:
            newfile = os.path.join(
                args.out_dir,
                os.path.splitext(os.path.basename(file))[0] + args.extension,
            )
        else:
            newfile = os.path.splitext(file)[0] + args.extension

        print(newfile)

        logging.debug(f"Parsing file {file} to {newfile}")

        parsed_code = proc.parse_file(file, identifiers=identifiers)
        with open(newfile, "w") as f:
            f.write(parsed_code)


if __name__ == "__main__":
    _cli()
