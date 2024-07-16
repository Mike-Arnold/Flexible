
import random
import time
import copy

import depthfun
import edgefun
import filefun
import graphing
import transmute

### functions used in test_roots() ###

def decide_edge_strategy(rt):
    if rt.iters%2 == 0:
        rt.edge_strat = "far"
    if rt.iters%2 == 1:
        rt.edge_strat = "near"
    # rt.edge_strat = "far" #test far-only
    # rt.edge_strat = "near" #test near-only

def decide_target_strategy(rt):
    # rt.target_list = rt.target_list_rev.copy() #test reverse-only
    # rt.target_list = rt.target_list_neg.copy() #test negate-only
    
    if rt.target_strat != "negate" and rt.is_last_neg is False:
        rt.target_strat = "negate"
        rt.target_list = rt.target_list_neg.copy()
    elif rt.target_strat != "reverse" and rt.is_last_rev is False:
        rt.target_strat = "reverse"
        rt.target_list = rt.target_list_rev.copy()
    if rt.iters%2 == 0 and rt.iters > 2*rt.num_edges**2 and rt.iters < rt.num_edges**3:
        rt.target_strat = "random"
        split_at = rt.min_depth + 3
        list_start = rt.target_list[:split_at]
        list_end = rt.target_list[split_at:]
        random.shuffle(list_end)
        rt.target_list = list_start + list_end

def apply_success(test, rt, node_labels):
    test.greens.append(rt.root)
    
    first_node = rt.root
    other_node = node_labels.index(max(node_labels))
    this_edge = [first_node,other_node]
    successful_class = -1
    
    for edge in rt.edgelist:
        if edge[0:2] == this_edge:
            successful_class = edge[2]
    for edge in rt.edgelist:
        if edge[2] == successful_class:
            test.results[edge[0]] = "success"
            test.results[edge[1]] = "success"

def report_result(result, rt, test, sn):
    print()
    print("tree_id",test.tree_id,"root",rt.root,rt.target_strat,"target_list",rt.target_list,result)
    print("min_depth",rt.min_depth,"max_depth",sn.max_depth,"strat",rt.target_strat,"total_iters",test.total_iters)

### functions used in backtrack() ###

def find_applicable(target, sn):
    applicable = []
    edge_classes = []
    unused = sn.unused_node_labels
    
    for edge in sn.active_edges:
        edge_class = edge[2]
        # try only one of each edge class
        if edge_class in edge_classes: continue
        # require class to never take greater label than it already has
        class_index = sn.class_list.index(edge_class)
        edge_label_min = sn.edge_label_mins[class_index]
        if target > edge_label_min: continue
        
        # append up to two cases
        plus_label = sn.node_labels[edge[0]] + target
        if plus_label in unused:
            case = applicable_case(sn, edge, plus_label)
            applicable.append(case)
            edge_classes.append(edge_class)
        minus_label = sn.node_labels[edge[0]] - target
        if minus_label in unused:
            case = applicable_case(sn, edge, minus_label)
            applicable.append(case)
            edge_classes.append(edge_class)

    if sn.edge_strat == "near":
        applicable.sort(key=lambda case: case.edge_distance,reverse=False)
    if sn.edge_strat == "far":
        applicable.sort(key=lambda case: case.edge_distance,reverse=True)
    # # test random order
    # if sn.iters > .3*sn.num_edges**3:
    #     random.shuffle(applicable)
    return applicable

def apply_new_label(case, sn, target):
    sn.node_labels[case.edge[1]] = case.new_label
    sn.unused_node_labels.remove(case.new_label)
    sn.labeled_edges.append(case.edge)
    sn.active_edges.remove(case.edge)
    for inactive in sn.inactive_edges:
        if inactive[0] == case.edge[1]:
            case.movers.append(inactive)
    for inactive in case.movers:
        sn.active_edges.append(inactive)
        sn.inactive_edges.remove(inactive)
    if sn.target_strat != "random":
        sn.edge_label_mins[case.edge_class_index] = target
    
    # print()
    # spacer = '	'*len(sn.labeled_edges)
    # print(spacer, "applying label for edge", case.edge[0:2])
    # print(spacer, "edge label:", target, ", node label:", case.new_label)
    # print(spacer, "node labels:", sn.node_labels)
    # print(spacer, "unused node labels:", sn.unused_node_labels)
    # print(spacer, "labeled edges:", [edge[0:2] for edge in sn.labeled_edges])
    # print(spacer, "active edges:", [edge[0:2] for edge in sn.active_edges])
    # print(spacer, "inactive edges:", [edge[0:2] for edge in sn.inactive_edges])

