#_______________________________________________________________________________________________
#The input of this program must be a transmittance .txt file from 300 to 2500 nm without header. 
#Decimals must be given with dots instead of commas.
#_______________________________________________________________________________________________

from scipy.interpolate import interp1d
import numpy as np

print ('--------------------------------------')
print ('       Solar transmittance            ')
print ('--------------------------------------')

#name = raw_input('Name of the .sp file: ') #add skiprows if the imput file has header
name ='Transmittace_00005'
x,y = np.loadtxt(name + '.sp',skiprows = 86, unpack = True)#Load Transmittance file
j,k = np.loadtxt('iso9845tot.txt', unpack = True)#Load solar irradiance spectrum
x = np.flipud(x) #PerkinElmer files start from 2500 to 300. we just reverse them with this
y = np.flipud(y)

T_int = interp1d(x, y, kind= 'linear') #Interpolation of transmittance
S_int = interp1d(j, k, kind= 'linear') #Interpolation of the solar spectrum

Wv = np.linspace(300, 2500, num =441, endpoint = True) #Creates wavelenght (nm) matrix (remember: pos.0=300 and pos.440->2500)
Transmittance= [None] * 441 #Creates a 441 element vector full of zeros, where we will write the Transmittance Spectrum
Solar= [None] * 441 #Creates a 441 element vector full of zeros, where we will write the Solar Irrandiance Spectrum
TS = [None] * 441 #Creates a 441 element vector full of zeros, where we will write Transmittance*Solar
###########
i = 0 #index for counting position in the vector/se incrementa de 1 en 1
l = 300 #index for knowing the wavelenght/se incrementa de 5 en 5
while (i <= 440): #441 elementos pero empieza a contar en 0, por eso solo hasta 440
	Transmittance[i] = T_int(l)
	Solar[i] = S_int(l)
	TS[i] = T_int(l) * S_int(l)
	i = i + 1
	l = l +5
############
Tsol = np.trapz(TS, Wv)/np.trapz(Solar, Wv)
print ("\n Tsol= "+ str(Tsol)+ " %")

