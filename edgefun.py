
import networkx as nx
from networkx.algorithms.isomorphism import rooted_tree_isomorphism
import copy

import transmute

### intialize edgelist and class list ###

def initialize_edgelist(edgelist):
    classify_edges(edgelist,0) # edge class is edge[2]
    append_edge_distances(edgelist) # distance is edge[3]
    return edgelist

def get_class_list(edgelist):
    class_list = []
    for edge in edgelist:
        edge_class = edge[2]
        if edge_class not in class_list:
            class_list.append(edge_class)
        else:
            index = class_list.index(edge_class)
            edge_class = class_list[index]
        edge[2] = edge_class
    for i,edge_class in enumerate(class_list): # number ids for classes of an edge
        edge_class.append(i)
    return class_list

### modify edgelist ###

def reassign(edgelist, assignment = []):
    edgelist = copy.deepcopy(edgelist)
    new_edgelist = []
    for e in edgelist:
        e[0] = assignment[e[0]]
        e[1] = assignment[e[1]]
        new_edgelist.append(e[0:2])
    return new_edgelist

def redirect_edgelist(edgelist,root=0):
    edgelist = copy.deepcopy(edgelist)
    checked = [root]
    unchecked = list(range(len(edgelist)+1))
    unchecked.remove(root)
    
    distance = 1
    while unchecked != []:
        movers = []
        for e in edgelist:
            if e[1] in checked and e[0] in unchecked:
                e[0],e[1] = e[1],e[0]
            if e[0] in checked and e[1] in unchecked:
                movers.append(e[1])
                e.append(distance)
        for n in movers:
            checked.append(n)
            unchecked.remove(n)
        distance += 1
    return edgelist

def append_edge_distances(edgelist):
    distances = transmute.edgelist_distances(edgelist)
    for i,edge in enumerate(edgelist):
        edge.append(distances[i])

### edge classes ###

def classify_edges(edgelist, root):
    # classifies any subtree
    subtree_lists = [[] for x in range(len(edgelist)+1)]
    treeclass_lists = []
    edgeclass_list = []
    for edge in edgelist:
        parent = edge[0]
        child = edge[1]
        subtree = get_subtree(edgelist,child)
        subtree_lists[parent].append(subtree)
    for parent,subtree_list in enumerate(subtree_lists):
        tree_classes = []
        if len(subtree_list) == 1: # only one subtree, only one class
            tree_classes = [0]
        elif subtree_list != []:
            tree_classes = classify_subtrees(subtree_list,parent)
        treeclass_lists.append(tree_classes)
    for edge in edgelist:
        parent = edge[0]
        child = edge[1]
        subtree_class = treeclass_lists[parent].pop(0)
        edge_class = [parent,subtree_class]
        edge.append(edge_class)

def get_subtree(edgelist, root):
    subtree_edgelist = []
    subtree_nodes = []
    
    unfinished = True
    while unfinished:
        unfinished = False
        for edge in edgelist:
            if edge[0] in subtree_nodes or edge[1] == root:
                if edge[1] not in subtree_nodes:
                    subtree_edgelist.append(edge)
                    subtree_nodes.append(edge[1])
                    unfinished = True
    return subtree_edgelist
            
def classify_subtrees(trees, root):
    tree_classes = [-1] * len(trees)
    nxtrees = []
    for tree in trees:
        nxtree = transmute.edgelist_to_nxtree(tree)
        nxtrees.append(nxtree)
    for i,tree1 in enumerate(nxtrees):
        for j,tree2 in enumerate(nxtrees):
            if i < j and tree_classes[j] == -1:
                if rooted_tree_isomorphism(tree1,root,tree2,root) != []:
                    tree_classes[i] = i
                    tree_classes[j] = i
        if tree_classes[i] == -1:
            tree_classes[i] = i
    return tree_classes

if __name__ == '__main__':
    print("don't run me directly")