from numpy import random

def rand_stations(stations,d1,d2):
    X = random.random_integers(d1,d2, stations)
    Y = random.random_integers(d1,d2, stations)
    return X, Y

X, Y = rand_stations(5, -40, 40)
output = open('station.dat','w')

for i in range(5):
    print >> output, 'ST'+str(i), X[i], Y[i], '0'

output.close()
