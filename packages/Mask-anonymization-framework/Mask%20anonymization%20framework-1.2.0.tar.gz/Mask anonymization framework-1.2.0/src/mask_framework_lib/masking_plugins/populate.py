import os
import csv
from typing import Set
import pathlib


def cities() -> Set:
    """
    returns name of citites
    """
    dirname = os.path.dirname(__file__)
    city_file = open(os.path.join(dirname, pathlib.Path(__file__).parent.resolve()+'../Dictionaries/Cities.txt'), 'r', encoding='utf 8')
    return set(line.strip().lower() for line in city_file)


def countries() -> Set:
    """
    returns name of countries
    """
    dirname = os.path.dirname(__file__)
    countries_file = open(os.path.join(dirname, '../Dictionaries/Countries.txt'), 'r', encoding='utf 8')
    return set(line.strip().lower() for line in countries_file)


def first_names() -> Set:
    """
    returns first names dictionary
    """
    dirname = os.path.dirname(__file__)
    first_names_file = open(os.path.join(dirname, '../Dictionaries/dictionary_first_names.txt'), 'r', encoding='utf 8')
    return set(line.strip().lower() for line in first_names_file)


def last_names() -> Set:
    """
    returns last names dictionary
    """
    dirname = os.path.dirname(__file__)
    last_names_file = open(os.path.join(dirname, '../Dictionaries/dictionary_surnames.txt'), 'r', encoding='utf 8')
    return set(line.strip().lower() for line in last_names_file)


def job_titles() -> Set:
    """
    returns job titles dictionary
    """
    dirname = os.path.dirname(__file__)
    jobs = set()
    with open(os.path.join(dirname, '../Dictionaries/job_title_dictionary.csv'), 'r', encoding='utf 8') as job_file:
        csv_file = csv.reader(job_file, delimiter=',')
        for row in csv_file:
            if row[2] == 'assignedrole':
                words = row[0].lower().split()
                min_2char_words = [word for word in words if len(word) > 2]
                jobs.add(' '.join(min_2char_words))
    return jobs







