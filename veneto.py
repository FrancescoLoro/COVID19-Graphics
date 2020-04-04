
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#CODICI 5 = VENETO, 3 = LOMBARDIA, 11 = MARCHE

CODICE_REGIONE = 3
plt.show()
data = pd.read_csv("COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv")
codice_regione = data["codice_regione"]
tamponi_reg = []
positivi_reg = []
giorni_reg = []

for i in np.where(codice_regione == CODICE_REGIONE):
    tamponi_reg.append(data["tamponi"][i])
    positivi_reg.append(data["variazione_totale_positivi"][i])
    giorni_reg.append(data["data"][i])


#REMOVE USELESS INDEXES
tamponi_reg = np.array([el[:] for el in map(tuple, tamponi_reg)]).reshape(len(giorni_reg[0]),)
positivi_reg = np.array([el[:] for el in map(tuple, positivi_reg)]).reshape(len(giorni_reg[0]),)
giorni_reg = np.array([el[:] for el in map(tuple, giorni_reg)])

print(positivi_reg)
temp = []
for i in range(len(tamponi_reg)-1):
    temp.append(tamponi_reg[i+1] - tamponi_reg[i])
temp = np.insert(np.array(temp), 0, tamponi_reg[0])
tamponi_reg = temp

temp = []
for i,y in enumerate(giorni_reg[0]):
    temp.append(giorni_reg[0][i][6:10])
giorni_reg = temp

fig, axes = plt.subplots(nrows=2, sharex=True)
axes[0].plot(positivi_reg)
axes[0].set_title("ANDAMENTO NUOVI POSITIVI, OGGI: " + str(positivi_reg[-1]))
axes[0].grid()
axes[1].plot(giorni_reg, np.divide(positivi_reg,tamponi_reg)*100)
axes[1].set_title("ANDAMENTO PERCENTUALE POSITIVI/TAMPONI, OGGI: "+ str(np.around((np.divide(positivi_reg[-1],tamponi_reg[-1])*100), decimals = 2)) + "%")
axes[1].grid()
plt.xticks(rotation=45)
plt.show()