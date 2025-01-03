import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

caminho = "/home/santiago/Projetos/temis-uvi/Maracanau.csv"
temis = pd.read_csv(caminho, skiprows=1, na_values=-999.0)
temis['data'] = pd.to_datetime(temis['data'])

temis['ano'] = temis['data'].dt.year
temis['mes'] = temis['data'].dt.month

def clim(grupo):
    return pd.Series({'media': grupo.mean(), 'despd': grupo.std()})

estats = temis.groupby(['ano', 'mes']).agg(clim).unstack()

clim1990 = estats.loc[1:30]
clim2020 = estats.loc[31:60]

clim1990['media']['ief'].plot(label='1960-1990')
clim2020['media']['ief'].plot(label='1990-2020')
plt.legend()
plt.title('Médias Climatológicas Mensais IEF')
plt.xlabel('Mês')
plt.ylabel('Intensidade (J/m²)')
plt.show()