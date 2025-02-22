#!/bin/bash

urlbase="https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/msr2"
dirsaida="/run/media/santiago/ext2tb/dados/TEMIS_UVI/msr2_2023"

# Informacoes e acesso aos dados
#  Multi-Sensor Reanalysis MSR-2 (v2.0-2.2)
# https://www.temis.nl/uvradiation/UVarchive.php

# Variaveis baixadas
# ief = Daily erythemal UV index from MSR-2
# dec = Daily Erythemal UV dose from MSR-2
# dvc = Daily Vitamin-D UV dose from MSR-2
# ddc = Daily DNA-damage UV dose from MSR-2

# URL de exemplo:
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/msr2/2022/12/uvief20221231_msr.hdf

for aa in $(seq -w 1960 2022)
#for aa in $(seq -w 2023 2023)
do
        for mm in $(seq -w 1 12)
        do
                for dd in $(seq -w 1 31)
                do
                        for var in ief dec dvc ddc 
                        do
				url="${urlbase}/${aa}/${mm}/uv${var}${aa}${mm}${dd}_msr.hdf"
				echo "URL: ${url}"
				arq="${dirsaida}/uv${var}${aa}${mm}${dd}_msr.hdf"
				echo "Destino: ${arq}"
                                /usr/bin/curl ${url} -oC ${arq}
                        done
                done
        done
done


