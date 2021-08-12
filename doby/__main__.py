"""Doby main function"""
import os
import sys
import subprocess
import argparse
from doby import Doby
from doby.utils import (
    write_list_to_file,
    clear_export_directory,
)


def parse_args(args):
    """Parse the arguments"""
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group("Optional arguments")
    parser.add_argument("config", help="Path to the configuration JSON file")
    parser.add_argument("output", help="Directory to write the file to")
    optional.add_argument(
        "-v", type=bool, help="Enables verbose output", nargs="?", const=True
    )
    parsed_args = parser.parse_args(args)

    return parsed_args


def yapf(args):
    """Format with yapf"""
    print("Formatting with YAPF")
    try:
        subprocess.run(["yapf", "--recursive", "-i", args.output], check=True)
    except subprocess.CalledProcessError:
        print("YAPF: Error with output file, please check the log above")
        sys.exit(1)


def black(args, lib_name):
    """Format with black"""
    print("Formatting with Black")
    try:
        subprocess.run(
            ["black", "--fast", f"{args.output}/{lib_name}/{lib_name}.py"],
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Black: Error with output file, please check the log above")
        sys.exit(2)


def test_compile(args, lib_name):
    """Test file compile"""
    print("Checking it compiles")
    try:
        subprocess.run(
            [
                "python3",
                "-m",
                "py_compile",
                f"{args.output}/{lib_name}/{lib_name}.py",
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Unable to compile code, check the output file")
        sys.exit(3)
    print("Done 🦈🪄")


def main(args):
    """Main build and write function"""

    doby = Doby(config_filename=args.config, debug=args.v)

    lib_name = doby.get_name()

    print(f"Creating export dir: {args.output}")
    clear_export_directory(args.output)
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    if not os.path.isdir(f"{args.output}/{lib_name}"):
        os.mkdir(f"{args.output}/{lib_name}")

    # TODO add version pinning support for config

    print(f"Building {lib_name}")

    all_files = doby.build_file()

    print(f"Writing files for {lib_name}")
    for write_filename in all_files:
        write_list_to_file(write_filename, args.output, all_files[write_filename])

    yapf(args)

    black(args, lib_name)

    test_compile(args, lib_name)

    return True


def init():
    """Run main"""
    if __name__ == "__main__":
        main(parse_args(sys.argv[1:]))


init()
