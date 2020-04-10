#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse


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
    del association['trento']
    association['bolzano_trento'] = association.pop('bolzano')
    return association


def national():
    data = pd.read_csv("COVID-19/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
    tamponi_ita = np.array(data["tamponi"])
    positivi_ita = np.array(data["variazione_totale_positivi"])
    dimessi_ita = np.array(data["dimessi_guariti"])
    giorni = np.array(data["data"])
    print(dimessi_ita)
    temp = []
    temp1 = []
    for i in range(len(tamponi_ita) - 1):
        temp.append(tamponi_ita[i + 1] - tamponi_ita[i])
        temp1.append(dimessi_ita[i + 1] - dimessi_ita[i])
    temp = np.insert(np.array(temp), 0, tamponi_ita[0])
    temp1 = np.insert(np.array(temp1), 0, dimessi_ita[0])
    tamponi_ita = temp
    dimessi_ita = temp1
    print(dimessi_ita)

    temp = []
    for i, y in enumerate(giorni):
        temp.append(giorni[i][6:10])
    giorni = temp

    pos_test_ratio = np.divide(positivi_ita, tamponi_ita)

    fig, axes = plt.subplots(nrows=3, sharex=True)
    axes[0].plot(positivi_ita)
    axes[0].set_title("ANDAMENTO NUOVI POSITIVI, OGGI: {}".format(positivi_ita[-1]))
    axes[0].grid()
    axes[1].plot(giorni, np.divide(positivi_ita, tamponi_ita) * 100)
    axes[1].set_title("ANDAMENTO PERCENTUALE POSITIVI/TAMPONI, OGGI: {:.2f}% ({:+.2f}%)".
                      format(pos_test_ratio[-1] * 100, (pos_test_ratio[-1] - pos_test_ratio[-2]) * 100))
    axes[1].grid()
    axes[2].plot(dimessi_ita)
    axes[2].set_title("ANDAMENTO NUOVI GUARITI, OGGI: {}".format(dimessi_ita[-1]))
    axes[2].grid()
    fig.canvas.set_window_title("Dati Nazionali")
    plt.xticks(rotation=45)
    plt.show()


def regional(regione_selezionata, nome_regione):
    plt.show()
    data = pd.read_csv("COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv")
    codice_regione = data["codice_regione"]
    tamponi_reg = []
    positivi_reg = []
    giorni_reg = []

    for i in np.where(codice_regione == regione_selezionata):
        tamponi_reg.append(data["tamponi"][i])
        positivi_reg.append(data["variazione_totale_positivi"][i])
        giorni_reg.append(data["data"][i])

    # REMOVE USELESS INDEXES
    tamponi_reg = np.array([el[:] for el in map(tuple, tamponi_reg)]).reshape(len(giorni_reg[0]), )
    positivi_reg = np.array([el[:] for el in map(tuple, positivi_reg)]).reshape(len(giorni_reg[0]), )
    giorni_reg = np.array([el[:] for el in map(tuple, giorni_reg)])

    print(positivi_reg)
    temp = []
    for i in range(len(tamponi_reg) - 1):
        temp.append(tamponi_reg[i + 1] - tamponi_reg[i])
    temp = np.insert(np.array(temp), 0, tamponi_reg[0])
    tamponi_reg = temp

    temp = []
    for i, y in enumerate(giorni_reg[0]):
        temp.append(giorni_reg[0][i][6:10])
    giorni_reg = temp

    # fix for bolzano/trento since they have the same regional code
    if regione_selezionata == 4:
        tmp_pos = []
        tmp_tamponi = []
        for idx in range(0, (len(positivi_reg)) // 2):
            tmp_pos.append(positivi_reg[idx] + positivi_reg[idx + 1])
        for idx in range(0, (len(tamponi_reg)) // 2):
            tmp_tamponi.append(tamponi_reg[idx] + tamponi_reg[idx + 1])
        positivi_reg = tmp_pos
        tamponi_reg = tmp_tamponi
        giorni_reg = giorni_reg[1::2]

    np.seterr(divide='ignore', invalid='ignore')
    pos_test_ratio = np.divide(positivi_reg, tamponi_reg)
    pos_test_ratio = np.abs(np.nan_to_num(pos_test_ratio, posinf=0.))

    fig, axes = plt.subplots(nrows=2, sharex=True)
    axes[0].plot(np.abs(positivi_reg))
    axes[0].set_title("ANDAMENTO NUOVI POSITIVI, OGGI: {}".format(positivi_reg[-1]))
    axes[0].grid()
    axes[1].plot(giorni_reg, pos_test_ratio)
    axes[1].set_title("ANDAMENTO PERCENTUALE POSITIVI/TAMPONI, OGGI: {:.2f}% ({:+.2f}%)".
                      format(pos_test_ratio[-1] * 100, (pos_test_ratio[-1] - pos_test_ratio[-2]) * 100))
    axes[1].grid()
    fig.canvas.set_window_title("Dati regione " + str(nome_regione))
    plt.xticks(rotation=45)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    region_choice = regions_builder()
    parser.add_argument('-r', '--region', type=str, choices=region_choice.keys(), metavar='REGION',
                        help='Region to be shown. Valid options are: %(choices)s')
    args = parser.parse_args()
    if args.region is None:
        national()
    else:
        regional(region_choice[args.region], args.region)
