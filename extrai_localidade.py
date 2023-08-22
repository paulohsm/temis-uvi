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

# Abrindo arquivo onde serão salvos os valores da radiacao
with open(localidade['nome']+'.csv', 'w', newline='') as arqcsv:
    escritor = csv.writer(arqcsv)
    escritor.writerow(['data', 'ief', 'dvc_nuvem', 'dec_nuvem', 'ddc_nuvem', 'dvc_limpo', 'dec_limpo', 'ddc_limpo'])

    # Iterando ao longo do anos, meses, dias, com variacao de 
    # numero de dias entre os meses e anos bissextos
    for aa in range(1980, 2000):
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

                #print('Carregando arquivo ' + caminho_ief)
                arquivo_ief = nc.Dataset(caminho_ief) # Daily erythemal UV index from MSR-2
                lats = arquivo_ief.variables['Latitudes'][:]
                lons = arquivo_ief.variables['Longitudes'][:]

                ilat = np.abs(lats - localidade['lat']).argmin()
                ilon = np.abs(lons - localidade['lon']).argmin()

                ief = arquivo_ief.variables['UVI_field'][ilat,ilon]

                #print('Carregando arquivo ' + caminho_dvc)
                arquivo_dvc = nc.Dataset(caminho_dvc) # Daily Vitamin-D UV dose from MSR-2
                dvc_nuvem = arquivo_dvc.variables['UVD_cloud-modified'][ilat,ilon]
                dvc_limpo = arquivo_dvc.variables['UVD_cloud-free'][ilat,ilon]

                #print('Carregando arquivo ' + caminho_dec)
                arquivo_dec = nc.Dataset(caminho_dec) # Daily Erythemal UV dose from MSR-2
                dec_nuvem = arquivo_dec.variables['UVD_cloud-modified'][ilat,ilon]
                dec_limpo = arquivo_dec.variables['UVD_cloud-free'][ilat,ilon]

                #print('Carregando arquivo ' + caminho_ddc)
                arquivo_ddc = nc.Dataset(caminho_ddc) # Daily DNA-damage UV dose from MSR-2
                ddc_nuvem = arquivo_ddc.variables['UVD_cloud-modified'][ilat,ilon]
                ddc_limpo = arquivo_ddc.variables['UVD_cloud-free'][ilat,ilon]

                #print('Escrevendo a data ' + ano + '-' + mes + '-' + dia + ' no .csv')
                escritor.writerow([ano+'-'+mes+'-'+dia, ief, dvc_nuvem, dec_nuvem, ddc_nuvem, dvc_limpo, dec_limpo, ddc_limpo])


