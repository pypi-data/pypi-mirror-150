from lib.anal.plotting import plot_debs
from lib.model.larva.deb import deb_default

# plot_debs(deb_dicts=[deb_default(f=i, id=f'f={i}') for i in [1,2,3,4,5]], save_as='comparative_deb_f.png')

import numpy as np
import matplotlib.pyplot as plt

if False :
    fr=2
    dur=10 # seconds
    c=1 # f decay coef
    df=1 # f increment on success
    EEB=1


    for dt in [0.5, 0.1, 0.05] :
        c_exp=np.exp(-c*dt)
        fdur = int(1 / (fr * dt))
        f = 0
        Nticks = int(dur / dt)
        trange = np.linspace(0,dur,Nticks)
        fs = np.zeros(Nticks) * np.nan
        for i in range(Nticks):
            if i%fdur==0 :
                if np.random.uniform(0, 1, 1) <= EEB:
                    f+=df
            # else :
            f *= c_exp
            fs[i]=f
        plt.plot(trange, fs)

        print(np.mean(fs))
    plt.show()




    # raise


f_fr=2
c_fr=1.5
cdur0=2
# dt=0.01
df=1*0.5
c=0.1 # f decay coef
dur=10000 #seconds

EEB=0.32
def decide(f) :
    if np.random.uniform(0, 1, 1) <= EEB:
        s = 0
        f += df
    else:
        s = 1
    return s,f

for dt in [0.1] :
# for dt in [0.1, 0.05, 0.01] :
    # fdur=int(1/(fr*dt))c_exp=np.exp(-c*dt)
    c_exp=np.exp(-c*dt)
    fdur = int(1 / (f_fr * dt))
    # cdur = int(1 / (c_fr * dt))
    cdur = int(cdur0 / dt)
    f=0
    Nticks=int(dur/dt)
    fs=np.zeros(Nticks)*np.nan
    s=0
    f_t=0
    c_t=0
    # f_t=0
    for i in range(Nticks) :
        if s==0 :
            f_t+=1
            if f_t==fdur :
                f_t=0
                s, f =decide(f)

        elif s==1 :
            c_t += 1
            if c_t==cdur :
                c_t=0
                s, f = decide(f)
        f *= c_exp
        fs[i]=f

    print(np.mean(fs))

plt.plot(fs)
plt.show()