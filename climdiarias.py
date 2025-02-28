import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# loading data file as dataframe
caminho = "/home/santiago/Projetos/temis-uvi/dados/Maracanau.csv"
uv = pd.read_csv(caminho, skiprows=1, na_values=-999.0, parse_dates=['data'])

uv['ano'] = uv['data'].dt.year
uv['dia_do_ano'] = uv['data'].dt.day_of_year

# selecting time intervals every 30 years for climatology purposes
uv['periodo'] = 3
uv.loc[(uv['ano'] >= 1960) & (uv['ano'] <= 1989), 'periodo'] = 1
uv.loc[(uv['ano'] >= 1990) & (uv['ano'] <= 2019), 'periodo'] = 2
ciclo_anual = uv.groupby(['periodo', 'dia_do_ano'])[['ief', 'dec', 'dvc', 'ddc']].agg(['mean', 'median', 'std'])
plt.figure(figsize=(19.2, 10.8), dpi=320)

def graf(dados, variavel, titulo):
    p1_avg = dados.loc[1, (variavel, 'mean')]
    p1_std = dados.loc[1, (variavel, 'std')]
    p2_avg = dados.loc[2, (variavel, 'mean')]
    p2_std = dados.loc[2, (variavel, 'std')]

    datas = [datetime(2023, 1, 1) + pd.Timedelta(days=int(dia)) for dia in p1_avg.index]

    plt.figure(figsize=(19.2, 10.8), dpi=320)
    ax = plt.gca()

    plt.plot(datas, p1_avg, label='1960-1989')
    plt.fill_between(datas, p1_avg - p1_std, p1_avg + p1_std, alpha=0.2)
    plt.plot(datas, p2_avg, label='1990-2019')
    plt.fill_between(datas, p2_avg - p2_std, p2_avg + p2_std, alpha=0.2)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    plt.title(titulo)
    plt.xlabel('Dia do ano')
    plt.xticks(rotation=45)
    plt.xlim(min(datas), max(datas))
    plt.ylim(0, 16.5)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'graficos/climdiaria_{variavel}.png')

variaveis = ['ief', 'dec', 'dvc', 'ddc']
titulos = ['Índice UV (ao meio dia)',
           'Dose UV diária eritemal', 
           'Dose UV diária de ativação da Vit. D',
           'Dose UV diária de dano ao DNA']

for variavel, titulo in zip(variaveis, titulos):
    graf(ciclo_anual, variavel, titulo)