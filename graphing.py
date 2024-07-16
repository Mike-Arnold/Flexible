
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import graphviz
import os
import copy

import edgefun
import filefun
import transmute


def f(number):
    return int(number*1000)/1000

def graph_nxtree(nxtree,node_num,tree_id=0,iter_mod=0,iters=0, \
                 greens=[],reds=[],title="",draw_node_labels=1,draw_edge_labels=1,
                 custom_node_labels=[]):
    # initialize the plot
    n_sqrt = node_num**.5
    plt.figure(figsize = (15+n_sqrt,15+n_sqrt))         # change to 20 or 30 for paths
    font_size = 150/n_sqrt                              #150 or 200
    pos = graphviz_layout(nxtree, prog="neato")          # neato, dot, fdp, twopi
    # pos = graphviz_layout(nxtree, prog="twopi")        # use for chandelier
    # pos = graphviz_layout(nxtree, prog="dot")          # use for 'needs flexible'
    # https://graphviz.org/docs/layouts/
    # remove any nodes that don't actually exist
    # nodes_without_positions = [node for node in nxtree.nodes() if node not in pos]
    # nxtree.remove_nodes_from(nodes_without_positions)
    
    # pos = {node: (y,x) for node, (x, y) in pos.items()} # flip image on diagonal
    
    # debug: show positions
    # for node, position in pos.items():
    #     print(f"Node {node}: Position {position}")
    # print(pos.items())
    
    # reds = [0] # use for the scorpion example
    
    # set node colors
    node_colors = ['#1f78b4']*node_num # blue default
    node_colors = ['#ffffff']*node_num # white default
    # set node_outlines
    node_outlines = ['#000000']*node_num # black default
    for u in nxtree.nodes():
        if u in greens: # mark graceful root(s) as green
            node_colors[u] = '#51b33b'
            node_outlines[u] = '#51b33b'
        if u in reds: # mark stingers as red
            # node_colors[u] = '#9e162f'
            node_outlines[u] = '#9e162f'
    nx.draw(nxtree, pos, node_size=20000/n_sqrt,  #30000
            linewidths=4, width=4,
            node_color = node_colors, edgecolors = node_outlines,
            # nodelist = list(range(node_num))) 
            )
    
    # # for the level sequence examples
    # # title = [1, 2, 3, 2, 3]
    # # title = [1, 2, 3, 2, 2]
    # title = [1, 2, 2, 2, 2]
    # title = plt.title(title, fontsize = 100)
    
    if draw_node_labels == 1:
        node_labels = {}
        for u in nxtree.nodes():
            node_labels[u] = u
            if custom_node_labels != []:
                node_labels[u] = custom_node_labels[u]
        nx.draw_networkx_labels(nxtree, pos, labels = node_labels, font_size = font_size)
    
    if (greens != [] and reds == []) or draw_edge_labels == 1:
        # set edge labels to be the difference between the nodes it connects
        edge_labels = {}
        for u,v in nxtree.edges():
            key = (u,v)
            if isinstance(node_labels[u], (int)) and isinstance(node_labels[v], (int)):
                value = abs(node_labels[u] - node_labels[v])
            else:
                value = ""
            edge_labels[key] = value
        text = nx.draw_networkx_edge_labels(nxtree, pos, edge_labels = edge_labels, font_size = font_size)
        for _,t in text.items():
            t.set_rotation('horizontal')
    
    # # format the title
    # parameters = str("Nodes = {} , Tree id = {}".format(node_num,tree_id))
    # if iters > 0: parameters += str("\n Iterations = {} ({})".format(iters,iter_mod))
    # plt.title(title + parameters,fontsize = 10*n_sqrt)
    
    # choose background color
    # plt.gcf().set_facecolor("#A9A9A9") # darker grey
    plt.gcf().set_facecolor("#FFFFFF") # white
    # plt.gcf().set_facecolor("#CCCCCC") # light grey
    
    # zoom out a bit
    plt.margins(0.1) # .1 or .2
    plt.axis('off')
    axis = plt.gca()
    # axis.set_ylim([1.4*y-0 for y in axis.get_ylim()]) # use for the smallest figures, subtract 70 or 167
    
    # save and show
    filename = str("graph output/{}_{}.png".format(node_num,tree_id))
    plt.savefig(filename,bbox_inches='tight')
    plt.show()
    
def graph_problem_tree(test):
    edgelist = copy.deepcopy(test.edgelist)
    edgelist = [edge[0:2] for edge in edgelist]
    nxtree = transmute.edgelist_to_nxtree(edgelist)
    graph_nxtree(nxtree, test.num_nodes, test.tree_id, draw_edge_labels=0)

def graph_solution_tree(test,labels):
    new_edgelist = edgefun.reassign(test.edgelist,labels)
    nxtree = transmute.edgelist_to_nxtree(new_edgelist)
    graph_nxtree(nxtree,test.num_nodes,test.tree_id,test.iter_mod, \
                 test.total_iters)

def graph_root_results(test):
    nxtree = transmute.edgelist_to_nxtree(test.edgelist)
    graph_nxtree(nxtree,test.num_nodes,test.tree_id,test.iter_mod, \
                 test.total_iters,test.greens,test.reds,title="Testing all roots \n")

def graph_edgelist(edgelist,draw_node_labels=1,draw_edge_labels=1):
    nxtree = transmute.edgelist_to_nxtree(edgelist)
    graph_nxtree(nxtree,len(nxtree), \
                 draw_node_labels = draw_node_labels, \
                 draw_edge_labels = draw_edge_labels,
                 reds = [3,9])

