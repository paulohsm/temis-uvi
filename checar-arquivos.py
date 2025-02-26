import netCDF4 as nc
import numpy as np
import csv
import os

# Caminho dos arquivos
dirent = '/run/media/santiago/ext2tb/dados/TEMIS_UVI/msr2_2023'
# dirent = '/home/santiago/Projetos/temis-uvi/backup_1960-1970_msr2'

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
localidade = {'nome': 'Baturite', 'lat': -4.343403, 'lon': -38.864222}

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

# Iterando ao longo do anos, meses, dias, com variacao de 
# numero de dias entre os meses e anos bissextos
for aa in range(2000, 2020):
    ano = str(aa)
    if aa % 4 == 0 and (aa % 100 != 0 or aa % 400 == 0):
        meses = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else: 
        meses = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for mm in range(0, 12):
        mes = str(mm+1).zfill(2)
        print('Processando arquivos do ano ' + ano + ', mês ' + str(mm+1).zfill(2) + '.')

        for dd in range(0, meses[mm]):
            dia = str(dd+1).zfill(2)
            caminho_ief = dirent + '/uvief' + ano + mes + dia + '_msr.hdf'
            caminho_dvc = dirent + '/uvdvc' + ano + mes + dia + '_msr.hdf'
            caminho_dec = dirent + '/uvdec' + ano + mes + dia + '_msr.hdf'
            caminho_ddc = dirent + '/uvddc' + ano + mes + dia + '_msr.hdf'

            if arquivoexiste(caminho_ief):
                dummy = []
            else:
                alertanaoexiste(caminho_ief)

            if arquivoexiste(caminho_dvc):
                dummy = []
            else:
                alertanaoexiste(caminho_dvc)

            if arquivoexiste(caminho_dec):
                dummy = []
            else:
                alertanaoexiste(caminho_dec)

            if arquivoexiste(caminho_ddc):
                dummy = []
            else:
                alertanaoexiste(caminho_ddc)



