
import networkx as nx
import csv
import random


def nexttree(L, W, n, p, q, h1, h2, c, r):
    false = 0
    true = 1
    infty = 10**9
    
    fixit = false
    
    if c == n+1 or ( p == h2 and ( ( L[h1-1]==L[h2-1]+1 and n-h2>r-h1 ) or \
                                   ( L[h1-1]==L[h2-1] and n-h2+1<r-h1) ) ):
        if L[r-1]>3:
            p = r
            q = W[r-1]
            if h1 == r:
                h1 -= 1
            fixit = true
        else:
            p = r
            r -= 1
            q = 2
    
    needr = false
    needc = false
    needh2 = false
    
    if p <= h1:
        h1 = p-1
    if p <= r:
        needr = true
    elif p <= h2:
        needh2 = true
    elif L[h2-1] == L[h1-1]-1 and n-h2 == r-h1:
        if p <= c:
            needc = true
    else:
        c = infty
    
    oldp = p
    t = q-p
    oldlq = L[q-1]
    oldwq = W[q-1]
    p = infty
    
    
    for i in range(oldp, n+1):
        L[i-1] = L[i-1+t]
        if L[i-1] == 2:
            W[i-1] = 1
        else:
            p = i
            if L[i-1] == oldlq:
                q = oldwq
            else:
                q = W[i-1+t] - t
            W[i-1] = q
        
        if needr and L[i-1] == 2:
            needr = false
            needh2 = true
            r = i-1
            
        if needh2 and L[i-1] <= L[i-2] and i>r+1:
            needh2 = false
            h2 = i-1
            if L[h2-1] == L[h1-1]-1 and n-h2 == r-h1:
                needc = true
            else:
                c = infty
        
        if needc:
            if L[i-1] != L[h1-h2+i-1]-1:
                needc = false
                c = i
            else:
                c = i+1
        
    if fixit:
        r = n-h1+1
        for i in range(r+1, n+1):
            L[i-1] = i-r+1
            W[i-1] = i-1
        W[r] = 1
        h2 = n
        p = n
        q = p-1
        c = 10**9
    else:
        if p == 10**9:
            if L[oldp-2] != 2:
                p = oldp-1
            else:
                p = oldp-2
            q = W[p-1]
        if needh2:
            h2 = n
            if L[h2-1] == L[h1-1]-1 and h1 == r:
                c = n+1
            else:
                c = 10**9
    
    return L, W, n, p, q, h1, h2, c, r

def generate_sequences(n):
    if n < 4: return [[1]+[2]*(n-1)]
    
    k = int(n/2) + 1  # round down
    L = list(range(1,k+1)) + list(range(2,n-k+2))
    
    W, W[k] = list(range(0,n)), 1
    p,q,h1,h2,r = n,n-1,k,n,k
    
    if n == 4:    p = n-1    # special case
    if n%2 == 1:  c = 10**9  # odd n
    else:         c = n+1    # even n
    
    level_sequences = [L.copy()]
    while q != 0:
        L, W, n, p, q, h1, h2, c, r = nexttree(L, W, n, p, q, h1, h2, c, r)
        level_sequences.append(L.copy())
            
    return level_sequences

def random_canon_trees(nodes,num_trees,seed):
    random.seed(seed)
    
    nont = nx.number_of_nonisomorphic_trees(nodes)
    tree_numbers = [random.randrange(0,nont,1) for i in range(num_trees)]
    tree_numbers.sort()
    random_trees = []
    all_trees = nx.nonisomorphic_trees(nodes)
    for i,tree in enumerate(all_trees):
        while 1:
            if len(tree_numbers) == 0:
                break
            if i == tree_numbers[0]:
                random_trees.append(tree)
                tree_numbers.pop(0)
            else:
                break
    return random_trees

def sample_trees(n,sample_size=4096):
    
    k = int(n/2) + 1  # round down
    L = list(range(1,k+1)) + list(range(2,n-k+2))
    
    unique_trees = nx.number_of_nonisomorphic_trees(n)
    sample_gap = (unique_trees-1) / (sample_size-1)
    sample_ids = []
    
    if unique_trees < sample_size:
        print("error, not enough trees to sample from")
        return "error"
    
    for i in range(sample_size+1):
        sample_number = sample_gap*i
        sample_ids.append(round(sample_number))
    
    W, W[k] = list(range(0,n)), 1
    p,q,h1,h2,r = n,n-1,k,n,k
    
    if n == 4:    p = n-1    # special case
    if n%2 == 1:  c = 10**9  # odd n
    else:         c = n+1    # even n
    
    tree_id = 0
    write_line_to_file([tree_id,L, W, n, p, q, h1, h2, c, r])
    while q != 0:
        L, W, n, p, q, h1, h2, c, r = nexttree(L, W, n, p, q, h1, h2, c, r)
        tree_id += 1
        if tree_id in sample_ids:
            write_line_to_file([tree_id,L, W, n, p, q, h1, h2, c, r])
        
    return "success"

def start_new_file(line_info):
    with open('canon_trees_sample.csv', mode='w', newline='') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(line_info)

def write_line_to_file(line_info):
    with open('canon_trees_sample.csv', mode='a+', newline='') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(line_info)

if __name__ == '__main__':
    
    # start_new_file(['id','L','W','n','p','q','h1','h2','c','r'])
    
    # for n in range(24,25):
    #     sample_trees(n)
    #     print("finished",n)
    
    for n in range(1,7):
        level_sequences = generate_sequences(n)
        for level in level_sequences:
            print(level)