def graph_level(node_nums,tree_id,draw_node_labels=1,draw_edge_labels=1):
    level = sample_trees[node_nums][tree_id]
    edgelist = transmute.level_to_edgelist(level)
    nxtree = transmute.edgelist_to_nxtree(edgelist)
    graph_nxtree(nxtree,len(nxtree), \
                 draw_node_labels = draw_node_labels, \
                 draw_edge_labels = draw_edge_labels)

if __name__ == '__main__':
    print("don't run me directly")
    
    # use axis.set_ylim([1.4*y for y in axis.get_ylim()])
    # graph_edgelist([[0,1],[1,2],[0,2],[3,3]],0,0) # blank triangle
    # graph_edgelist([[0,1],[1,2],[0,2],[3,3]]) # failed attempt
    # graph_edgelist([[0,1],[1,3],[0,3],[2,2]]) # graceful triangle
    
    # # added node
    # graph_edgelist([[1,2],[2,4],[1,4],[3,3]]) # add one to all node labels
    # graph_edgelist([[4,3],[3,1],[4,1],[2,2]]) # reversed order
    
    # graph_edgelist([[0,1],[1,2],[1,3],[2,3],[3,4],[4,5],[5,6],[6,7],[7,3]],0,0) # not a tree
    # graph_edgelist([[0,1],[1,2],[2,3],[3,4],[2,5],[2,6],[6,7],[6,8]],0,0) # is a tree
    
    # turn off axis.set_ylim
    # graph_edgelist([[0,1],[0,2],[0,3],[0,4]]) # star1
    # graph_edgelist([[4,3],[4,2],[4,1],[4,0]]) # star2
    
    # complementary solutions
    # graph_edgelist([[5,0],[0,6],[0,7],[7,3],[3,4],[4,1],[4,2]])
    # graph_edgelist([[2,7],[7,1],[7,0],[0,4],[4,3],[3,6],[3,5]])
    
    # use twopi instead of neato
    # graph_edgelist([[0,28],[28,1],[1,27],[1,26],[27,3],[27,4],[27,5],[27,6], \
    #                 [27,7],[27,8],[27,9],[3,20],[5,21],[7,22],[9,23],[3,16], \
    #                     [5,17],[7,18],[4,14],[6,15],[27,19],[6,13],[19,25],  \
    #                         [19,24],[8,12],[8,11],[4,2],[9,10]]) # chandelier
    
    # graph_edgelist([[0,5],[5,1],[1,4],[4,2],[2,3]]) # path
    # graph_edgelist([[0,9],[9,1],[9,2],[9,3],[3,8],[3,7],[3,6],[6,4],[6,5]]) # caterpillar
    
    # graph_edgelist([[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[5,8],[8,9],[8,10]],0,0) # scorpion with red stinger
    
    # use axis.set_ylim([1.4*y for y in axis.get_ylim()])
    # graph_edgelist([[0,4],[4,1],[1,3],[4,2]],0,1) # root labeled 0
    # # first edge labeled
    # # try middle edge
    # # try rightmost edge
    # # failed to apply label
    # # back one, try lefthand
    # # failed to apply label
    # graph_edgelist([[0,4,],[4,1],[4,2],[2,3]]) # backup more, try lefthand
    # # success with middle edge
    # # success with rightmost edge
    
    # turn off axis.set_ylim
    # graph_edgelist([[2,5],[5,4],[4,0],[0,6],[6,1],[1,3]]) # needs flexible target list
    
    # # hrnciar's tree of diamter five
    # graph_edgelist([[0,17],[0,2],[0,4],[0,13],[0,15],[2,9],[2,11],[15,7],[15,10], \
    #                 [17,1],[17,16],[17,3],[17,14],[17,5],[1,12],[16,6],[14,8]])
    
    # # rofa's symmetrical rooted tree
    # graph_edgelist([[0,32],[0,16],[32,1],[32,6],[32,11],[1,31],[1,30],[1,29], \
    #                 [1,28],[6,26],[6,25],[6,24],[6,23],[11,21],[11,20],[11,19], \
    #                 [11,18],[16,17],[16,22],[16,27],[17,15],[17,14],[17,13], \
    #                 [17,12],[22,10],[22,9],[22,8],[22,7],[27,5],[27,4],[27,3],[27,2]])
    
    # level sequences
    # graph_edgelist([[0,1],[1,2],[0,3],[3,4]],0,0)
    # graph_edgelist([[0,1],[1,2],[0,3],[0,4]],0,0)
    # graph_edgelist([[0,1],[0,2],[0,3],[0,4]],0,0)
    
    # global sample_trees
    # sample_trees = filefun.read_sample_trees('canon tree info/canon_trees_15.csv')
    # sample_trees = filefun.read_sample_trees('canon tree info/canon_trees.csv')
    # level = sample_trees[10][19]
    # edgelist = transmute.level_to_edgelist(level)
    # nxtree = transmute.edgelist_to_nxtree(edgelist)
    # graph_nxtree(nxtree,10,custom_node_labels=[9,0,7,"","","","",1,6,""])
    
    graph_edgelist([[0,1],[0,2],[1,3],[2,4],[2,5],[2,6],[2,9],[0,7],[7,8]],0,0)
    
    # graph_level(15,2734,0,0) # case where far is better
    # graph_level(15,2717,0,0) # case where near is better
    
    # graph_level(15,1767,0,0) # case where reverse is best
    # graph_level(15,1780,0,0) # case where negate is best
    # graph_level(15,3448,0,0) # case where switching is best
    
    # graph_level(15,1531,0,0) # ruling out bad edge classes
    
    # graph_level(15,3451,0,0) # using minimum depth
    # graph_level(15,1760,0,0) # using classwise depth
    
    # graph_level(15,6890,0,0) # does terribly with default edge priority - requires 15 million iterations