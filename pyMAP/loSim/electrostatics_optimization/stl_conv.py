import numpy as np
# from stl import mesh
import trimesh as mesh
import skimage as skim
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import gem_tools as gem
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
# from matplotlib import cm
plt.ion()

cs_mesh = mesh.load_mesh(r'C:\Users\Jonny Woof\Google Drive\research\Projects\IMAP\references\imap 3d model\p10_inner_fringe.stl')
inertia_trans = cs_mesh.principal_inertia_transform
cs_mesh.apply_transform(inertia_trans)

esa_mesh = mesh.load_mesh(r'C:\Users\Jonny Woof\Google Drive\research\Projects\IMAP\references\imap 3d model\p10_inner_fringe.stl')
# esa_mesh = mesh.load_mesh(r'C:\Users\Jonny Woof\Google Drive\research\Projects\IMAP\references\imap 3d model\IMAP-LO Concept 3_ESA_STACK.stl')
esa_mesh.apply_transform(inertia_trans)

plane = [0,.5,-.45]

# plane = [0,.5,.5]
goot = [0,1]
col = 'red'
cs_parts = cs_mesh.section(plane_origin=cs_mesh.centroid,plane_normal=plane).discrete
slice1 = esa_mesh.section(plane_origin=cs_mesh.centroid, 
                 plane_normal=plane)
parts = slice1.discrete

part_slice = []
for part in parts:
	if np.all(part[:,1] > 0):
		r = np.sqrt(part[:,1]**2 + part[:,2]**2)
		plt.plot(part[:,0],r,color = col)
		part_slice += [np.transpose(np.stack((part[:,0],r)))]

#=====================================================
# group pieces together
R_MAX = 350.3377/2
scale = R_MAX/np.max(np.concatenate(part_slice)[:,1])*12
shift = np.min(np.concatenate(part_slice),axis = 0)*scale
part_groupers = []
img = np.zeros((3400,2200))
canvas_shape = img.shape
n = 0
for part in part_slice:
	draw_part = part*scale - shift
	locs = skim.draw.polygon(draw_part[:,0],draw_part[:,1],shape = canvas_shape)
	img[locs[0],locs[1]] = n+1
	n = n+1
# plt.imshow(img)

grouper = gem.part_group(np.transpose(img))
grouper.connect()
part_groups = grouper.part_groups

# for verts in [vert_parts[j[0]] for j in np.argwhere(part_groups[:,1]==i)]:

i = 0
part_names = {}
xlim = [min(np.concatenate(part_slice)[:,0]),max(np.concatenate(part_slice)[:,0])]
ylim = [min(np.concatenate(part_slice)[:,1]),max(np.concatenate(part_slice)[:,1])]
for group in np.unique(part_groups[:,1]):
	i+=1
	for part in [part_slice[j[0]] for j in np.argwhere(part_groups[:,1]==group)]:
		print(group)
		cmap = plt.cm.get_cmap('hsv')
		plt.plot(part[:,0],part[:,1],color = cmap(group/max(part_groups[:,1])))
		plt.xlim(xlim)
		plt.ylim(ylim)
	# plt.show()
	part_names[group] = input('Input Name of Part:')
	plt.close()

# fig,ax = plt.subplots()
# ax.add_collection(pat_group)


# part_names = {part_groups[24,0]:'outter ESA',part_groups[0,0]:'inner ESA',part_groups[20,0]:'p12 Elec',
# 				part_groups[8,0]:'ground can',part_groups[10,0]:'p9',part_groups[4,0]:'p3',
# 				part_groups[1,0]:'outer CS chamber',part_groups[11,0]:'CS'}
name_parts = dict((v,k) for k,v in part_names.items())

inner_esa_height = max(part_slice[int(name_parts['inner ESA']) - 1][:,0]) - min(part_slice[int(name_parts['inner ESA']) - 1][:,0])
scale = 46.7614/inner_esa_height
# R_MAX = 350.3377/2
# scale = R_MAX/np.max(np.concatenate(part_slice)[:,1])
# old_tip_loc = np.array([-101.72,93.85])
# old_tip_loc = np.array([-.102145,.09421])
for n in range(len(part_slice)):
	# part_slice[n] = part_slice[n]*scale - shift
	plt.plot(part_slice[n][:,0],part_slice[n][:,1])
x = input('Tip loc x:')
r = input('Tip loc r')
plt.close()
old_tip_loc = np.array([x,r]).astype(float)
new_tip_loc = np.array([25.7,94.285])
# scale = new_tip_loc[1]/old_tip_loc[1]
shift = old_tip_loc*scale - new_tip_loc
# sml_parts = gem.clean_verts(part_slice)
for n in range(len(part_slice)):
	part_slice[n] = part_slice[n]*scale - shift
	plt.plot(part_slice[n][:,0],part_slice[n][:,1])


#=====================================================
# strip down the number of points
big_part = []
for part in part_slice:
	big_part += [(part*10).astype(int)]
	plt.plot(big_part[-1][:,0],big_part[-1][:,1])

clean_verts = gem.clean_verts(big_part)
#=======================================================
n = 0
img[:,:] =0
for draw_part in big_part:
	locs = skim.draw.polygon(draw_part[:,0],draw_part[:,1],shape = canvas_shape)
	img[locs[0],locs[1]] = part_groups[n,1]
	n = n+1

out_verts = list(np.fliplr(vert)/10 for vert in clean_verts)
loc = 'mag.gem'
gem.print_verts(out_verts,loc,part_groups = part_groups,
				part_lable = part_names )

