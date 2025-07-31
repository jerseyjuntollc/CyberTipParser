#!/usr/bin/env python3
# Cyber Tip Parser - CTP
# Written by John Luko
# Date:  7/10/2025
# Utilizes py-pdf-parser

import os
import argparse
from py_pdf_parser.loaders import load_file

__version__ = "1.0.0"
__author__ = "John Luko"


def parse_pdf(pdf_file, hash_file):
    # open file - ensure it is in the same directory as the script
    document = load_file(pdf_file)
    # gathers all of the elements related to the MD5
    md5Elements = document.elements.filter_by_text_equal("MD5:")
    # list that will hold all of the MD5s
    md5List = []
    # gathers all of the elements related to the filename
    filenames = document.elements.filter_by_text_equal("Filename:")
    # list that will hold all of the filenames
    fileNamesList = []
    # gets a count to be used by the while loop
    totalNumOfElements = len(document.elements.filter_by_text_equal("MD5:"))
    count = 0

    # adds the filename to the list of filenames
    for name in filenames:
        fileNamesList.append(document.elements.to_the_right_of(name).extract_single_element().text())

    # add the md5 to the list of MD5s
    for md5 in md5Elements:
        md5List.append(document.elements.to_the_right_of(md5).extract_single_element().text())
    with open(hash_file, 'w') as file:
        while count < totalNumOfElements:
            line = fileNamesList[count] + "," + md5List[count]
            file.write(f"{line}\n")
            print(line)
            count += 1


def main():
    arg_parse = argparse.ArgumentParser(description=f"Cyber Tip Parser v{__version__}")
    arg_parse.add_argument('pdf', help='source pdf file')
    arg_parse.add_argument('-o', '--output', metavar="DIR", help='destination directory for the hashes txt file')
    args = arg_parse.parse_args()
    if not os.path.exists(os.path.abspath(args.pdf)):
        arg_parse.error(f"The file {args.pdf} does not exist. Please check your file path and try again.")
    if not os.path.exists(os.path.dirname(args.output)):
        arg_parse.error(f"The path {args.hashes} does not exist. Please check your desired file path and try again.")
    pdf = os.path.abspath(args.pdf)
    hashes = f"{os.path.dirname(args.output)}{os.sep}{os.path.splitext(os.path.basename(pdf))}.txt"
    parse_pdf(pdf, hashes)


if __name__ == "__main__":
    main()
