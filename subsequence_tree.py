import numpy as np
from sklearn.cluster import AffinityPropagation
#import pydotplus as pydot
from collections import Counter
from distance_utils import time_series_twed


class SubsequenceTree:

    def __init__(self, max_level, prototype_subsequences_list,
                 affinities, db_time_series):
        self.max_level = max_level
        #self.graph = pydot.Dot(graph_type='graph')
        self.query_ts = None
        self.query_score_chart = None
        self.node_shortcuts = None
        self.weights = None
        self.d_matrix = None
        self._original_time_series_ids = None
        self._query_vector = None
        self.n_nodes = 0
        prototype_subsequences = np.array(prototype_subsequences_list)
        self._build_tree(affinities, prototype_subsequences)
        self._populate_tree(db_time_series)
        self._build_node_shorcuts()
        self._build_weights_vector()
        self._build_d_matrix()

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

    def get_next_subsequence_id(self):
        id_ = self.next_subsequence_id
        self.next_subsequence_id += 1
        return id_

    def make_query(self, time_series):
        subsequences = time_series.run_sliding_window()
        for node in self.node_shortcuts:
            node.n_query_subsequences = 0
        self._query_vector = None
        for subsequence in subsequences:
            self.root.add_query_subsequence(subsequence)
        not_zero_node_ids = np.where(self.query_vector != 0)[0]
        not_zero_query_vector = self.query_vector[not_zero_node_ids]
        not_zero_d_matrix = self.d_matrix[:, not_zero_node_ids]
        score = np.sum(not_zero_query_vector*not_zero_d_matrix, axis=1)
        return 2-2*score


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

    def get_node_d_vector(self, node_id):
        def _get_node_d_vector():
            return self.d_matrix[:, node_id]
        return _get_node_d_vector

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

    def _build_tree(self, affinities, prototypes):
        self.root = Node(0, self.max_level, prototypes, affinities, None,
                         None, self.get_next_node_id(),
                         self.get_original_time_series_ids())

    def _populate_tree(self, db_time_series):
        for ts in db_time_series:
            for subsequence in ts.run_sliding_window():
                self._add_subsequence(subsequence)

    def _build_node_shorcuts(self):
        shortcut_dict = {}
        self.root.add_shortcut_to_dict(shortcut_dict)
        shortcut_list = [shortcut_dict[i] for i in range(self.n_nodes)]
        self.node_shortcuts = shortcut_list

    def _build_weights_vector(self):
        weights_list = [node.weight for node in self.node_shortcuts]
        self.weights = np.array(weights_list)

    def _build_d_matrix(self):
        d_list = []
        for node in self.node_shortcuts:
            d_list.append(node.d_vector)
        d_matrix = np.column_stack(d_list)
        d_norm = np.linalg.norm(d_matrix, axis=1)
        d_matrix = (d_matrix.T / d_norm).T
        d_matrix[d_matrix == np.inf] = 0
        self.d_matrix = np.nan_to_num(d_matrix)

    def _add_subsequence(self, subsequence):
        id_ = subsequence._id
        self.db_subsequences_dict[id_] = subsequence
        self.db_subsequences_ids.append(id_)
        self.root.add_db_subsequence(subsequence)


class Node:

    def __init__(self, level, max_level, prototypes, affinities, center,
                 parent, next_node_id_getter, original_time_series_ids_getter):
        self.level = level
        self.max_level = max_level
        self.center = center
        self.parent = parent
        self.get_original_time_series_ids_in_tree = original_time_series_ids_getter
        self._id = next_node_id_getter()
        self.n_query_subsequences = 0
        self.children = None
        self._inverted_file = None
        if level + 1 == max_level or len(prototypes) == 1:
            self._generate_inverted_file(prototypes)
        else:
            self._generate_children(affinities, next_node_id_getter, prototypes)

    @property
    def is_leaf(self):
        return self.children is None

    @property
    def inverted_file(self):
        if self.is_leaf:
            return self._inverted_file
        else:
            inverted_file = Counter()
            for child in self.children:
                inverted_file += child.inverted_file
            return inverted_file

    @property
    def n_original_time_series_in_node(self):
        return len(self.inverted_file)

    @property
    def n_original_time_series_in_tree(self):
        return len(self.get_original_time_series_ids_in_tree())

    @property
    def weight(self):
        return np.log(self.n_original_time_series_in_tree/
                      self.n_original_time_series_in_node)

    @property
    def m_vector(self):
        m = np.zeros(self.n_original_time_series_in_tree)
        ids = self.get_original_time_series_ids_in_tree()
        for key, value in self.inverted_file.items():
            index = ids.index(key)
            m[index] = value
        return m

    @property
    def q(self):
        if self.n_query_subsequences is None:
            return None
        return self.n_query_subsequences*self.weight

    @property
    def d_vector(self):
        return self.weight*self.m_vector

    def add_shortcut_to_dict(self, shortcut_dict):
        shortcut_dict[self._id] = self
        if not self.is_leaf:
            for child in self.children:
                child.add_shortcut_to_dict(shortcut_dict)

    def _generate_children(self, affinities,
                           next_node_id_getter, prototypes):
        ap = AffinityPropagation(affinity='precomputed', verbose=True)
        ap.fit(affinities)
        n_clusters = len(ap.cluster_centers_indices_)
        cluster_centers = prototypes[ap.cluster_centers_indices_]
        labels = ap.labels_
        children = []
        for cluster_label, center in zip(range(n_clusters),
                                              cluster_centers):
            indices = np.where(labels==cluster_label)[0]
            child_prototypes = prototypes[indices]
            child_affinities = affinities[indices][:, indices]
            child = Node(self.level+1, self.max_level, child_prototypes,
                         child_affinities, center,
                         self, next_node_id_getter,
                         self.get_original_time_series_ids_in_tree)
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
            nearest_child.add_query_subsequence(subsequence)

    def _generate_inverted_file(self, prototypes):
        original_time_series_id = (subsequence.original_id
                                   for subsequence in prototypes)
        self._inverted_file = Counter(original_time_series_id)

    # def add_to_graph(self, parent_graph_node, graph):
    #     graph_node = pydot.Node(str(self))
    #     graph.add_node(graph_node)
    #     if parent_graph_node is not None:
    #         graph.add_edge(pydot.Edge(parent_graph_node,
    #                                   graph_node))
    #     if self.children is not None:
    #         for child in self.children:
    #             child.add_to_graph(graph_node, graph)