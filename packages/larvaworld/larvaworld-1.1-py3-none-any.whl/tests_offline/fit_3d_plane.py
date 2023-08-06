import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def main():
    # Generate Data...
    # numdata = 100
    # x = np.random.random(numdata)
    # y = np.random.random(numdata)
    # z = x**2 + y**2 + 3*x**3 + y + np.random.random(numdata)
    df=pd.read_csv('results.csv')
    x=df['explore2exploit_bias'].values
    y=df['f_decay'].values
    z=df['deb_f_mean'].values

    # Fit a 3rd order, 2d polynomial
    m = polyfit2d(x,y,z)


    # Evaluate it on a grid...
    nx, ny = 100, 100
    xx, yy = np.meshgrid(np.linspace(x.min(), x.max(), nx),
                         np.linspace(y.min(), y.max(), ny))
    zz = polyval2d(xx, yy, m)

    # Plot
    plt.imshow(zz, extent=(x.min(), x.max(), y.max(), y.min()))
    plt.scatter(x, y, c=z)
    # plt.show()

    y0=np.array([0.6])
    x0=np.linspace(0.39,0.4,5)
    print(x0)
    print(polyval2d(x0, y0, m))

def polyfit2d(x, y, z, order=3):
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    ij = itertools.product(range(order+1), range(order+1))
    for k, (i,j) in enumerate(ij):
        G[:,k] = x**i * y**j
    m, _, _, _ = np.linalg.lstsq(G, z)
    return m

def polyval2d(x, y, m):
    order = int(np.sqrt(len(m))) - 1
    ij = itertools.product(range(order+1), range(order+1))
    z = np.zeros_like(x)
    for a, (i,j) in zip(m, ij):
        z += a * x**i * y**j
    return z

main()