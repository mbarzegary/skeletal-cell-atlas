import loompy
import pandas as pd
import h5py

ds = loompy.connect("SCA_v.0.5.0_preprint.loom")

umap_1 = ds.ca["UMAP_1"]
umap_2 = ds.ca["UMAP_2"]
umap_3d_1 = ds.ca["umap_3d_1"]
umap_3d_2 = ds.ca["umap_3d_2"]
umap_3d_3 = ds.ca["umap_3d_3"]
tech = ds.ca["Tech"]
organism = ds.ca["Organism"]
origin = ds.ca["Origin"]
devtp = ds.ca["DevTP"]
identity = ds.ca["Identity"]
author = ds.ca["Author"]

data = {'umap_1': umap_1, 'umap_2': umap_2,
        'umap_3d_1': umap_3d_1, 'umap_3d_2': umap_3d_2, 'umap_3d_3': umap_3d_3,
        'tech': tech, 'organism': organism, 'origin': origin,
        'devtp': devtp, 'identity': identity, 'author': author}
df = pd.DataFrame(data=data)

df.to_csv('data.csv', index=False)

genes = ds.ra["Gene"]
data = {'gene': genes}
df = pd.DataFrame(data=data)
df.to_csv('genes.csv', index=False)

# hf = h5py.File("matrix.h5", 'w')
# # hf.create_dataset('data', data=ds[:,:], compression="gzip")
# hf.create_dataset('data', data=ds[:,:])
# hf.close()

ds.close()
