import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# loading data file as dataframe
caminho = "/home/santiago/Projetos/temis-uvi/dados/Maracanau.csv"
uv = pd.read_csv(caminho, skiprows=1, na_values=-999.0, parse_dates=['data'])

variaveis = uv.columns[1:]

uv['ano'] = uv['data'].dt.year
uv['mes'] = uv['data'].dt.month

# selecting time intervals every 30 years for climatology purposes
uv['periodo'] = '2020 em diante'
uv.loc[(uv['ano'] >= 1960) & (uv['ano'] <= 1989), 'periodo'] = '1960-1989'
uv.loc[(uv['ano'] >= 1990) & (uv['ano'] <= 2019), 'periodo'] = '1990-2019'
uv = uv[uv['periodo'].isin(['1960-1989', '1990-2019'])]

meses_abreviados = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
plt.figure(figsize=(19.2, 10.8), dpi=320)

def boxes(dados, variavel, titulo):
    plt.figure(figsize=(19.2, 10.8), dpi=320)
    ax = sns.boxplot(data=dados, 
                     x='mes', 
                     y=variavel, 
                     hue='periodo', 
                     palette='Set2', 
                     hue_order=['1960-1989', '1990-2019'])

    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    ax.set_xticks(range(12))
    ax.set_xticklabels(meses_abreviados)
    ax.legend(title='Período')

    plt.title(titulo)
    plt.xlabel('Mês')
    plt.ylabel(variavel)
    plt.tight_layout()

    plt.savefig(f'graficos/dispersao_{variavel}.png')
    plt.close()

titulos = ['Índice UV (ao meio dia)',
           'Dose UV diária eritemal', 
           'Dose UV diária de ativação da Vit. D',
           'Dose UV diária de dano ao DNA']

for variavel, titulo in zip(variaveis, titulos):
    boxes(uv, variavel, titulo)

print(uv.describe())