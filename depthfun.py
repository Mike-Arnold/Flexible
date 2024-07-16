
import edgefun

### permutations and depth ###

def iterate_list_strat(rt, sn):
    # print(rt.target_list,"list before skip, max depth",sn.max_depth)
    if rt.target_strat == "negate":
        skip_list(rt, sn.max_depth)
    # print(rt.target_list,"after skip, before iterate via",rt.target_strat)
    rt.target_list, rt.is_last = iterate_list(rt.target_list,rt.min_depth,rt.target_strat)
    # print(rt.target_list,"after iterate")
    if rt.target_strat == "negate":
        rt.target_list_neg = rt.target_list.copy()
        rt.is_last_neg = rt.is_last
    if rt.target_strat == "reverse":
        rt.target_list_rev = rt.target_list.copy()
        rt.is_last_rev = rt.is_last
    if rt.is_last_neg is True or rt.is_last_rev is True:
        return True
    else:
        return False

def skip_list(rt,depth):
    list_start = rt.target_list[:depth]
    list_end = rt.target_list[depth:]
    list_end.sort()
    rt.target_list = list_start + list_end

def iterate_list(target_list, min_depth, strat="negate"):
    split_at = min_depth + 3
    list_start = target_list[:split_at]
    list_end = target_list[split_at:]
    is_last = False
    
    if strat == "negate":
        list_end = [-x for x in list_end]
        is_last = not(next_permutation(list_end))
        list_end = [-x for x in list_end]
    if strat == "reverse":
        list_end.reverse()
        is_last = not(next_permutation(list_end))
        list_end.reverse()
    # if strat == "random":
    #     is_last = False
        
    target_list = list_start + list_end
    return target_list, is_last

def next_permutation(arr):
    # Soure: https://www.nayuki.io/page/next-lexicographical-permutation-algorithm
    # Find non-increasing suffix
    i = len(arr) - 1
    while i > 0 and arr[i - 1] >= arr[i]:
        i -= 1
    if i <= 0:
        return False
    
    # Find successor to pivot
    j = len(arr) - 1
    while arr[j] <= arr[i - 1]:
        j -= 1
    arr[i - 1], arr[j] = arr[j], arr[i - 1]
    
    # Reverse suffix
    arr[i : ] = arr[len(arr) - 1 : i - 1 : -1]
    return True

def transpose_list(my_list):
    return [list(i) for i in zip(*my_list)]

def find_min_depth(edgelist,root):
    t_list = transpose_list(edgelist)
    min_depth = 0
    
    while True:
        if t_list[0].count(root) == 1:
            min_depth += 1
            root_index = t_list[0].index(root)
            root = t_list[1][root_index]
        else:
            break
    
    return min_depth

def find_edge_classes(edgelist):
    edge_classes = []
    for edge in edgelist:
        edge_class = edge[2]
        if edge_class not in edge_classes:
            edge_classes.append(edge_class)
    return edge_classes

def count_good_edges(edgelist,bad_edge_classes):
    good_edge_count = 0
    for edge in edgelist:
        edge_class = edge[2]
        if edge_class not in bad_edge_classes:
            good_edge_count += 1
    return good_edge_count

def get_depth(sn):
    if sn.target_strat == "negate":
        if sn.num_classes < sn.num_edges - 4:
            classwise_depth(sn)
        else:
            naive_depth(sn)

def naive_depth(sn):
    sn.depth = len(sn.labeled_edges)
    
    sn.max_depth = max(sn.max_depth, sn.depth)

def classwise_depth(sn):
    open_edges = sn.active_edges + sn.inactive_edges
    open_edge_classes = find_edge_classes(open_edges)
    sn.depth = count_good_edges(sn.labeled_edges,open_edge_classes)
    
    sn.max_depth = max(sn.max_depth, sn.depth)

if __name__ == '__main__':
    print("don't run me directly")
    
    target_list = [14,13,12,11,10,9,8,7,6,5,4,3,2,1]
    print(target_list)   
    target_list, is_last = iterate_list(target_list, 2,"negate")
    print(target_list)    
    target_list = [14,13,12,11,10,9,8,7,6,5,4,3,2,1]
    target_list, is_last = iterate_list(target_list, 2,"reverse")
    print(target_list)