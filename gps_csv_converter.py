"""Parses through a GPS CSV file and outputs a CSV file to the needed specifications"""
# Name: Trinten Patten
# Date: 5/24/2021
# For use in CILE-490: Interdisciplinary Capstone
# Version 2.1: Cleaned up code, error catching for the following: Importing, Reading in file, parsing of arguements
#              Changed Vel: 40 -> 5, Updated Help Tips, added in Velocity & Angle inputs
# Assumptions:
# Python Version: 3.9.1
# Dependencies: Pandas 1.2.4, utm 0.7.0
# Works with single CSV at a time

# Included Packages
import os
import argparse
import sys

# Need to be installed packages
module_list = ['numpy', 'pandas', 'utm']
try:
    import utm
    import numpy
    import pandas
except ModuleNotFoundError:
    not_in_list = ", ".join(x for x in module_list - sys.modules.keys())
    print(f"Module(s) {not_in_list} not installed correctly. Please install the required module(s) and run again")
    sys.exit()


def arg_parsing():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help=("Type: String\n"
                                                         "Def Value: N/A\n"
                                                         "Descr: Input file namepath with extension.\n"), required=True)
    parser.add_argument("-o", "--output", type=str, help=("Type: String\n"
                                                          "Def Value: N/A\n"
                                                          "Descr: Output filepath with extension.\n"), required=True)
    parser.add_argument("-m", "--mode", type=str, default="xyz", help=("Type: String\n"
                                                                       "Def Value: xyz\n"
                                                                       "Descr: Set to LLA for output to be in LLA fornmat.\n"))  # Mode Selection
    parser.add_argument("-w", "--waypoints", type=str, default=10, help=("Type: String | Int\n"
                                                                         "Def Value: 10\n"
                                                                         "Descr: Sets the number of waypoints created. All will use all points available.\n"))
    parser.add_argument("--header", type=str2bool, default=False, help=("Type: Boolean\n"
                                                                        "Def Value: False\n"
                                                                        "Descr: Set to True if there is a 13 row header, as seen with data from GPS.\n"))
    parser.add_argument("-t", "--tab", type=str2bool, default=False, help=("Type: Boolean\n"
                                                                           "Def Value: False\n"
                                                                           "Descr: Set to True if file is tab seperated (.tsv).\n"))
    parser.add_argument("-s", "--spaced", type=str2bool, default=False, help=("Type: Boolean\n"
                                                                              "Def Value: False\n"
                                                                              "Descr: Set to True for a blank space after every row in the output.\n"))  # Spaced Output file
    parser.add_argument("-r", "--rawoutput", type=str2bool, default=False, help=("Type: Boolean\n"
                                                                                 "Def Value: False\n"
                                                                                 "Descr: Set to True if you want the raw output.\n"))
    parser.add_argument("-n", "--normalize", type=str2bool, default=False, help=("Type: Boolean\n"
                                                                                 "Def Value: False\n"
                                                                                 "Descr: Set to True for normalized data.\n"))
    parser.add_argument("--normvalue", type=float, default=20.0, help=("Type: Float\n"
                                                                       "Def Value: 20.0\n"
                                                                       "Descr: If normalizing this is the number normalized to.\n"))
    parser.add_argument("-v", "--velocity", type=float, default=5.0, help=("Type: Float\n"
                                                                           "Def Value: 5.0\n"
                                                                           "Descr: Value that will be used for velocity.\n"))
    parser.add_argument("-a", "--angle", type=float, default=0.0, help=("Type: Float\n"
                                                                        "Def Value: 0.0\n"
                                                                        "Descr: Value that will be used for angle.\n"))
    args = parser.parse_args()
    return args


def normalize(series, norm_val):
    out = []
    max = series.max()
    min = series.min()

    for num in series.to_list():
        out.append(norm_val * ((num - min) / (max - min)))  # Normalizes to the 20X20 set-up by assure
    returned_Series = pandas.Series(out)

    return returned_Series


def offset(series):
    first = series[0]
    output = []

    for num in series:
        output.append(num - first)
    return output


def str2bool(string):
    if isinstance(string, bool):
        return string
    if string.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif string.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean string expected.')


# Parse through command line arguements
args = arg_parsing()

# Default values
header_size = None
delim = ','

if args.header:
    header_size = 13

if args.tab:
    delim = '\t'

try:
    cleaned = pandas.read_csv(args.input, skiprows=header_size, sep=delim)  # Read in GPS Data
except FileNotFoundError:
    print("The input filepath is incorrect. Please double check and try again. Check for spaces in the file name.")
    sys.exit()
except PermissionError:
    print("File is opened in another task. Please close and try again.")
    sys.exit()
except AttributeError:
    print(
        "Header row (Longitude, Latitude, Altitude) was not found. Check delimiter, if there is a header, or if there is the 13 rows of data from the GPS.")
    sys.exit()
except pandas.errors.EmptyDataError:
    print("File that was given is empty. Please change file names and try again.")
    sys.exit()

if args.waypoints.lower() == "all":
    args.waypoints = len(cleaned.index)
else:
    try:
        args.waypoints = int(args.waypoints)
    except ValueError:
        print("Number of waypoints must be an integer. Please remove the decimal point and try again.")
        sys.exit()

    # Get rid of unneeded data first
    spacing = [num for num in numpy.linspace(0, len(cleaned.index) - 1, num=args.waypoints, dtype=int)]
    entries = []

    for index in spacing:
        temp = cleaned.iloc[index]
        entries.append(temp)

    cleaned = pandas.concat(entries, axis=1).transpose().reset_index(drop=True)

#  Check Mode prior to doing large amounts of data processing
if args.mode.lower() == "xyz":
    # Convert form GPS to UTM
    cleaned['Temp'] = cleaned.apply(lambda x: utm.from_latlon(x.Latitude, x.Longitude),
                                    axis=1)  # X Y UTM_Zone UTM_Letter
    cleaned['X'], cleaned['Y'], *_ = zip(*cleaned.Temp)  # Reads the first two of the tuple and discards the others
    cleaned['Z'] = cleaned['Altitude']  # Altitude remains the same
    good_columns = ['X', 'Y', 'Z']
elif args.lower() == "lla":
    good_columns = ['Latitude', 'Longitude', 'Altitude']
else:
    print("Please choose either lla or xyz as a mode and try again.")
    sys.exit()

trash_cols = [x for x in cleaned.columns if x not in good_columns]  # All columns but the ones specified
cleaned = cleaned.drop(columns=trash_cols)

if not args.rawoutput:
    cleaned.update(cleaned.apply(lambda x: offset(x)))

if args.normalize:
    cleaned.update(cleaned.apply(lambda x: normalize(x, args.normvalue)))

cleaned['Theta'] = args.angle
cleaned['Vel'] = args.velocity
final = cleaned

if not args.spaced:
    final.to_csv(f"{args.output}", index=False, header=False)
else:
    final.to_csv('__temp.csv', index=False, header=False)
    with open("__temp.csv") as temp_file:
        with open(f"{args.output}", 'w') as output:
            # output.write(next(temp_file)) # Used if output header is wanted, like with human readable
            for line in temp_file:
                output.write(line[:-1] + '\r\n')
    os.remove('__temp.csv')

print("CSV Conversion Finished!")