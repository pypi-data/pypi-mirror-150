from larvaworld.lib.anal.plotting import plot_debs
from larvaworld.lib.model.larva import deb_default

d=[]

d.append(deb_default(starvation_days=[[0.8,7]]))
# d.append(deb_default(starvation_days=[[2,6]]))
# d.append(deb_default(starvation_days=[[2,5]]))
# d.append(deb_default(starvation_days=[[2,4]]))
# d.append(deb_default(starvation_days=[[2,3]]))
d.append(deb_default(starvation_days=[]))

# plot_debs(d, save_as=f'debs_{len(d)}x.png')
plot_debs(d, save_as=f'debs_{len(d)}x_death2.png')
# plot_debs(d, save_as=f'debs_{len(d)}x_minimal.png', mode='minimal')
plot_debs(d, save_as=f'debs_{len(d)}x_death2_minimal.png', mode='minimal')