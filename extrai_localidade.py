import netCDF4 as nc
import numpy as np
import csv
import os
from datetime import datetime

# Variaveis baixadas
# ief = Daily erythemal UV index from MSR-2
# dvc = Daily Vitamin-D UV dose from MSR-2
# dec = Daily Erythemal UV dose from MSR-2
# ddc = Daily DNA-damage UV dose from MSR-2

# Fonte dos dados:
# Archives of the UV radiation monitoring products
# Multi-Sensor Reanalysis MSR-2 (v2.0-2.2) 
# https://www.temis.nl/uvradiation/UVarchive.php

# Lendo arquivos netCDF4 com python e outras dicas fundamentais:
# https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/
# http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html

# Coords Recepcao IFCE Baturite:
# latitude = 4°20'36.25"S = -4.343403
# longitude = 38°51'51.20"O = -38.864222
#localidade = {'nome': 'Baturite', 'lat': -4.343403, 'lon': -38.864222}
# 
# Coords Portaria IFCE Maracanau:
# latitude = 3°52'20.2"S = -3.8722845
# longitude = 38°36'38.4"W = -38.6113503
localidade = {'nome': 'Maracanau', 'lat': -3.8722845, 'lon': -38.6113503}

# Anos inicial e final
anoi = 1960
anof = 2022

# Caminho dos arquivos
dirent = '/run/media/santiago/ext2tb/dados/TEMIS_UVI/msr2_2023'
# dirent = '/home/santiago/Projetos/temis-uvi/backup_1960-1970_msr2'

# testando a existencia do arquivo de origem dos dados (netcdf)
def arquivoexiste(meuarquivo):
    try:
        with open(meuarquivo, 'r'):
            pass
    except FileNotFoundError:
        return False
    else:
        return True

def alertanaoexiste(meuarquivo):
    print('ALERTA! Arquivo nao encontrado: ' + meuarquivo)

# Localizando as coordenadas mais proximas
arquivo_coords = dirent + '/uvief' + str(anoi) + '0101_msr.hdf'
if arquivoexiste(arquivo_coords): 
    dados_coords = nc.Dataset(arquivo_coords)
    lats = dados_coords.variables['Latitudes'][:]
    lons = dados_coords.variables['Longitudes'][:]
    ilat = np.abs(lats - localidade['lat']).argmin()
    ilon = np.abs(lons - localidade['lon']).argmin()
else:
    alertanaoexiste(arquivo_coords)
dados_coords.close()

# Lista de datas sem dados:
semdado = -999.0
semdados = []

print('Extração das variáveis de radiação UV dos dados globais TEMIS para a ')
print('localidade: ' + localidade['nome'] + ', lat = ' + str(lats[ilat]) + ', lon = ' + str(lons[ilon]) + '.')
print('Ano inicial: ' + str(anoi) + ', ano final: ' + str(anof) + '.')
print('Caminho dos arquivos de entrada:')
print(dirent)
print(' ')

