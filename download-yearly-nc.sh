#!/bin/bash

# Daily UV index and UV dose data in yearly netCDF files
# https://www.temis.nl/uvradiation/UVarchive/uvncfiles.php

# example file urls:
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc/2022/uvief2022_world.nc
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc/2022/uvdec2022_world.nc
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc/2022/uvdvc2022_world.nc
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc/2022/uvddc2022_world.nc
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc/2024/uvief2024_world.nc
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc/2024/uvief2024_world.nc
# https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc/2002/uvief2002_world.nc

urlbase="https://d1qb6yzwaaq4he.cloudfront.net/uvradiation/v2.0/nc"
dirsaida="/run/media/santiago/ext2tb/dados/TEMIS_UVI/operational"

# Downloaded variables
# uvief = clear-sky erythemal UV index & ozone field 
# uvdec = clear-sky & cloud-modified erythemal UV dose 
# uvdvc = clear-sky & cloud-modified vitamin-D UV dose 
# uvddc = clear-sky & cloud-modified DNA-damage UV dose

for aa in $(seq -w 2002 2024)
do
        for var in ief dec dvc ddc
        do
                url="${urlbase}/${aa}/uv${var}${aa}_world.nc"
                echo "URL: ${url}"
                arq="${dirsaida}/uv${var}${aa}_world.nc"
                echo "Destino: ${arq}"
                /usr/bin/curl ${url} -o ${arq}
		echo " "
        done
done
