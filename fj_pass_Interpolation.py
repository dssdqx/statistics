import os
import pandas as pd
import re
import csv
import numpy as np

# заполняем пропуски в значениях координат xy, по соседним значениям, сохраняя поступательную последовательность 

path = os.path.abspath(os.curdir)
tab = input("таблица: ")

#tab = "EVENT_PL1_KP840000-880000_01_revB.csv"
r_tab = pd.read_csv((f'{tab}'), sep = ",")

fix_tab = pd.DataFrame(r_tab, columns = ['FJ Number', 'Easting', 'Northing'])
fix_tab.rename(columns={'FJ Number': 'FJ'}, inplace=True)


k = len(fix_tab)
fix_tab = fix_tab.dropna(subset = ["FJ"])
fix_tab = fix_tab.sort_values('FJ') 
dl = 10 


fix_tab.reset_index(drop= True , inplace= True ) 

start1 = fix_tab["FJ"][0][:]  
start = int(start1[dl-5:dl])                        

end1 = fix_tab["FJ"].value_counts().index[-1]
end = int(end1[dl-5:dl])

name = fix_tab["FJ"][10][0:dl-5]



lst_index = [i for i in range(start, end + 1)]
lst_now = []
for i in fix_tab["FJ"]:
	lst_now.append(int(i[dl-5:dl]))


print("sum : ", len(lst_now) - len(lst_index))

lst_interpolation =[]
lst_numbers = []

for i in lst_index:
	if i not in lst_now:
		lst_interpolation.append(name + str(i))
		lst_numbers.append(int(i))


lst_numbers.sort()

print("Пропуски в fj: ", *lst_interpolation, sep = "\n")



i = 0
while i < len(lst_numbers):  
	#print(name + str(lst_numbers[i]-1))
	fix_tab.loc[k+1 +i] = [lst_interpolation[i], np.nan, np.nan]
	i += 1	

fix_tab = fix_tab.sort_values('FJ') 
fix_tab.reset_index(drop= True , inplace= True )    

fix_tab["Easting"] = fix_tab["Easting"].interpolate()    
fix_tab["Northing"] = fix_tab["Northing"].interpolate()

fix_tab["Northing"] = fix_tab["Northing"].round(2)
fix_tab["Easting"] = fix_tab["Easting"].round(2)

#passes = open("passes_FJ.csv", "w")




rezult = pd.DataFrame(columns=['FJ', 'Easting', 'Northing'])


i = 0
while i < len(lst_interpolation):
	a = fix_tab.loc[(fix_tab['FJ'] == lst_interpolation[i])]
	rezult = rezult.append(a, ignore_index = True )
	#print(a)
	i += 1


rezult.rename(columns={'FJ': 'FJ Number'}, inplace=True)


rezult.to_csv(os.path.join(f"passes_FJ.csv"), sep = ",", index = False )

print(rezult)

print(f"таблица тут - {path}\\passes_FJ.csv")


u_input = input("Ready! ")




