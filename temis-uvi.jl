# Analysis of interannual variability of incident solar UV index radiation from TEMIS data.

# Original data source and documentation:
# https://www.temis.nl/uvradiation/product/uvi-uvd.html

# Guided by:
# https://towardsdatascience.com/read-csv-to-data-frame-in-julia-programming-lang-77f3d0081c14

println("aqui começa")

using CSV
using DataFrames

uvi_path = "/home/santiago/Projetos/temis-uvi/TEMIS_UVI_Acarau.csv"
uvi_file = CSV.File(uvi_path, header=1, delim=";")
uvi_data = DataFrame(uvi_file)

# CSV file column names:
# yyyy; mm; dd; date; uvief; uvdef; uvdvf; uvddf; ozone

#println(typeof(temis_f))
#for row in temis_f 
#    println("Valores: $(row.yyyy), $(row.mm), $(row.dd), $(row.uvief),  $(row.uvdef), $(row.uvdvf), $(row.uvddf), $(row.ozone)")
#    println("Valores: $(row.yyyy), $(row.mm), $(row.dd), $(row.ozone)")
#end

#println(uvi_file[1,1]) 

mi = 1
for row in uvi_file
    println("$(mi) | Date: $(row.date) | Ozone (DU): $(row.ozone)")
    local mi = mi + 1
end

# println(uvi_file.ozone[])

println("aqui termina")
