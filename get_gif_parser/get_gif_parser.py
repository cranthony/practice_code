# This script reads a filename from stdin, and outputs a file that contains the
# unique GIF images from the successful (HTTP status = 200) GET requests in the
# input file.  The input file is a space-delimited table with the following
# format:
#
# A - - "GET /path/to/file.gif HTTP/1.0" 1 200
#
# The definitions of most of these terms isn't clear, but the quoted 4th column
# contains the GET request, for which we want to grab the GIF files, and the
# last column contains a status code.
#
# In the above case, the output file would contain:
#
# file.gif
#
# To test this script, you can run the following command:
#
# echo test_requests.txt | python3 ./get_git_parser.py && echo -- && cat gif*

import csv
import os

filename = input()

def csv_approach(input_file):
    """
    Returns a set containing the GIF filenames from the given request file,
    using an approach that uses a CSV utility to parse the input file like a
    table.
    """

    # Track the list of GIF files with a set because we don't care about order
    # and we want unique filenames.
    gif_filenames = set()

    input_csv = csv.reader(input_file, delimiter=' ')
    for line in input_csv:
        # We only care about successful requests.  The 6th column is the HTTP
        # status code.
        if int(line[5]) != 200:
            continue

        # Per the format above, the 4th column contains the GET request.
        request = line[3].split(' ')

        if request[0].upper() == 'GET':
            # Assume that the filename is unquoted and is the second term of
            # the request, immediately after the GET.
            requested_filename = os.path.basename(request[1])
            if requested_filename.split('.')[-1].lower() == 'gif':
                gif_filenames.add(requested_filename)

    return gif_filenames

def string_parse_approach(input_file):
    """
    Returns a set containing the GIF filenames from the given request file,
    using simple string parsing, for illustration of comments and coding style.
    """

    # Track the list of GIF files with a set because we don't care about order
    # and we want unique filenames.
    gif_filenames = set()

    for line in input_file:
        split_line = line.split(' ')

        # We only care about successful requests.  The last column is the HTTP
        # status code.
        if int(split_line[-1]) != 200:
            continue

        # The GIF is in the GET request in the third-to-last column.  The last
        # and second-to-last columns don't have spaces, and the third-to-last
        # column is always of the following form:
        #   "GET /path/to/file HTTP/1.0"
        #
        # Since the file's path doesn't have spaces, and the term after the
        # file doesn't have spaces, we know that the 4th-to-last term is the
        # file path.  Here's an example line:
        #   A - - "GET /path/to/file.gif HTTP/1.0" 1 200
        requested_filename = os.path.basename(split_line[-4])
        if requested_filename.split('.')[-1].lower() == 'gif':
            gif_filenames.add(requested_filename)

    return gif_filenames

with open(filename, 'r') as input_file:
    csv_gif_filenames = csv_approach(input_file)

    # Go back to the beginning of the file and do it again, with another
    # approach, for illustration.
    input_file.seek(0)
    string_parse_gif_filenames = string_parse_approach(input_file)

    if csv_gif_filenames == string_parse_gif_filenames:
        print("Results are the same for the CSV and String parse approaches")
    else:
        print("Results are different between the approaches:")
        print('CSV approach: ', csv_gif_filenames)
        print('String parse approach: ', string_parse_gif_filenames)

    gif_filenames = csv_gif_filenames

# Write the GIF filenames to the output file.
with open('gif_{}'.format(filename), 'w') as output_file:
    for filename in gif_filenames:
        output_file.write(filename + '\n')
