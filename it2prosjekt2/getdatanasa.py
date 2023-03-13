#from astropy.time import Time
from astroquery.jplhorizons import Horizons #bibliotek fra Nasa som henter informasjon om planeter i sanntid
import math 
import csv 

obj = Horizons(id=3, location="@sun", id_type='id').vectors()
speedvals, distvals = [], []

#dekomponerer vektorene
def realspeed2(vx, vy, vz):
    normen2= math.sqrt(vx**2 + vy**2 + vz**2) * 149597870691 / (60*60*24)
    return normen2
def reald(ipsum, dolor, sit):
    normen = math.sqrt(ipsum**2 + dolor**2 + sit**2)
    return normen

for i in range(1, 5): #henter informasjon om planeter fra merkur frem til mars
    obj = Horizons(id=i, location="@sun", id_type='id').vectors()
    speedvals.append(realspeed2(obj["vx"], obj["vy"], obj["vz"]))
    distvals.append(reald(float(obj["x"]), float(obj["y"]), float(obj["z"])))

#lagrer en csv fil med den uthentet data
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(0, 4):
        writer.writerow([speedvals[i], distvals[i]])

file.close()

print(obj['m'])