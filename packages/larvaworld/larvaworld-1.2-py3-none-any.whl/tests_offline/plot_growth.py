from lib.anal.plotting import plot_debs, plot_endpoint_params
from lib.model.larva.deb import deb_default, deb_dict
from lib.stor.managing import get_datasets

deb=True
if deb :
    d=get_datasets('SimGroup', names=['RvS_2l_120h'], last_common='single_runs/growth_2x')[0]



    plot_endpoint_params(datasets=[d], labels=[d.id], mode='deb')
    deb_dicts= [deb_dict(d, id) for id in d.agent_ids]+[deb_default()]
    plot_debs(deb_dicts=deb_dicts,save_to=d.plot_dir, save_as='comparative_deb.pdf')
    plot_debs(deb_dicts=deb_dicts,save_to=d.plot_dir, save_as='comparative_deb_minimal.pdf', mode='minimal')
    plot_debs(deb_dicts=deb_dicts[:-1],save_to=d.plot_dir, save_as='deb.pdf')
    plot_debs(deb_dicts=deb_dicts[:-1],save_to=d.plot_dir, save_as='deb_f.pdf', mode='f')
    plot_debs(deb_dicts=deb_dicts[:-1],save_to=d.plot_dir, save_as='deb_minimal.pdf', mode='minimal')
