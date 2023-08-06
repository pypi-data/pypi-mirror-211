# SPDX-FileCopyrightText: 2023 Civic Hacker, LLC
#
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid
import random
import csv

from otherworlds.klingon import FEMALE_KLINGON, MALE_KLINGON

DEFAULT_SEED = 270055

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
    "starnames",
    "exoplanets"
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

EXOPLANETS = list()
STARNAMES = list()


def generate_name(include_klingon=False):
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
    if include_klingon:
        NAME_SOURCES.append('female_klingon')
        NAME_SOURCES.append('male_klingon')
    namefix = NAME_SOURCES[starting_ans % len(NAME_SOURCES)]
    suffix = ''
    if namefix == 'female_klingon':
        name = random.sample(FEMALE_KLINGON, 1)[0]
    elif namefix == 'male_klingon':
        name = random.sample(MALE_KLINGON, 1)[0]
    elif namefix == 'exoplanets':
        name = random.sample(EXOPLANETS, 1)[0]
    elif namefix == 'starnames':
        name = random.sample(STARNAMES, 1)[0]
    if suffix_source == 'numerical':
        suffix = f'{random.sample(NUMERICAL, 1)[0]}'
    elif suffix_source == 'mathematical':
        suffix = random.sample(MATHEMATICAL, 1)[0]
    return f'{" ".join([name, suffix]).strip()}'
