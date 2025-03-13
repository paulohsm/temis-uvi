import os
import pandas as pd


class TemisUV:
    def __init__(self, caminho_arquivo_uv):
        """
        Classe TemisUV
        Fornece estatísticas dos dados de radiação solcar uv incidente
        a partir de dados gerados pelo TEMIS.
    
        Args:
        caminho_arquivo_uv (str): Caminho do arquivo uv contendo os dados.
        """    
        # Converte caminho para absoluto
        self.caminho_arquivo_uv = os.path.abspath(caminho_arquivo_uv)

        # Verifica a existência do arquivo de dados
        self._verificar_arquivo_uv()
        
        # Carrega os dados:
        self.dados_uv = self._carregar_dados()
        self._carregar_metadados()
        
        # Obtém os nomes das variáveis
        self.variaveis = self.dados_uv.columns.drop('data')
        
        # Lista as métricas estatísticas a serem calculadas
        self.estatisticas = ['mean', 'std', 'median', 'min', 'max']

        # Calcula estatísticas e anomalias
        self._calcular_estatisticas()
        self._calcular_anomalias()

    def _verificar_arquivo_uv(self):
        """
        Verifica a existência do arquivo .csv contendo os dados de radiação uv.
        """

        if not os.path.isfile(self.caminho_arquivo_uv):
            mensagem_arquivo_ausente = (
                f"Arquivo não encontrado: {self.caminho_arquivo_uv}\n"
                "Verifique o caminho de arquivo fornecido e tente novamente."
            )
            raise FileNotFoundError(mensagem_arquivo_ausente)
            
        print(f"Trabalhando com o arquivo {self.caminho_arquivo_uv}")

    def _carregar_metadados(self):
        """
        Carrega as informações de localidade do arquivo .csv e associa aos dados.
        """

        with open(self.caminho_arquivo_uv, 'r') as arquivo_uv:
            linha_localidade = arquivo_uv.readline().strip()

        info_localidade = linha_localidade.split(',')
        self.localidade = info_localidade[0].split('=')[1].strip().strip('"')
        self.latitude = float(info_localidade[1].split('=')[1].strip().strip('"'))
        self.longitude = float(info_localidade[2].split('=')[1].strip().strip('"'))

    def _carregar_dados(self):
        """
        Carrega dados de radiação solar uv incidente a partir do arquivo .csv.
        
        Returns:
        dados_uv.DataFrame: DataFrame contendo os dados carregados.
        """

        print(f"Carregando dados de {self.caminho_arquivo_uv}")
        return pd.read_csv(
            self.caminho_arquivo_uv,
            skiprows=1,
            na_values=-999.0,
            parse_dates=['data']
        )

    def _calcular_estatisticas(self):
        """
        Calcula máximos, mínimos, médias, medianas, desvios padrão nas
        escalas de tempo diária, semanal, mensal, trimestral e anual.
        """
      
        # Estatísticas diárias
        self.estatisticas_diarias = (
            self.dados_uv.resample('D', on='data')[self.variaveis]
                                     .agg(self.estatisticas)
                                     )

        # Estatísticas semanais
        self.estatisticas_semanais = (
            self.dados_uv.resample('W', on='data')[self.variaveis]
                                      .agg(self.estatisticas)
                                      )

        # Estatísticas mensais
        self.estatisticas_mensais = (
            self.dados_uv.resample('M', on='data')[self.variaveis]
                                     .agg(self.estatisticas)
                                     )

        # Estatísticas trimestrais
        self.estatisticas_trimestrais = (
            self.dados_uv.resample('Q', on='data')[self.variaveis]
                                         .agg(self.estatisticas)
                                         )

        # Estatísticas anuais
        self.estatisticas_anuais = (
            self.dados_uv.resample('Y', on='data')[self.variaveis]
                                    .agg(self.estatisticas)
                                    )

        def _calcular_anomalias(self):
            """
            Calcula os desvios em relação média nas diferentes escalas de tempo.
            """
            
            # Anomalias diárias
            self.anomalias_diarias = (
                self.dados_uv.set_index('data')[self.variaveis] - self.estatisticas_diarias.loc['mean']
            )
            self.anomalias_diarias = self.dados_uv.set_index('data') - self.estatisticas_diarias['mean']

            # Anomalias semanais 
            self.anomalias_semanais = self.dados_uv.set_index('data') - self.estatisticas_semanais['mean']

            # Anomalias mensais
            self.anomalias_mensais = self.dados_uv.set_index('data') - self.estatisticas_mensais['mean']

            # Anomalias trimestrais
            self.anomalias_trimestrais = self.dados_uv.set_index('data') - self.estatisticas_trimestrais['mean']

            # Anomalias anuais
            self.anomalias_anuais = self.dados_uv.set_index('data') - self.estatisticas_anuais['mean']

