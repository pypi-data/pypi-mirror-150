#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script aims to collect functions related to the graph data structure manipulation.
We use the ``networkx`` package to represent the graph data structure.
"""

import itertools
from typing import List
import networkx as nx
from copy import deepcopy
import matplotlib.pyplot as plt
import random
import time


def connected_subgraphs(G: nx.Graph, k: int) -> List[nx.Graph]:
    r"""Find all subgraphs of size :math:`k` of a graph.

    We assume that the input graph is undirected. Each subgraph must satisfy the following two conditions:

    1. The subgraph is connected; and
    2. The number of nodes of the subgraph is k.

    References: https://www.py4u.net/discuss/199398

    :param G: nx.Graph, an undirected graph whose connected subgraphs to be extracted
    :param k: int, the number of nodes in each connected subgraph
    :return: List[nx.Graph], a list of connected subgraphs of type ``networkx.Graph``
    """
    subgraphs = []
    # TODO: the following algorithm's efficiency can be improved
    for sg in (G.subgraph(selected_nodes) for selected_nodes in itertools.combinations(G, k)):
        if nx.is_connected(sg):
            subgraphs.append(sg)

    return subgraphs


def new_algorithm(G, k):
    all_subgraphs = []

    def dfs(selected_nodes: List, extension, removed):
        #print(selected_nodes,extension,removed)
        if len(selected_nodes) == k-1:
            for final_node in extension:
                all_subgraphs.append(G.subgraph(selected_nodes+[final_node]))
            return

        for i in range(len(extension)):
            current_node = extension[i]
            dfs(selected_nodes + [current_node],
                extension[i+1:]+[nxt_node
                                 for nxt_node in G.neighbors(current_node)
                                 if nxt_node > start and
                                 nxt_node not in selected_nodes and
                                 nxt_node not in removed
                                 and nxt_node not in extension],
                removed+[current_node],)
            removed.append(current_node)

    for node in G.nodes:
        start = node
        dfs([node], [x for x in G.neighbors(node) if x > node], [])

    return all_subgraphs


if __name__ == '__main__':

    def test():
        n = 100
        k = 6
        G = nx.Graph()
        H = nx.path_graph(n)
        G.add_nodes_from(H)
        seed = random.randint(1, 1000)
        print(seed)
        random.seed(84)

        def rand_edge(vi, vj, p=0.2):
            probability = random.random()
            if (probability < p):
                G.add_edge(vi, vj)

        p = 0.2
        for i in range(n):
            for j in range(i):
                rand_edge(i, j, p)

        start2 = time.time()
        sub2 = new_algorithm(G, k)
        end2 = time.time()
        print(end2 - start2)
        start1 = time.time()
        sub1 = connected_subgraphs(G, k)
        end1 = time.time()
        print(end1 - start1)

        print(len([x.nodes for x in sub2]))
        print(len([x.nodes for x in sub1]))

        nx.draw_networkx(G)
        plt.show()


    test()
