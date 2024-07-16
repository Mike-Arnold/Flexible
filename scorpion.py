
import csv
import time

import filefun
import backtrack

def clawlist_to_edgelist(L,R,T=0):
    edgelist = [[0,1],[0,2]]
    n = 3
    
    while n < 3 + L:
        leaf = [1,n]
        edgelist.append(leaf)
        n += 1
    while n < 3 + L + R:
        leaf = [2,n]
        edgelist.append(leaf)
        n += 1
    if T != 0:
        leaf = [0,n]
        edgelist.append(leaf)
        
        while n < 3 + L + R + T-1:
            leaf = [n,n+1]
            edgelist.append(leaf)
            n += 1
    
    return edgelist

def get_scorpion_edgelists(clawlists):
    edgelists = []
    for clawlist in clawlists:
        L,R = clawlist[0],clawlist[1]
        edgelist = clawlist_to_edgelist(L,R)
        edgelists.append(edgelist)
    return edgelists

def list_clawlist_sizes(n_max):
    clawlists = []
    for R in range(1, n_max+1):
        for L in range(0, R+1):
            if L+R+3 <= n_max:
                clawlists.append((L,R))
    return clawlists

def theorize_graceful_clawlists(m,k):
    # print("m,k:",m,k)
    if m < 2:
        print("m must be >= 2")
        return None
    if k < 1:
        print("k must be >= 1")
        return None
    # print("m =",m,"k =",k,"n =",m*k+1)
    unswitched = [m-2, m*(k-1)]
    switched = [m-2 + k-1, (m-1)*(k-1)]
    
    current = unswitched
    clawlists = []
    while current[0] <= switched[0]:
        
        # print(current)
        if current[0] <= current[1]:
            clawlists.append(tuple(current))
        elif current[0] > current[1]:
            reverse_current = (current[1],current[0])
            clawlists.append(reverse_current)
            
        if (k-1) % 2 == 0: # even claw size
            current[0] += 2
            current[1] -= 2
        if (k-1) % 2 == 1: # odd claw size
            current[0] += 1
            current[1] -= 1
        
    # print(clawlists)
    # print()
    return clawlists

def get_graceful_clawlists(n_max):
    graceful_clawlists = []
    for m in range(2, n_max+1):
        for k in range(1, n_max+1):
            if (m * k) + 1 <= n_max:
                # print(f"m = {m}, k = {k}, (m * k) + 1 = {(m * k) + 1}")
                mk_clawlists = theorize_graceful_clawlists(m,k)
                graceful_clawlists += mk_clawlists.copy()
    # graceful_clawlists = set(graceful_clawlists)
    all_clawlists = list_clawlist_sizes(n_max)
    graceful_clawlists = [x for x in all_clawlists if x in graceful_clawlists]
    
    return graceful_clawlists

def get_non_graceful_clawlists(graceful_clawlists, n_max):
    all_clawlists = list_clawlist_sizes(n_max)
    non_graceful_clawlists = [x for x in all_clawlists if x not in graceful_clawlists]
    return non_graceful_clawlists

class tailless_scorpion:
    def __init__(self, clawlist):
        self.L = L = clawlist[0]
        self.R = R = clawlist[1]
        self.n = L + R + 3
        self.clawlist = clawlist
        self.edgelist = clawlist_to_edgelist(L,R)

def test_scorpions(clawlists,prediction):
    results_data = []
    for clawlist in clawlists:
        print("testing",clawlist)
        scorpion = tailless_scorpion(clawlist)
        L = scorpion.L
        R = scorpion.R
        n = scorpion.n
        
        start = time.time()
        test = backtrack.test_parameter_list(n, 0, scorpion.edgelist, n, 1)
        print("num classes",len(test.class_list))
        print("num edges",test.num_nodes-1)
        print()
        test.total_iters = backtrack.test_roots(test)
        end = time.time()
        test_time = int(100 * (end - start))/100
        results_data.append([n, L, R, test.total_iters, test_time, test.reds, prediction])
    filefun.write_results('scorpion_results.csv',results_data)

def count_clawlists(clawlists,n_max):
    n_column = [0] * (n_max+1)
    for clawlist in clawlists:
        this_n = clawlist[0] + clawlist[1] + 3
        n_column[this_n] += 1
    for n in range(n_max+1):
        print(n,n_column[n])

if __name__ == '__main__':
    
    n_max = 100
    graceful_clawlists = get_graceful_clawlists(n_max)
    # print("graceful_clawlists", graceful_clawlists)
    # count_clawlists(graceful_clawlists,n_max)
    non_graceful_clawlists = get_non_graceful_clawlists(graceful_clawlists, n_max)
    # print("non_graceful_clawlists",non_graceful_clawlists)
    count_clawlists(non_graceful_clawlists,n_max)
    
    # filefun.start_new_file('scorpion_results.csv',["Nodes","Left","Right","Iterations","Seconds","Reds","Prediction"])
    # test_scorpions(graceful_clawlists,"graceful")
    # test_scorpions(non_graceful_clawlists,"non-graceful")
    
    