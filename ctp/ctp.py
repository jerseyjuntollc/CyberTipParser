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


def parse_pdf(pdf_file, output_path, verbose=False):
    # open file - ensure it is in the same directory as the script
    hashes = f"{output_path}-hashes.txt"
    ips = f"{output_path}-ips.txt"
    document = load_file(pdf_file)
    # gathers all of the elements related to the MD5 and IP
    md5Elements = document.elements.filter_by_text_equal("MD5:")
    ipElements = document.elements.filter_by_test_equal("IP Address:")
    # lists that will hold all of the MD5s and IPs
    md5List = []
    ipList = []
    # gathers all of the elements related to the filename
    filenames = document.elements.filter_by_text_equal("Filename:")
    # list that will hold all of the filenames
    fileNamesList = []
    # gets a count to be used by the while loop
    totalNumOfHashes = len(document.elements.filter_by_text_equal("MD5:"))
    totalNumOfIps = len(document.elements.filter_by_text_equal("IP Address:"))
    hashCount = 0
    ipCount = 0
    # adds the filename to the list of filenames
    for name in filenames:
        fileNamesList.append(document.elements.to_the_right_of(name).extract_single_element().text())

    # add the md5 to the list of MD5s
    for md5 in md5Elements:
        md5List.append(document.elements.to_the_right_of(md5).extract_single_element().text())

    # add the IP to the list of IPs
    for ip in ipElements:
        ipList.append(document.elements.to_the_right_of(ip).extract_single_element().text())

    if verbose:
        print(ipList)

    with open(hashes, 'w') as file:
        while hashCount < totalNumOfHashes:
            line = fileNamesList[count] + "," + md5List[count]
            file.write(f"{line}\n")
            if verbose:
                print(line)
            hashCount += 1

    with open(ips, 'w') as file:
        while ipCount < totalNumOfIps:
            line = ipList[ipCount]
            file.write(f"{line}\n")
            if verbose:
                print(line)
            ipCount += 1
    print(f"Hashes written to {hashes}")
    print(f"IPs written to {ips}")


def main():
    arg_parse = argparse.ArgumentParser(description=f"Cyber Tip Parser v{__version__}")
    arg_parse.add_argument('pdf', help='source pdf file')
    arg_parse.add_argument('-o', '--output', metavar="DIR", help='destination directory for the output files')
    arg_parse.add_argument('-V', '--verbose', help='prints results to stdout', dest='verbose', action='store_true')
    args = arg_parse.parse_args()
    if not os.path.exists(os.path.abspath(args.pdf)):
        arg_parse.error(f"The file {args.pdf} does not exist. Please check your file path and try again.")
    if not os.path.exists(os.path.dirname(args.output)):
        arg_parse.error(f"The path {args.hashes} does not exist. Please check your desired file path and try again.")
    pdf = os.path.abspath(args.pdf)
    output_path = f"{os.path.dirname(args.output)}{os.sep}{os.path.splitext(os.path.basename(pdf))}"
    parse_pdf(pdf, output_path, verbose=args.verbose)


if __name__ == "__main__":
    main()
