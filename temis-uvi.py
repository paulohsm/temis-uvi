# Analysis of interannual variability of incident solar UV index radiation from TEMIS data.

# Original data source and documentation:
# https://www.temis.nl/uvradiation/product/uvi-uvd.html

# Instructions from:
# https://realpython.com/python-csv/

#import csv

print('começa aqui...')

import numpy as np
uvi_path = '/home/santiago/Projetos/temis-uvi/TEMIS_UVI_Acarau.csv'
uvi_data = np.genfromtxt(uvi_path, delimiter=';', names=True, dtype=None, encoding=None)
print(uvi_data.dtype.names)

yy = uvi_data['yyyy']
mm = uvi_data['mm']
dd = uvi_data['dd']
dt = uvi_data['date']
ief = uvi_data['uvief']
uef = uvi_data['uvdef']
dvf = uvi_data['uvdvf']
ddf = uvi_data['uvddf']
ozo = uvi_data['ozone']

clim_ozo = []
for m in range(1,13):
    print(m)
    print(np.average(ozo[np.where(mm == m)]))
    np.append(clim_ozo, np.average(ozo[np.where(mm == m)]))
#    clim_ozo = np.average(ozo[np.where(mm == m)])


print(clim_ozo)

ijan = np.where(mm == 1)

print(ijan)

print(ozo[ijan])

print(np.average(ozo[ijan]))

print(range(1,12))
range(12)

for i in range(1, 12):
    print(i)

print('chegamos ao fim!')

