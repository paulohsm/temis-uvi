# Variations of UV index and doses for selected locations

This project consists in tools to statistically and climatologically analize TEMIS UVI data for selected locations. 

The clear-sky UV index is a measure for the effective UV irradiance (1 unit equals 25 mW/m2) reaching the Earth's surface.

The UV dose is the effective UV irradiance (given in kJ/m2) reaching the Earth's surface integrated over the day and taking the attenuation of the UV radiation due to clouds into account. The UV dose is computed for three different action spectra, i.e. for three different health effects: erythema (sunburn) of the skin, vitamin-D production in the skin and DNA-damage. 

Follow the links for more information:

https://www.temis.nl/uvradiation/UVindex.php

https://www.temis.nl/uvradiation/UVdose.php

https://www.temis.nl/uvradiation/UVarchive.php

For basic definitions of variables, see https://www.temis.nl/uvradiation/info/index.html.

# Data download

In order to extract a time series for a single location, one must first download the UV radiation products datasets provided by TEMIS' UV radiation monitoring archive (https://www.temis.nl/uvradiation/UVarchive.php). This is made by 'baixar-msr2.sh' bash script.

# Data check

After the hole archive os localy available, may be useful to check all files (one per day and per variable) really exists. This task is performed by "checar-arquivos.py".

# Location extraction

"extrai_localidade.py" is the python script that reads the entire archive and writes a .csv time series for (lat, lon) pair. 

# Decadal monthly means and standard deviations

For each variable, script "decadas.py" plots six decades superimposed curves of monthly means. Monthly standard deviations are added as shades following curves of means. 

# Monthly climatologies