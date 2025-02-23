import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

caminho = "/home/santiago/Projetos/temis-uvi/Maracanau.csv"
df = pd.read_csv(caminho, skiprows=1, na_values=-999.0)
df['data'] = pd.to_datetime(df['data'])

df['decada'] = (df['data'].dt.year // 10) * 10
df['mes_na_decada'] = (df['data'].dt.year % 10) * 12 + df['data'].dt.month

resultados = df.groupby(['decada', 'mes_na_decada']).agg(['mean', 'std'])

min_val = df[['ief', 'dvc', 'dec', 'ddc']].min().min()
max_val = df[['ief', 'dvc', 'dec', 'ddc']].max().max()

variaveis = ['ief', 'dvc', 'dec', 'ddc']
for var in variaveis:
    plt.figure(figsize=(21, 9))
    for decada in resultados.index.levels[0]:
        dados_decada = resultados.loc[decada, var]
        plt.plot(dados_decada.index, dados_decada['mean'], label=f'{decada}s')

        plt.fill_between(
            dados_decada.index,
            dados_decada['mean'] - dados_decada['std'],
            dados_decada['mean'] + dados_decada['std'],
            alpha=0.2
        )

        plt.xlim(1, 120)
        plt.ylim(min_val-1, max_val+1)
        plt.xticks(np.arange(12, 121, 12))
        #plt.tight_layout()
        plt.title(f'{var.upper()} - médias e desvios padrão (sobreposição por década)', fontsize=16)
        plt.xlabel('Meses', fontsize=14)
        plt.ylabel(var, fontsize=14)
        plt.legend(fontsize=16)
        plt.grid()
        #plt.show()
        figname = f'decadas_{var}.png'       
        plt.savefig(figname, dpi=300, bbox_inches='tight')

exit()
