#!/usr/bin/env python3
# Copyright (c) 2023 Krishna Miriyala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
import yaml


def parse_args():
    parser = argparse.ArgumentParser(
        description='Yaml to cli parames converter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--input-files', action='extend', nargs='+', default=[],
        help='Yaml configuration files in order of overrides')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    params = {}
    cli_params = ""

    for input_file in args.input_files:
        with open(input_file, encoding='UTF-8') as filep:
            data = yaml.safe_load(filep)
            for key, val in data.items():
                params[key] = val

    for key, value in params.items():
        cli_params += " "
        if len(key) == 1:
            cli_params += f"-{key}"
        else:
            cli_params += f"--{key}"
        if isinstance(value, list):
            cli_params += " ".join([f"\"{val}\"" for val in value])
        else:
            cli_params += f"{value}"
    print(cli_params)


if __name__ == '__main__':
    main()