def remove_new_label(case, sn):
    sn.node_labels[case.edge[1]] = 0
    sn.unused_node_labels.append(case.new_label)
    sn.active_edges.append(case.edge)
    sn.labeled_edges.remove(case.edge)
    for active in case.movers:
        sn.inactive_edges.append(active)
        sn.active_edges.remove(active)
    if sn.target_strat != "random":
        sn.edge_label_mins[case.edge_class_index] = case.label_min

    # print()
    # spacer = '	'*len(sn.labeled_edges)
    # print(spacer, "removing label for edge", case.edge[0:2])
    # print(spacer, "unused node labels:", sn.unused_node_labels)
    # print(spacer, "labeled edges:", [edge[0:2] for edge in sn.labeled_edges])
    # print(spacer, "active edges:", [edge[0:2] for edge in sn.active_edges])
    # print(spacer, "inactive edges:", [edge[0:2] for edge in sn.inactive_edges])

### classes ###

class test_parameter_list:
    def __init__(self, num_nodes, tree_id, edgelist, iter_mod, all_roots):
        self.num_nodes = num_nodes
        self.edgelist = edgefun.initialize_edgelist(edgelist)
        self.class_list = edgefun.get_class_list(self.edgelist)
        self.tree_id = tree_id
        self.iter_mod = iter_mod
        self.total_iters = 0
        self.all_roots = all_roots
        self.greens, self.reds = [],[]    
        self.results = [""]*num_nodes
        self.rooted_trees = [None]*num_nodes
        self.iter_limit = num_nodes * iter_mod

class rooted_tree:
    def __init__(self, root, edgelist):
        num_nodes = len(edgelist) + 1
        self.root = root
        self.num_edges = len(edgelist)
        self.edgelist = edgefun.redirect_edgelist(edgelist, root)
        self.target_list = [num_nodes-x for x in range(1,num_nodes)]
        self.target_list_neg = self.target_list.copy()
        self.target_list_rev = self.target_list.copy()
        self.is_last_neg = False
        self.is_last_rev = False
        self.edge_strat = "near"
        self.iters = 0
        self.min_depth = depthfun.find_min_depth(self.edgelist,root)
        self.target_strat = "reverse" # will get changed immediately to negate
        # iterate the non-default strategy right away so the default list isn't tried twice
        self.target_list_rev,foo = depthfun.iterate_list(self.target_list_rev,self.min_depth,"reverse")
        
class root_solution:
    def __init__(self, rt, test):
        num_nodes = rt.num_edges + 1
        self.num_edges = rt.num_edges
        self.unused_node_labels = list(range(1,num_nodes))
        self.node_labels = [0]*num_nodes
        self.edge_strat = rt.edge_strat
        self.target_strat = rt.target_strat
        self.iters, self.iter_limit = 0, test.iter_limit
        self.depth, self.max_depth = 0,0
        
        self.edgelist = rt.edgelist
        self.class_list = test.class_list
        self.num_classes = len(self.class_list)
        self.edge_label_mins = [num_nodes] * self.num_classes
        self.labeled_edges,self.active_edges,self.inactive_edges = [],[],[]
        for edge in rt.edgelist:
            if edge[0] == rt.root:
                self.active_edges.append(edge)
            else:
                self.inactive_edges.append(edge)
                
class applicable_case:
    def __init__(self, sn, edge, new_label):
        self.edge = edge
        self.new_label = new_label
        self.movers = []
        self.edge_class = edge[2]
        self.edge_distance = edge[3]
        self.edge_class_index = self.edge_class[2]
        self.label_min = sn.edge_label_mins[self.edge_class_index]

### test functions ###

