# Cyber Tip Parser - CTP
# Written by John Luko
# Date:  7/10/2025
# Utilizes py-pdf-parser

from py_pdf_parser.loaders import load_file


# open file - ensure it is in the same directory as the script
document = load_file("206973054.pdf")

# file name
file_name = 'hashes.txt'


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

with open(file_name, 'w') as file:
    while count < totalNumOfElements:
        temp = fileNamesList[count] + "," + md5List[count]
        file.write(f"{temp}\n")
        print(temp)
        count += 1

