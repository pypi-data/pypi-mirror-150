import numpy as np
from shapely.geometry import Polygon, LineString
from shapely.ops import split

N = 5
r=[5/11, 6/11]

def body(points, start=[1,0], stop=[0,0]) :
    xy=np.zeros([len(points)*2+2,2])*np.nan
    xy[0,:]=start
    xy[len(points)+1,:]=stop
    for i in range(len(points)) :
        x,y=points[i]
        xy[1+i,:] = x,y
        xy[-1-i,:] = x,-y
    return xy

def segment_body(N, xy0, seg_ratios=None, centered=True):
    if seg_ratios is None :
        seg_ratios = [1 / N] * N
    p = Polygon(xy0)
    ps=[p]
    for i, (r, cum_r) in enumerate(zip(seg_ratios, np.cumsum(seg_ratios))) :
        l = LineString([(cum_r, -10), (cum_r, 10)])
        new_ps=[]
        for p in ps :
            new_p = [new_p for new_p in split(p, l)]
            new_ps+=new_p
        ps=new_ps
    ps.sort(key=lambda x: x.exterior.xy[0], reverse=True)
    ps=[p.exterior.coords.xy for p in ps]
    ps=[np.array([[x,y] for x,y in zip(xs,ys)]) for xs,ys in ps]
    if centered :
        for i,(p, r,cum_r) in enumerate(zip(ps,seg_ratios, np.cumsum(seg_ratios))) :
            # print(p,r,cum_r)
            ps[i] -= [1-cum_r+r/2, 0]
    return ps


points=np.array([[0.9,0.1],[0.5, 0.11], [0.05,0.1]])

xy0=body(points)

ps=segment_body(N, xy0, seg_ratios=None, centered=True)

# print(ps)



import matplotlib.pyplot as plt

r = 1.5
for i in range(len(ps)) :
    # plt.plot(*ps[i].exterior.xy)
    plt.plot(ps[i][:, 0], ps[i][:, 1])
    plt.xlim([-r, r])
    plt.ylim([-r, r])
plt.show()
