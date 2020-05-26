###this file read the values of the TXT file and returns in a separated vectors the float values, of latitude, longitude and altitude
#import matplotlib.pyplot as plt
import math
path="D:/Users/miles/Desktop/TT/logging.txt"
x=[]
y=[]
alt=[]

def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

with open(path) as f_o:    
    lines=f_o.readlines()
for co in range(len(lines)):
    b=lines[co]
    temp=b.rstrip().replace("["+str(co)+"]","")
    temp=temp.split(',')
    x.append(float(temp[0]))
    y.append(float(temp[1]))
    alt.append(float(temp[2]))

startp=x[0],y[0]
stopp=x[len(lines)-1],y[len(lines)-1]
print(len(lines)-1)
print("starting point {}".format(startp))
print("starting point {}".format(stopp))
distance = haversine(startp,stopp)
print("total distance {:.2f} meters".format(distance))

#print(distance)
#plt.plot(x)
#plt.ylabel('latitud')
#plt.axis([0, len(lines)-1, 0, 20])
#plt.show()
##plt.plot(y)
#plt.ylabel('longitud')
#plt.axis([0, len(lines)-1, 0, -100])
#plt.show()
#plt.plot(alt)
#plt.ylabel('altura')
#plt.axis([0, len(lines)-1, 0, 2500])
#plt.show()

