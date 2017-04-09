import numpy as np
#import pydotplus as pydot
from collections import Counter
from distance_utils import time_series_twed
import kmedoids
import pandas as pd


class KMedioidsSubsequenceTree:

    def __init__(self, max_level, prototype_subsequences_list,
                 distances, time_window, time_step,
                 branching_factor, weighted=True):
        self.time_window = time_window
        self.time_step = time_step
        self.max_level = max_level
        self.branching_factor = branching_factor
        #self.graph = pydot.Dot(graph_type='graph')
        self.query_ts = None
        self.query_score_chart = None
        self.node_shortcuts = None
        self.weights = None
        self.d_data_frame = None
        self._original_time_series_ids = None
        self._query_vector = None
        self.n_nodes = 0
        self._weighted = weighted
        prototype_subsequences = np.array(prototype_subsequences_list)
        self._build_tree(distances, prototype_subsequences)
        self._build_node_shorcuts()

    def populate_from_tree_sum(self, tree_list):
        self.weights = None
        self.d_data_frame = None
        self._original_time_series_ids = None
        self._query_vector = None
        local_leaves = [node for node in self.node_shortcuts if node.is_leaf]
        for local_leaf in local_leaves:
            local_leaf.generate_inverted_file()
        for tree in tree_list:
            tree_leaves = [node for node in tree.node_shortcuts if node.is_leaf]
            for local_leaf, tree_leaf in zip(local_leaves, tree_leaves):
                print('leaf')
                print(local_leaf.id)
                print(tree_leaf.id)
                local_leaf.add_to_inverted_file(tree_leaf.inverted_file)
        self._build_weights_vector()
        self._build_d_data_frame()

    def populate(self, db_time_series):
        self.weights = None
        self.d_data_frame = None
        self._original_time_series_ids = None
        self._populate_tree(db_time_series)
        self._build_weights_vector()
        self._build_d_data_frame()



    @property
    def n_subsequences(self):
        return len(self.db_subsequences_dict)


    @property
    def original_time_series_ids(self):
        if self._original_time_series_ids is None:
            self._original_time_series_ids = list(self.root.inverted_file)
        return self._original_time_series_ids

    @property
    def n_original_time_series(self):
        return len(self.original_time_series_ids)

    @property
    def query_vector(self):
        if self._query_vector is None:
            q_vector = np.array([node.q for node in self.node_shortcuts])
            q_norm = np.linalg.norm(q_vector)
            self._query_vector = q_vector / q_norm
        return self._query_vector

    @property
    def _queried_time_series_ids(self):
        return list(set().union(*self._queried_time_series_ids_iterator()))


    def prune(self):
        self._build_node_shorcuts(True)
        self._build_weights_vector()
        self._build_d_data_frame()

    def _queried_time_series_ids_iterator(self):
        for node in self.node_shortcuts:
            if node.is_leaf and node.n_query_subsequences > 0:
                yield node.inverted_file.keys()

    def get_next_subsequence_id(self):
        id_ = self.next_subsequence_id
        self.next_subsequence_id += 1
        return id_

    def make_query(self, time_series, timer=None):
        if timer is not None:
            timer.start()
        subsequences = time_series.run_sliding_window(self.time_window, self.time_step)
        if timer is not None:
            timer.stop()
            timer.start()
        for node in self.node_shortcuts:
            node.n_query_subsequences = 0
        if timer is not None:
            timer.stop()
            timer.start()
        self._query_vector = None
        for subsequence in subsequences:
            self.root.add_query_subsequence(subsequence)
        if timer is not None:
            timer.stop()
            timer.start()
       # not_zero_node_ids = np.where(self.query_vector != 0)[0]
        #not_zero_query_vector = self.query_vector[not_zero_node_ids]
        not_zero_ts_ids = self._queried_time_series_ids
        self.d_data_frame *= self.query_vector

       # not_zero_d_dataframe = self.d_data_frame.loc[not_zero_ts_ids, not_zero_node_ids]
        if timer is not None:
            timer.stop()
            timer.start()
        score = -self.d_data_frame.sum(axis=1).loc[not_zero_ts_ids]# -df.sum-np.sum(not_zero_query_vector*not_zero_d_dataframe.values, axis=1)
        #score = 2-2*score
        if timer is not None:
            timer.stop()
            timer.start()
        score.sort()
        result = score.index.values
        if timer is not None:
            timer.stop()
        return result

    def get_db_subsequences_dict(self):
        def _get_db_subsequences_dict():
            return self.db_subsequences_dict
        return _get_db_subsequences_dict

    def get_next_node_id(self):
        def _get_next_node_id():
            n_nodes = self.n_nodes
            self.n_nodes += 1
            return n_nodes
        return _get_next_node_id

    def get_original_time_series_ids(self):
        def _get_original_time_series_ids():
            return self.original_time_series_ids
        return _get_original_time_series_ids

    # def save_graph(self):
    #     self.generate_graph()
    #     self.graph.write_png('graph.png')
    #
    # def generate_graph(self):
    #     self.root.add_to_graph(None, self.graph)

    def _build_tree(self, distances, prototypes):
        self.root = Node(0, self.max_level, prototypes, distances, None,
                         None, self.get_next_node_id(),
                         self.get_original_time_series_ids(), self.branching_factor, weighted=self._weighted)

    def _populate_tree(self, db_time_series):
        print("populating tree")
        print('time window')
        print(self.time_window)
        print('time step')
        print(self.time_step)
        print(type(db_time_series))
        print(db_time_series)
        for i, ts in enumerate(db_time_series):
            print(ts)
            for subsequence in ts.run_sliding_window(self.time_window, self.time_step):
                #print(subsequence)
                self._add_subsequence(subsequence)
            print("{0} time series added".format(i))

    def _build_node_shorcuts(self, just_leaves=False):
        shortcut_dict = {}
        self.root.add_shortcut_to_dict(shortcut_dict)
        shortcut_list = [v for v in shortcut_dict.values()
                         if not just_leaves or v.is_leaf]
        self.node_shortcuts = shortcut_list

    def _build_weights_vector(self):
        weights_list = [node.weight for node in self.node_shortcuts]
        self.weights = np.array(weights_list)

    def _build_d_data_frame(self, just_leaves=False):
        print('{} nodes'.format(len(self.node_shortcuts)))
        print('building d list')
        d_list = [node.d_vector for node in self.node_shortcuts]
        print('DONE')
        print('building d matrix')
        d_matrix = np.column_stack(d_list)
        d_norm = np.linalg.norm(d_matrix, axis=1)
        d_matrix = (d_matrix.T / d_norm).T
        d_matrix[d_matrix == np.inf] = 0
        print('DONE')
        print('building d dataframe')
        self.d_data_frame = pd.DataFrame(np.nan_to_num(d_matrix),
                                       index=self.original_time_series_ids)
        print('DONE')

    def _add_subsequence(self, subsequence):
        self.root.add_db_subsequence(subsequence)

    def calculate_inverted_files(self):
        return self.root.inverted_file


