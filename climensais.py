import pandas as pd

caminho = "/home/santiago/Projetos/temis-uvi/Maracanau.csv"
uv = pd.read_csv(caminho, skiprows=1, na_values=-999.0, parse_dates=['data'])

# novas colunas para diferentes fracionamentos do tempo
uv['ano'] = uv['data'].dt.year
uv['mes'] = uv['data'].dt.month
uv['est'] = uv['mes'] % 12 // 3 + 1

# secionando o intervalo de tempo em partes de 30 anos
uv['periodo'] = 3
uv.loc[(uv['ano'] >= 1960) & (uv['ano'] <= 1989), 'periodo'] = 1
uv.loc[(uv['ano'] >= 1990) & (uv['ano'] <= 2019), 'periodo'] = 2

# cálculo de métricas estatísticas
clim = uv.groupby(['periodo', 'mes'])[['ief', 'dec', 'dvc', 'ddc']].agg(['mean', 'median', 'std'])

print(clim.head())

print(clim.loc[1, ('ief', 'mean')])