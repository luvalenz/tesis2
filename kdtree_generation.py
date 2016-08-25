import dill
import os
from sklearn.neighbors import KDTree

if __name__ == '__main__':
    #LOAD SUBSEQUENCE TREE
    root = '/home/lucas/tesis2'
    model_name = 'sequence_tree_20000samples_20levels'
    st_path = os.path.join(root, 'models/{0}.dill'.format(model_name))
    output_path = os.path.join(root,
                               'kdtree_models/{0}_kd_tree.dill'.format(model_name))
    with open(st_path, 'rb') as f:
        tree = dill.load(f)
    data_frame = tree.d_data_frame
    data_set = data_frame.values
    ids = data_frame.index
    kd_tree = KDTree(data_set)
    output = {'ids': ids, 'kd_tree': kd_tree}
    with open(output_path, 'wb') as f:
        dill.dump(output, f)




