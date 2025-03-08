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
        # Carrega os dados:
        self.dados_uv = self._carregar_dados()
        self._calcular_estatisticas()
        self._calcular_anomalias()

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
        self.estatisticas_diarias = self.dados_uv.resample('D', on='data').agg(
            ['mean', 'std', 'median', 'min', 'max']
        )

        # Estatísticas semanais
        self.estatisticas_semanais = self.dados_uv.resample('W', on='data').agg(
            ['mean', 'std', 'median', 'min', 'max']
        )

        # Estatísticas mensais
        self.estatisticas_mensais = self.dados_uv.resample('M', on='data').agg(
            ['mean', 'std', 'median', 'min', 'max']
        )

        # Estatísticas trimestrais
        self.estatisticas_trimestrais = self.dados_uv.resample('Q', on='data').agg(
            ['mean', 'std', 'median', 'min', 'max']
        )

        # Estatísticas anuais
        self.estatisticas_anuais = self.dados_uv.resample('Y', on='data').agg(
            ['mean', 'std', 'median', 'min', 'max']
        )

        def _calcular_anomalias(self):
            """
            Calcula os desvios em relação média nas diferentes escalas de tempo.
            """
            
            # Anomalias diárias
            self.anomalias_diarias = self.dados_uv.set_index('data') - self.estatisticas_diarias['mean']

            # Anomalias semanais 
            self.anomalias_semanais = self.dados_uv.set_index('data') - self.estatisticas_semanais['mean']

            # Anomalias mensais
            self.anomalias_mensais = self.dados_uv.set_index('data') - self.estatisticas_mensais['mean']

            # Anomalias trimestrais
            self.anomalias_trimestrais = self.dados_uv.set_index('data') - self.estatisticas_trimestrais['mean']

            # Anomalias anuais
            self.anomalias_anuais = self.dados_uv.set_index('data') - self.estatisticas_anuais['mean']

            