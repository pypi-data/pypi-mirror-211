# SPDX-FileCopyrightText: 2023 Civic Hacker, LLC
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import uuid
import random
import csv

PREFIX_TYPES = [
    "mathematical",
    "empty"
]


SUFFIX_TYPES = [
    'numerical',
    'mathematical',
    'empty'
]

NAME_SOURCES = [
    "male_klingon",
    "exoplanets",
    "female_klingon"
]

MATHEMATICAL = [
    'Alpha',
    'Prime',
    'Beta',
    'Rho',
    'Delta',
    'Omega',
    'Epsilon',
    'Theta'
]

NUMERICAL = random.sample(range(1, 10), 1)

FEMALE_KLINGON = [
    "Azetbur",
    "B'Etor",
    "Ba'el",
    "Ch'Rega",
    "Ezri",
    "Grilka",
    "Jadzia Dax",
    "K'Ehleyr",
    "Lursa",
    "Miral",
    "Valkris",
]

MALE_KLINGON = [
    "Antaak",
    "Atul",
    "Brota",
    "Klaang",
    "Kol",
    "Kol-Sha",
    "Magh",
    "Maltz",
    "Orak",
    "Rodek",
    "Sisko",
    "Toral",
    "Voq",
]

EXOPLANETS = list()
STARNAMES = list()

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", help="Select a name randomly",
                    action="store_true")
parser.add_argument("-s", "--story", help="Print the entire story of a planet",
                    action="store_true")

if __name__ == '__main__':
    args = parser.parse_args()
    with open('./data/NameExoWorlds.csv', 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            EXOPLANETS.append(line.get("Name Exoplanet"))
            STARNAMES.append(line.get("Name Star"))
    UUID = str(uuid.uuid4())
    ending = UUID.split('-')[-1]
    starting = UUID.split('-')[0]
    ending_ans = int(ending[0], base=16)+int(ending[1], base=16)
    starting_ans = int(starting[0], base=16)+int(starting[1], base=16)
    suffix_source = SUFFIX_TYPES[ending_ans % len(SUFFIX_TYPES)]
    namefix = NAME_SOURCES[starting_ans % len(NAME_SOURCES)]
    suffix = ''
    if namefix == 'female_klingon':
        name = random.sample(FEMALE_KLINGON, 1)[0]
    elif namefix == 'male_klingon':
        name = random.sample(MALE_KLINGON, 1)[0]
    elif namefix == 'exoplanets':
        name = random.sample(EXOPLANETS, 1)[0]
    if suffix_source == 'numerical':
        suffix = f'{random.sample(NUMERICAL, 1)[0]}'
    elif suffix_source == 'mathematical':
        suffix = random.sample(MATHEMATICAL, 1)[0]
    print(f'{" ".join([name, suffix])}')
