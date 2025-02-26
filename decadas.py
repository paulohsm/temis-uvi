import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# loading data
caminho = "/home/santiago/Projetos/temis-uvi/dados/Maracanau.csv"
uv = pd.read_csv(caminho, skiprows=1, na_values=-999.0, parse_dates=['data'])

# 'dcd' refers to 'decada'; should be 'dec', but one variable is named so.
uv['dcd'] = (uv['data'].dt.year // 10) * 10
uv['mes'] = (uv['data'].dt.year % 10) * 12 + uv['data'].dt.month

# monthly averages and standard deviations
decadas = uv.groupby(['dcd', 'mes']).agg(['mean', 'std'])

# min and max values for axes limits
min_val = uv[['ief', 'dvc', 'dec', 'ddc']].min().min()
max_val = uv[['ief', 'dvc', 'dec', 'ddc']].max().max()

# opening a figure
plt.figure(figsize=(6.4, 3.6), dpi=300)

def graf(decada, variavel, titulo):
    plt.figure(figsize=(6.4, 3.6), dpi=300)
    for anodec in decada.index.levels[0]:
        dec_avg = decada.loc[anodec, (variavel, 'mean')]
        dec_std = decada.loc[anodec, (variavel, 'std')]
        plt.plot(dec_avg.index, dec_avg, label=f'{anodec}s')
        plt.fill_between(
            dec_avg.index,
            dec_avg - dec_std, 
            dec_avg + dec_std, 
            alpha = 0.2
        )
    plt.xlim(1, 120)
    plt.ylim(min_val - 1, max_val + 1)
    plt.xticks(np.arange(12, 121, 12))
    plt.title(titulo)
    plt.xlabel('Mês')
    plt.ylabel(variavel)
    plt.legend()
    plt.savefig(f'graficos/decadas_{variavel}.png')

variaveis = ['ief', 'dec', 'dvc', 'ddc']
titulos = ['Índice UV (ao meio dia)', 
           'Dose diária Eritemal', 
           'Dose diária ativação da Vitamina D', 
           'Dose diária de dano ao DNA']

for variavel, titulo in zip(variaveis, titulos):
    graf(decadas, variavel, titulo)