def test_parameters(node_nums,tree_ids,iter_mods=None,all_roots=1):
    if iter_mods is None:
        iter_mods = node_nums
    if isinstance(node_nums,list):
        for node_num in node_nums:
            test_parameters(node_num,tree_ids,iter_mods,all_roots)
    elif isinstance(tree_ids,list):
        for tree_id in tree_ids:
            print(node_nums,tree_id)
            random.seed(tree_id) # set seed here to remove random effects from other tree tests
            test_parameters(node_nums,tree_id,iter_mods,all_roots)
    elif isinstance(iter_mods,list):
        for iter_mod in iter_mods:
            test_parameters(node_nums,tree_ids,iter_mod,all_roots)
    else:
        level = sample_trees[node_nums][tree_ids]
        edgelist = transmute.level_to_edgelist(level)
        ##### try custom edgelist here
        
        # random.shuffle(edgelist)
        node_nums = len(edgelist)+1
        start = time.time()
        test = test_parameter_list(node_nums,tree_ids,edgelist,iter_mods,all_roots)
        test.total_iters = test_roots(test)
        end = time.time()
        test_time = end - start
        results_data.append([node_nums,tree_ids,iter_mods,test.total_iters,test_time,test.reds])
        
def test_roots(test):
    # graphing.graph_problem_tree(test)
    
    root = 0
    # test.results = [""] # for testing
    while "" in test.results:
        if test.results[root] == "":
            rt = test.rooted_trees[root]
            if rt is None:
                rt = test.rooted_trees[root] = rooted_tree(root, test.edgelist)
            
            decide_edge_strategy(rt)
            decide_target_strategy(rt)
            
            sn = root_solution(rt, test)
            
            print()
            print("trying root",root,"list strat",rt.target_strat,"target list",rt.target_list)
            
            result = backtrack(rt.target_list, sn)
            rt.iters += sn.iters
            test.total_iters += sn.iters
            
            if result == "success":
                # report_result(result, rt, test, sn)
                # graphing.graph_solution_tree(test,sn.node_labels)
                if test.all_roots == 0:
                    return test.total_iters
                apply_success(test, rt, sn.node_labels)
                
            if result == "impossible":
                # report_result(result, rt, test, sn)
                is_last = depthfun.iterate_list_strat(rt, sn)
                if is_last is True:
                    test.results[root] = "impossible"
                    test.reds.append(root)
        
        root += 1
        if root == test.num_nodes:
            root = 0
            test.iter_limit *= 2
        # root = (root+1)%test.num_nodes # keep trying roots until they finish
        # test.iter_limit += test.iter_mod
    
    # print("Total iterations: ",test.total_iters)
    return test.total_iters

def backtrack(target_list, sn):
    if target_list == []: return "success"
    sn.iters += 1
    this_iter = sn.iters
    # print()
    # print('	'*len(sn.labeled_edges),"starting iteration",this_iter)
    if sn.iters > sn.iter_limit: return "hit limit"
    
    target = target_list[0]
    applicable = find_applicable(target, sn)
    # print('	'*len(sn.labeled_edges),"applicable:",[case.edge[0:2] for case in applicable])
    for case in applicable:
        
        apply_new_label(case, sn, target)
        depthfun.get_depth(sn)
        
        next_list = target_list[1:]
        result = backtrack(next_list, sn)
        if result == "success" or result == "hit limit":
            # print()
            # print("exiting iteration",this_iter)
            return result
        
        remove_new_label(case, sn)
    
    # print()
    # print('	'*len(sn.labeled_edges),"exiting iteration",this_iter)
    return "impossible"

### main function ###

if __name__ == '__main__':
    
    random.seed(327)
    
    global sample_trees
    sample_trees = filefun.read_sample_trees('canon tree info/canon_trees_15.csv')
    # sample_trees = filefun.read_sample_trees('canon tree info/canon_trees.csv')
    global results_data
    results_data = []
    
    node_nums = 15
    # tree_ids = list(range(0, 4096, 1))
    tree_ids = list(range(0, 7741, 1))
    # tree_ids = list(range(0, 10))
    
    tree_ids = [6774]
    
    iter_mods = 15
    # iter_mods = list(range(5, 40, 5))
    all_roots = 0
    
    start = time.perf_counter()
    test_parameters(node_nums,tree_ids,iter_mods,all_roots)
    print(int((time.perf_counter() - start)*1000)/1000)
    
    headers = ["Num_nodes","Tree_id","Iter_mod","Total_iters","Seconds","Reds"]
    filename = 'results backtrack 6774.csv'
    filefun.start_new_file(filename,headers)
    filefun.write_results(filename,results_data)
