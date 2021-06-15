import numpy as np

p1 = [1.0,1.0]
p2 = [0.0,2.0]

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


a = cart2pol(p1[0],p1[1])
b = cart2pol(p2[0],p2[1])

print(np.degrees(b[1]))