class Node:

    next_id = 0

    def __init__(self, level, max_level, prototypes, distances, center,
                 parent, next_node_id_getter, original_time_series_ids_getter,
                 branching_factor, weighted=True):
        self.id = self.__class__.next_id
        self.__class__.next_id += 1
        self.level = level
        self._weighted = weighted
        self.max_level = max_level
        self.center = center
        self.parent = parent
        self.branching_factor = branching_factor
        self.get_original_time_series_ids_in_tree = original_time_series_ids_getter
        self._id = next_node_id_getter()
        parent_id = parent._id if parent is not None else None
        print("-- NODE {0} --".format(self._id))
        print("parent = {0}".format(parent_id))
        print("level {0}".format(level))
        print("prototypes length = {0}".format(len(prototypes)))
        shape = distances.shape if distances is not None else None
        print("distances shape = {0}".format(shape))
        print("")
        self.n_query_subsequences = 0
        self.children = None
        self._inverted_file = None
        if level + 1 == max_level or distances.shape[0] < self.branching_factor:
            self.generate_inverted_file()
        else:
            self._generate_children(distances, next_node_id_getter, prototypes)

    @property
    def is_leaf(self):
        return self.children is None

    @property
    def inverted_file(self):
        if self._inverted_file is None:
            inverted_file = Counter()
            for child in self.children:
                inverted_file += child.inverted_file
            self._inverted_file = inverted_file
        return self._inverted_file

    @property
    def n_original_time_series_in_node(self):
        print('getting n_original_time_series_in_node')
        n = len(self.inverted_file)
        print('DONE')
        return n

    @property
    def n_original_time_series_in_tree(self):
        print('getting n_original_time_series_in_tree...')
        n = len(self.get_original_time_series_ids_in_tree())
        print('DONE')
        return n

    @property
    def weight(self):
        if not hasattr(self, '_weight') or self._weight is None:
            print('Calculating weight in node {}... '.format(self.id))
            w = 0
            if self.n_original_time_series_in_node != 0:
                w = np.log(self.n_original_time_series_in_tree/
                           self.n_original_time_series_in_node)
            try:
                if not self._weighted:
                    w = 1
            except AttributeError:
                print("Attribute Error caught")
                print("weight = {0}".format(w))
            print('DONE')
            self._w = w
        return self._w

    @property
    def m_vector(self):
        print('building m vector in node {}'.format(self.id))
        m = np.zeros(self.n_original_time_series_in_tree)
        ids = self.get_original_time_series_ids_in_tree()
        indices = {id_: index for index, id_ in enumerate(ids)}
        for key, value in self.inverted_file.items():
            index = indices[key]
            m[index] = value
        print('DONE')
        return m

    @property
    def q(self):
        if self.n_query_subsequences is None:
            return None
        return self.n_query_subsequences*self.weight

    @property
    def d_vector(self):
        if not hasattr(self, '_d_vector') or self._d_vector is None:
            self._d_vector = self.weight*self.m_vector
        return self._d_vector

    def add_shortcut_to_dict(self, shortcut_dict):
        shortcut_dict[self._id] = self
        if not self.is_leaf:
            for child in self.children:
                child.add_shortcut_to_dict(shortcut_dict)

    def run_kmedoids(self, distances):
        center_indices, labels_dict = kmedoids.kMedoids(distances, self.branching_factor)
        labels = np.empty(distances.shape[0]).astype(int)
        for key, value in labels_dict.items():
            labels[value] = key
        return center_indices, labels

    def _generate_children(self, distances,
                           next_node_id_getter, prototypes):
        center_indices, labels = self.run_kmedoids(distances)
        cluster_centers = prototypes[center_indices]
        n_clusters = len(center_indices)
        children = []
        for cluster_label, center in zip(range(n_clusters),
                                              cluster_centers):
            indices = np.where(labels==cluster_label)[0]
            child_prototypes = prototypes[indices]
            child_distances = distances[indices][:, indices]
            child = Node(self.level + 1, self.max_level, child_prototypes,
                         child_distances, center,
                         self, next_node_id_getter,
                         self.get_original_time_series_ids_in_tree,
                         self.branching_factor)
            children.append(child)
        self.children = children


    def add_query_subsequence(self, subsequence):
        self.n_query_subsequences += 1
        if not self.is_leaf:
            distances = [time_series_twed(subsequence, node.center)
                        for node in self.children]
            nearest_child = self.children[np.argmin(distances)]
            nearest_child.add_query_subsequence(subsequence)

    def add_db_subsequence(self, subsequence):
        if self.is_leaf:
            counter = Counter({subsequence.original_id: 1})
            self._inverted_file += counter
        else:
            distances = [time_series_twed(subsequence, node.center)
                        for node in self.children]
            nearest_child = self.children[np.argmin(distances)]
            nearest_child.add_db_subsequence(subsequence)

    def generate_inverted_file(self):
        # original_time_series_id = (subsequence.original_id
        #                            for subsequence in prototypes)
        # self._inverted_file = Counter(original_time_series_id)
        self._inverted_file = Counter()

    def add_to_inverted_file(self, inverted_file):
        self._inverted_file += inverted_file

    # def add_to_graph(self, parent_graph_node, graph):
    #     graph_node = pydot.Node(str(self))
    #     graph.add_node(graph_node)
    #     if parent_graph_node is not None:
    #         graph.add_edge(pydot.Edge(parent_graph_node,
    #                                   graph_node))
    #     if self.children is not None:
    #         for child in self.children:
    #             child.add_to_graph(graph_node, graph)