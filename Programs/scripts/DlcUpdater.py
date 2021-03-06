#!/bin/python
# -*- coding: utf-8 -*-
###############################################################################
#  Update the content of distribution and tweet files - V1.0                  #
#  Copyright 2015 Benito Palacios (aka pleonex)                               #
#                                                                             #
#  Licensed under the Apache License, Version 2.0 (the "License");            #
#  you may not use this file except in compliance with the License.           #
#  You may obtain a copy of the License at                                    #
#                                                                             #
#      http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                             #
#  Unless required by applicable law or agreed to in writing, software        #
#  distributed under the License is distributed on an "AS IS" BASIS,          #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#  See the License for the specific language governing permissions and        #
#  limitations under the License.                                             #
###############################################################################

from argparse import ArgumentParser
from struct import pack
from os import listdir, path
from datetime import date, datetime
from binascii import crc32
import xml.etree.ElementTree as ET

# Set today as global variable just in case the day change while the
# program is running (very very rare case but...)
TODAY = datetime.utcnow().date()


def rc4(data):
    KEY = bytearray([0x72, 0x2B, 0x41, 0x8B, 0x4C, 0xFB, 0x9F, 0x27,
                    0xB2, 0x1D, 0x05, 0xAF, 0xFB, 0x2B, 0x80, 0x9F])

    i = j = 0
    s = rc4_create_array_s(KEY)
    for index in range(len(data)):
        i = (i + 1) % 256
        j = (j + s[i]) % 256

        swap = s[i]
        s[i] = s[j]
        s[j] = swap

        k = s[(s[i] + s[j]) % 256]
        data[index] ^= k

    return data


def rc4_create_array_s(key):
    s = bytearray(256)
    t = bytearray(256)

    for i in range(256):
        s[i] = i
        t[i] = key[i % len(key)]

    j = 0
    for i in range(256):
        j = (j + s[i] + t[i]) % 256

        swap = s[i]
        s[i] = s[j]
        s[j] = swap

    return s


def add_distribution_header(data):
    HEADER = "NNKN"
    checksum = crc32(data) & 0xffffffff
    return bytearray(HEADER, 'ascii') + pack("<I", checksum) + data


def xml2binary(node, date_format):
    NUM_ELEMENTS = int(0x80 / 8)  # Actually, there are 0x72
    INVALID_DATE = date(1, 1, 1)

    data = bytearray(NUM_ELEMENTS)
    for el in node.findall("Element"):
        el_date = datetime.strptime(el.get("releaseOn"), date_format).date()

        if el_date != INVALID_DATE and el_date <= TODAY:
            el_id = int(el.get("id"))
            byte_index = int(el_id / 8)
            bit_index = el_id % 8
            data[byte_index] |= (1 << bit_index)

    return data


def should_update_file(base_path, filename):
    # Get full name without extension and basename
    file_date = date(1, 1, 1)
    for file in listdir(base_path):
        if file == filename:
            file_date = datetime.utcfromtimestamp(path.getmtime(path.join(base_path,file))).date()

    # If the file does not exist
    if file_date.year == 1:
        return True

    return file_date < TODAY


def update_distribution(node, base_path, lang, list_data):
    # Get output path and date format
    out_path = path.join(base_path, node.get("output"))
    date_format = node.get("dateFormat")

    # Get distribution node
    filename =  "distribution_" + lang + ".bin"
    file_path = path.join(out_path, filename)
    filesize = 0
    if should_update_file(out_path, filename):
        data = xml2binary(node, date_format)
        data = add_distribution_header(data)
        data = rc4(data)

        filesize = len(data)

        # Write to file
        with open(file_path, "wb") as file:
            file.write(data)
    else:
        # Get filesize
        filesize = path.getsize(file_path)
        

    list_data.append((filename, filesize, lang))


def update_magic_news(node, base_path, lang, list_data):
    if lang == "SPA":
        list_data.append(("tweets29052015_spa.bin", 2416, "SPA")) # Remove once magic news is implemented

    # Not implemented
    pass


def update_translation_files(node, base_path, list_data):
    lang = node.get("language")

    # Get distribution node
    distribution = node.find("Distribution")
    update_distribution(distribution, base_path, lang, list_data)

    # Get magic news node
    magic_news = node.find("MagicNews")
    update_magic_news(magic_news, base_path, lang, list_data)



def write_list_file(base_path, list_data):
    file_path = path.join(base_path, "_list.txt")

    format = "%s\t\t%s\t\t\t%d"
    with open(file_path, "w") as file:
        for l in list_data:
            file.write(format % (l[0], l[2], l[1]))
            file.write("\n")

if __name__ == "__main__":
    # Get arguments
    parser = ArgumentParser(description="Update DLC files of Ninokuni DS")
    parser.add_argument('dlcinfo', help='path to XML with the info')
    args = parser.parse_args()

    # Get base path (the one from the xml)
    base_path = path.dirname(path.realpath(args.dlcinfo))

    # The data for the output _list.txt database file
    # Initial values are the static Japanese DLC files
    list_data = [ ("distribution110609.bin", 24, ""), ("tweet111209.bin", 2416, "") ] # For Japanese DLC

    # Get translations nodes
    root = ET.parse(args.dlcinfo).getroot()
    for trans in root.findall("Ninokuni"):
        update_translation_files(trans, base_path, list_data)

    print list_data
    write_list_file(base_path, list_data)
