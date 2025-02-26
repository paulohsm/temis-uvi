import pandas as pd
import matplotlib.pyplot as plt

# loading data file as dataframe
caminho = "/home/santiago/Projetos/temis-uvi/dados/Maracanau.csv"
uv = pd.read_csv(caminho, skiprows=1, na_values=-999.0, parse_dates=['data'])

# data columns for different time slices
uv['ano'] = uv['data'].dt.year
uv['mes'] = uv['data'].dt.month
uv['est'] = uv['mes'] % 12 // 3 + 1

# selecting time intervals every 30 years for climatology purposes
uv['periodo'] = 3
uv.loc[(uv['ano'] >= 1960) & (uv['ano'] <= 1989), 'periodo'] = 1
uv.loc[(uv['ano'] >= 1990) & (uv['ano'] <= 2019), 'periodo'] = 2

# computing statistics
clim = uv.groupby(['periodo', 'mes'])[['ief', 'dec', 'dvc', 'ddc']].agg(['mean', 'median', 'std'])

# preview statistics dataframe content
#print(clim.head())

# example command to list monthly 
# comando de exemplo para selecionar um conjunto de estatisticas mensais
#print(clim.loc[1, ('ief', 'mean')])

# a function to plot the four variables
meses = range(1, 13)
mesest = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
def graf(clim, variavel, titulo):
    plt.figure(figsize=(6.4, 3.6), dpi=300)

    p1_avg = clim.loc[1, (variavel, 'mean')]
    p1_std = clim.loc[1, (variavel, 'std')]
    p2_avg = clim.loc[2, (variavel, 'mean')]
    p2_std = clim.loc[2, (variavel, 'std')]

    plt.plot(meses, p1_avg, label='1960-1989', marker='o', color='blue')
    plt.fill_between(meses, p1_avg - p1_std, p1_avg + p1_std, color='blue', alpha=0.2)
    plt.plot(meses, p2_avg, label='1990-2019', marker='o', color='red')
    plt.fill_between(meses, p2_avg - p2_std, p2_avg + p2_std, color='red', alpha=0.2)

    plt.title(titulo)
    plt.xlabel('Mês')
    plt.ylabel('Média')
    plt.ylim(0, 16)
    plt.xticks(meses, mesest)
    plt.xlim(1, 12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'graficos/climensal_{variavel}.png')

variaveis = ['ief', 'dec', 'dvc', 'ddc']
titulos = ['Índice UV (ao meio dia)', 
           'Dose diária Eritemal', 
           'Dose diária ativação da Vitamina D', 
           'Dose diária de dano ao DNA']

for variavel, titulo in zip(variaveis, titulos):
    graf(clim, variavel, titulo)