# Abrindo arquivo onde serão salvos os valores da radiacao
with open(localidade['nome']+'.csv', 'w', newline='') as arqcsv:
    escritor = csv.writer(arqcsv)
    escritor.writerow(['localidade = ' + localidade['nome'], ', latitude = ' + str(lats[ilat]), ', longitude = ' + str(lons[ilon])])
    escritor.writerow(['data', 'ief', 'dvc_nuvem', 'dec_nuvem', 'ddc_nuvem', 'dvc_limpo', 'dec_limpo', 'ddc_limpo'])

    # Iterando ao longo do anos, meses, dias, com variacao de 
    # numero de dias entre os meses e anos bissextos
    for aa in range(anoi, anof):
        ano = str(aa)
        if aa % 4 == 0 and (aa % 100 != 0 or aa % 400 == 0):
            meses = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else: 
            meses = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for mm in range(0, 12):
            mes = str(mm+1).zfill(2)
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(agora + ' | ' + 'Processando arquivos do ano ' + ano + ', mês ' + str(mm+1).zfill(2) + '.')

            for dd in range(0, meses[mm]):
                dia = str(dd+1).zfill(2)
                amd = ano + '-' + mes + '-' + dia # aaaa-mm-dd
                caminho_ief = dirent + '/uvief' + ano + mes + dia + '_msr.hdf'
                caminho_dvc = dirent + '/uvdvc' + ano + mes + dia + '_msr.hdf'
                caminho_dec = dirent + '/uvdec' + ano + mes + dia + '_msr.hdf'
                caminho_ddc = dirent + '/uvddc' + ano + mes + dia + '_msr.hdf'

                #print('Carregando arquivo ' + caminho_ief)
                if arquivoexiste(caminho_ief):
                    arquivo_ief = nc.Dataset(caminho_ief) # Daily erythemal UV index from MSR-2
                    fator_escala = arquivo_ief.variables['UVI_field'].Scale_factor
                    ief = arquivo_ief.variables['UVI_field'][ilat,ilon] * fator_escala
                    arquivo_ief.close()
                else:
                    alertanaoexiste(caminho_ief)
                    ief = semdado
                    semdados.append(amd)
                    semdados.append('UVI_field')

                #print('Carregando arquivo ' + caminho_dvc)
                if arquivoexiste(caminho_dvc):
                    arquivo_dvc = nc.Dataset(caminho_dvc) # Daily Vitamin-D UV dose from MSR-2
                    fator_escala = arquivo_dvc.variables['UVD_cloud-free'].Scale_factor
                    dvc_nuvem = arquivo_dvc.variables['UVD_cloud-modified'][ilat,ilon] * fator_escala
                    dvc_limpo = arquivo_dvc.variables['UVD_cloud-free'][ilat,ilon] * fator_escala
                    arquivo_dvc.close()
                else:
                    alertanaoexiste(caminho_dvc)
                    dvc_nuvem = semdado
                    dvc_limpo = semdado
                    semdados.append(amd)
                    semdados.append('UVD_cloud-modified')
                    semdados.append('UVD_cloud-free')

                #print('Carregando arquivo ' + caminho_dec)
                if arquivoexiste(caminho_dec):
                    arquivo_dec = nc.Dataset(caminho_dec) # Daily Erythemal UV dose from MSR-2
                    fator_escala = arquivo_dec.variables['UVD_cloud-free'].Scale_factor
                    dec_nuvem = arquivo_dec.variables['UVD_cloud-modified'][ilat,ilon] * fator_escala
                    dec_limpo = arquivo_dec.variables['UVD_cloud-free'][ilat,ilon] * fator_escala
                    arquivo_dec.close()
                else:
                    alertanaoexiste(caminho_dec)
                    dec_nuvem = semdado
                    dec_limpo = semdado
                    semdados.append(amd)
                    semdados.append('UVD_cloud-modified')
                    semdados.append('UVD_cloud-free')

                #print('Carregando arquivo ' + caminho_ddc)
                if arquivoexiste(caminho_ddc):
                    arquivo_ddc = nc.Dataset(caminho_ddc) # Daily DNA-damage UV dose from MSR-2
                    fator_escala = arquivo_ddc.variables['UVD_cloud-free'].Scale_factor
                    ddc_nuvem = arquivo_ddc.variables['UVD_cloud-modified'][ilat,ilon] * fator_escala
                    ddc_limpo = arquivo_ddc.variables['UVD_cloud-free'][ilat,ilon] * fator_escala
                    arquivo_ddc.close()
                else:
                    alertanaoexiste(caminho_ddc)
                    ddc_nuvem = semdado
                    ddc_limpo = semdado
                    semdados.append(amd)
                    semdados.append('UVD_cloud-modified')
                    semdados.append('UVD_cloud-free')

                #print('Escrevendo a data ' + ano + '-' + mes + '-' + dia + ' no .csv')
                #escritor.writerow([ano+'-'+mes+'-'+dia, ief, dvc_nuvem, dec_nuvem, ddc_nuvem, dvc_limpo, dec_limpo, ddc_limpo])
                escritor.writerow([ano+'-'+mes+'-'+dia, ief, dvc_limpo, dec_limpo, ddc_limpo])

print('Dados faltando:')
for itemfaltando in semdados:
    print(itemfaltando)


