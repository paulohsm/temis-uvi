import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.dates as mdates

# Trazendo dados do arquivo
caminho = "/home/santiago/Projetos/temis-uvi/dados/Maracanau.csv"
uv = pd.read_csv(caminho, skiprows=1, na_values=-999.0, parse_dates=['data'])
vars = uv.columns[1:]

# Agrupando por ano e por dia do ano
uv['ano'] = uv['data'].dt.year
uv['dia'] = uv['data'].dt.day_of_year

# Separando períodos de 30 anos 
uv['periodo'] = '2020 em diante'
uv.loc[(uv['ano'] >= 1960) & (uv['ano'] <= 1989), 'periodo'] = '1960-1989'
uv.loc[(uv['ano'] >= 1990) & (uv['ano'] <= 2019), 'periodo'] = '1990-2019'
uv = uv[uv['periodo'].isin(['1960-1989', '1990-2019'])]

# Função para cálculo das tendências
def calcular_tendencias(dados):
    X = dados['ano'].values.reshape(-1, 1)
    tendencias = {}
    for variavel in vars:
        dados_limpos = dados.dropna(subset=[variavel])
        if len(dados_limpos) > 1:
           y = dados_limpos[variavel].values
           modelo = LinearRegression()
           indices_X = np.where(np.isin(dados['ano'], dados_limpos['ano']))[0]
           X_limpo = X[indices_X]
           #X_limpo = X[dados_limpos.index.to_numpy() - dados.index.to_numpy()[0]]
           modelo.fit(X_limpo, y)
           tendencias[variavel] = modelo.coef_[0]
        else:
           tendencias[variavel] = no.nan
        #y = dados[variavel].values
        #modelo = LinearRegression()
        #modelo.fit(X, y)
        #tendencias[variavel] = modelo.coef_[0]
    return tendencias

# Armazenando as tendêncas calculadas em um dataframe
tendencias = pd.DataFrame(index=range(1, 367), 
                          columns=['dia'] + 
                          [f'tend_p1_{var}' for var in vars] +
                          [f'tend_p2_{var}' for var in vars])

 # Calculando tendências para cada dia do ano
for dia in range(1, 367):
    dados_dia = uv[uv['dia'] == dia]

    dados_p1 = dados_dia[dados_dia['periodo'] == '1960-1989']
    if not dados_p1.empty: 
      tendencias_p1 = calcular_tendencias(dados_p1)
    else:
      tendencias_p1 = {var: np.nan for var in vars}

    dados_p2 = dados_dia[dados_dia['periodo'] == '1990-2019']
    if not dados_p2.empty:
       tendencias_p2 = calcular_tendencias(dados_p2)
    else:
       tendencias_p2 = {var: np.nan for var in vars}

    tendencias.loc[dia - 1] = [dia] + [tendencias_p1[var] for var in vars] + [tendencias_p2[var] for var in vars]

# Removendo dias sem dados
tendencias = tendencias.dropna()
tendencias = tendencias.sort_values(by='dia')

datas = [datetime(2023, 1, 1) + pd.Timedelta(days=int(dia)) for dia in tendencias.index]

titulos = ['Índice UV (ao meio dia)',
           'Dose UV diária eritemal', 
           'Dose UV diária de ativação da Vit. D',
           'Dose UV diária de dano ao DNA']

# Produzindo os gráficos
for i, variavel in enumerate(vars):
    #plt.figure(figsize=(19.2, 10.8), dpi=320)
    ax = plt.gca()

    plt.plot(datas, tendencias[f'tend_p1_{variavel}'], label='1960-1989')
    plt.plot(datas, tendencias[f'tend_p2_{variavel}'], label='1990-2019')

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    plt.title(f'Tendências de {titulos[i]} por dia do ano')
    plt.xlabel('Dia do ano')
    plt.xlim(min(datas), max(datas))
    plt.ylabel('Coeficiente de inclinação (tendência)')
    plt.ylim(-0.04, 0.04)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'graficos/tendencias_{variavel}.png')
    plt.close()