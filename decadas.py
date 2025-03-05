import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Carregando dados
caminho = "/home/santiago/Projetos/temis-uvi/dados/Maracanau.csv"
uv = pd.read_csv(caminho, skiprows=1, na_values=-999.0, parse_dates=['data'])

# Metadados para utilização nos gráficos
siglas = uv.columns[1:].values
unidades = ['Índice UV', 'kJ/m2', 'kJ/m2', 'kJ/m2'] # 1  [ 1 UV index unit equals 25 mW/m2 ]
descricoes = ['Índice UV ao meio dia local', 
              'Dose diária UV - Vitamina D', 
              'Dose diária UV - Eritemal', 
              'Dose diária UV - Dano ao DNA']
minimos = [0., 7., 3.5, 2.]
maximos = [18., 17., 8.5, 6.]

# Dicionário com metadados das variáveis
variaveis = {
    'sigla': siglas, 
    'unidade': unidades,
    'descricao': descricoes,
    'minimo': minimos,
    'maximo': maximos
}

# Novas colunas para organizar por década e por mês
uv['decada'] = (uv['data'].dt.year // 10) * 10
uv['mes_na_decada'] = (uv['data'].dt.year % 10) * 12 + uv['data'].dt.month

# Calculando médias e desvios padrão mensais
decadas = uv.groupby(['decada', 'mes_na_decada']).agg(['mean', 'std'])

# Gerando os gráficos, por variável
for i, variavel in enumerate(variaveis['sigla']):
    plt.figure(figsize=(19.2, 10.8), dpi=320)

    # Linhas para delimitar os anos
    for ano in range(12, 121, 12):
        plt.axvline(x=ano, color='gray', linestyle='--', linewidth=0.5)

    # Customizações
    plt.xticks(np.arange(3, 121, 3), ['M', 'J', 'S', 'D'] * 10)
    plt.title(
        f"{variaveis['descricao'][i]} "
        "(médias e desvios padrão - décadas sobrepostas)"
    )
    plt.xlim(1, 120)
    plt.ylabel(variaveis['unidade'][i])
    plt.ylim(variaveis['minimo'][i], variaveis['maximo'][i])
    plt.tight_layout()

    # Gerando as curvas para cada década
    for decada in decadas.index.levels[0][0:6]:
        dados_decada = decadas.loc[decada, variavel]
        plt.plot(dados_decada.index, dados_decada['mean'], label=f'{decada}s')

        # Áreas correspondentes aos desvios padrão
        plt.fill_between(
            dados_decada.index,
            dados_decada['mean'] - dados_decada['std'],
            dados_decada['mean'] + dados_decada['std'],
            alpha=0.2
        )
    
    # Acabamento final e salvamento do arquivo do gráfico
    plt.legend()
    plt.savefig(f'graficos/decadas_{variavel}.png')
    plt.close()