# Cyber Tip Parser - CTP
# Written by John Luko
# Date:  7/10/2025
# Utilizes py-pdf-parser

from py_pdf_parser.loaders import load_file


# open file - ensure it is in the same directory as the script
document = load_file("")

# file name
file_name = 'hashes.txt'
ip_file_name = 'ips.txt'

# gathers all of the elements related to IP
ipElements = document.elements.filter_by_text_equal("IP Address:")
# list that will hold all of the IP addresses
ipList = []

# gathers all of the elements related to the MD5
md5Elements = document.elements.filter_by_text_equal("MD5:")
# list that will hold all of the MD5s
md5List = []

# gathers all of the elements related to the filename
filenames = document.elements.filter_by_text_equal("Filename:")
# list that will hold all of the filenames
fileNamesList = []

# gets a count to be used by the while loop and for IPS
totalNumOfElements = len(document.elements.filter_by_text_equal("MD5:"))
totalNumOfIps = len(document.elements.filter_by_text_equal("IP Address:"))
count = 0
countIP = 0

# adds the filename to the list of filenames
for name in filenames:
    fileNamesList.append(document.elements.to_the_right_of(name).extract_single_element().text())

# add the md5 to the list of MD5s
for md5 in md5Elements:
    md5List.append(document.elements.to_the_right_of(md5).extract_single_element().text())

# add the IP to the list of IPs
for ip in ipElements:
    ipList.append(document.elements.to_the_right_of(ip).extract_single_element().text())
print(ipList)
with open(file_name, 'w') as file:
    while count < totalNumOfElements:
        temp = fileNamesList[count] + "," + md5List[count]
        file.write(f"{temp}\n")
        print(temp)
        count += 1

with open(ip_file_name, 'w') as file:
    while countIP < totalNumOfIps:
        temp = ipList[countIP]
        file.write(f"{temp}\n")
        print(temp)
        countIP += 1
