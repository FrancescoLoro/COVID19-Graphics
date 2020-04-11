import argparse
import pandas as pd
import numpy as np
from utils.plotter import regional, national
from git import Repo, NoSuchPathError


def regions_builder():
    """

    :return: dictionary of region -> code
    :rtype: dict
    """
    data = pd.read_csv("COVID-19/dati-regioni/dpc-covid19-ita-regioni-latest.csv")
    codici_regioni = np.array(data['codice_regione'])
    nomi_regioni = np.array(data['denominazione_regione'])
    nomi_regioni = [x.lower().replace('p.a. ', '').replace(' ', '_').replace('\'', '_') for x in nomi_regioni]
    association = dict(zip(nomi_regioni, codici_regioni))
    association.pop('trento')
    association['bolzano_trento'] = association.pop('bolzano')
    return association


if __name__ == '__main__':
    try:
        repo = Repo('COVID-19')
        print('Updating repository data')
        repo.remote('origin').pull()
    except NoSuchPathError:
        print('Downloading repository')
        Repo.clone_from('https://github.com/pcm-dpc/COVID-19.git', 'COVID-19')

    parser = argparse.ArgumentParser(prog='python3 main.py',
                                     description='A tool to show the COVID-19 infected, healed and positive people '
                                                 'relative to Italy and its regions according to official Github data')
    region_choice = regions_builder()
    parser.add_argument('-r', '--region', type=str, choices=region_choice.keys(), metavar='REGION',
                        help='Region to be shown. Valid options are: %(choices)s')
    args = parser.parse_args()

    if args.region is None:
        national()
    else:
        regional(region_choice[args.region], args.region)
