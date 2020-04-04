
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("COVID-19/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
tamponi_ita = np.array(data["tamponi"])
positivi_ita = np.array(data["variazione_totale_positivi"])
dimessi_ita = np.array(data["dimessi_guariti"])
giorni = np.array(data["data"])
print(dimessi_ita)
temp = []
temp1 = []
for i in range(len(tamponi_ita)-1):
    temp.append(tamponi_ita[i+1] - tamponi_ita[i])
    temp1.append(dimessi_ita[i+1] - dimessi_ita[i])
temp = np.insert(np.array(temp), 0, tamponi_ita[0])
temp1 = np.insert(np.array(temp1), 0, dimessi_ita[0])
tamponi_ita = temp
dimessi_ita = temp1
print(dimessi_ita)

temp = []
for i,y in enumerate(giorni):
    temp.append(giorni[i][6:10])
giorni = temp

fig, axes = plt.subplots(nrows=3, sharex=True)
axes[0].plot(positivi_ita)
axes[0].set_title("ANDAMENTO NUOVI POSITIVI, OGGI: " + str(positivi_ita[-1]))
axes[0].grid()
axes[1].plot(giorni, np.divide(positivi_ita,tamponi_ita)*100)
axes[1].set_title("ANDAMENTO PERCENTUALE POSITIVI/TAMPONI, OGGI: "+ str(np.around((np.divide(positivi_ita[-1],tamponi_ita[-1])*100), decimals = 2)))
axes[1].grid()
axes[2].plot(dimessi_ita)
axes[2].set_title("ANDAMENTO NUOVI GUARITI, OGGI: " + str(dimessi_ita[-1]))
axes[2].grid()
plt.xticks(rotation=45)
plt.show()