import h5py

from lib.stor import paths

batch_type='local-search'
batch_id='local-search_32'

dir_path = f'{paths.path("BATCH")}/{batch_type}'
filename = f'{dir_path}/{batch_type}.hdf5'
# traj_name = f'{batch_id}_traj'

# traj = load_trajectory(filename=filename, name=traj_name, load_all=2)
#
# res=get_results(traj, res_names=None)
# print(res)
f = h5py.File(filename, 'r+')
tr=list(f.keys())

# del f['local-search_37']
#
# # r=f[tr[0]]['results']['runs']
# r=f[tr[0]]['overview']['runs']['parameter_summary']
#
#
print(tr)
# # for k,v in r.items() :
# #     print(r[k].)
#
# # ff=Dataset()