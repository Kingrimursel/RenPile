"""
This program is written in python3.6. It is able to rename multiple elements
at once.
Given a root word, it renames the queued elements to "word root" + an integer,
starting with 0 and counting up from there.
The user gives the program a source-directory, where the program will operate.
It is able to either rename files by a specific type or just directories, as
well as all children of the given parent directory.
The program can also change the type of a file.

For more informations open a shell, navigate to the directory where this file
is stored and type:'python3* RenPile.py -h'
*or whatever python interpreter you are using.
"""
from argparse import ArgumentParser
from argparse import SUPPRESS
import os
from os import listdir
from os.path import isfile, join
from termcolor import colored

# Setting up the arguments passed when running the program.
parser = ArgumentParser(description="Rename-Pile Help:",
                        prog="RenPile",
                        usage='%(prog)s [-h] [-v,--version]',
                        add_help=False)

informational_arguments = parser.add_argument_group('Informational arguments')
informational_arguments.add_argument('-h', '--help', action='help',
                                     default=SUPPRESS,
                                     help="Show this message and exit.")
informational_arguments.add_argument('-v', '--version', action='version',
                                     version='%(prog)s 1.0',
                                     help="Show the programs version and exit."
                                     )
required_arguments = parser.add_argument_group('Required arguments')
required_arguments.add_argument("-dir", "--directory", dest="directory",
                                help="Source directory.",
                                required=True, metavar="\b")
required_arguments.add_argument("-r", "--root", dest="root",
                                help="New root word.", required=True,
                                metavar="\b")

optional_arguments = parser.add_argument_group('Optional arguments')
optional_arguments.add_argument("-ft", "--fromtype", dest="fromtype",
                                help="Just rename files from this type. Use "
                                "\"dir\" or \"directory\" to just rename "
                                "directories.", metavar="\b")
optional_arguments.add_argument("-tt", "--totype", dest="totype",
                                help="Convert to type.", metavar="\b")

args = parser.parse_args()

# Check if source directory exists.
is_directory = os.path.isdir(args.directory)

# If the passed source directory exists, keep going.
if is_directory:
    # The array that will contain the files that should be renamed.
    dirfiles = []
    # If 'fromtype' was set, just queue elements by this type.
    if args.fromtype is not None:
        # Check if fromtype is 'directory'
        if (args.fromtype == "dir" or args.fromtype == "directory"):
            # Add elements that should be renamed to the array.
            dirfiles = [x[0] for x in os.walk(args.directory)]
            del dirfiles[0]
        # If 'fromtype' is set but not as 'dir', do the following.
        else:
            for f in listdir(args.directory):
                # Safe the old file extension of every file in the directory
                old_extension = os.path.splitext(join(args.directory, f))[1]
                # Check if the old file extension is equal to the current file.
                if(old_extension == "." + args.fromtype):
                    # ... ad to the array.
                    dirfiles.append(join(args.directory, f))
    # If fromtype is not set
    else:
        # Take all files in the source direcotry and put them into the array
        dirfiles = [f for f in listdir(args.directory)
                    if isfile(join(args.directory, f))]
    i = 0
    # Take one file after the other from the array.
    for file in dirfiles:
        #  Check if the type of the files should be changed.
        if args.totype is not None:
            # If 'fromtype' is set and equal to 'directory', exit because you
            # can't change a directories type.
            if(args.fromtype == "dir" or args.fromtype == "directory"):
                print(colored('Can\'t change the type of a directory', 'red'))
                exit(2)
            else:
                # If 'totype' is set and not equal to 'directory', safe the new
                # file extension.
                new_extension = "." + args.totype
        else:
            # If 'totype' is not set, every file should keep it's extension.
            new_extension = os.path.splitext(file)[1]
        # Check if the new name exists, if not rename the file.
        if not os.path.exists(os.path.join(args.directory, args.root + str(i)
                                           + new_extension)):
            os.rename(os.path.join(args.directory, file),
                      os.path.join(args.directory, args.root + str(i)
                                   + new_extension))
        # If the new name does exist, exit.
        else:
            print(colored('Name ' + args.root + str(i) + ' already exists.',
                          'yellow'))
            exit(2)
        i += 1
    # If everything went right and more than 0 items were converted, print.
    if(len(dirfiles) > 0):
        print(colored('Successfully converted', 'green'))
    # If nothing was converted, print.
    else:
        print(colored('No items found, so nothing converted.', 'red'))
# If source directory doesn't exist, exit.
else:
    print(colored('Source directory doesn\'t exist', 'red'))
    exit(2)
