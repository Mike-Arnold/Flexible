
import networkx as nx

### change tree format
 
def edgelist_to_matrix(edgelist):
    N = len(edgelist) + 1
    # fill a matrix with zeroes
    matrix = [[0]*(N) for i in range(N)]
    
    # place the 1s
    for e in edgelist:
        i = e[0]
        j = e[1]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix
    
def edgelist_to_nxtree(edgelist):
    p_edgelist = []
    for edge in edgelist:
        edge = edge[0:2]
        line = ' '.join(str(x) for x in edge)
        p_edgelist.append(line)
    nxtree = nx.parse_edgelist(p_edgelist, delimiter=" ", nodetype=int)
    
    return nxtree

def level_to_edgelist(level):
    edgelist = []
    
    for i in range(1,len(level)):
        searching = 1
        second = i
        first = i-1
        while searching:
            if level[first] < level[second]:
                edgelist.append([first,second])
                searching = 0
            else:
                first -= 1
    return edgelist

def matrix_to_edgelist(matrix):
    edge_list = []
    i = 0
    while i < len(matrix)-1:
        j = i+1
        while j < len(matrix):
            if matrix[i][j] == 1:
                edge_list.append([i,j])
            j += 1
        i += 1
    return edge_list

def matrix_to_nxtree(matrix, nodes):
    adjacency_list = []
    for i in range(nodes):
        temp = str(i)
        for j in range(nodes):
            foo = matrix[i][j]
            if(j>i and foo == 1):
                temp += " " + str(j)
        adjacency_list.append(temp)
    nxtree = nx.parse_adjlist(adjacency_list, nodetype=int)
    return nxtree

def matrix_to_prufer(matrix):
    prufer = []
    while len(matrix) > len(prufer)+2:
        i = 0
        while i < len(matrix):
            if sum(matrix[i]) == 1:
                axil = matrix[i].index(1)
                prufer.append(axil)
                #print(prufer)
                matrix[i][axil] = 0
                matrix[axil][i] = 0
                break
            i += 1
    return prufer

def nxtree_to_edgelist(nxtree):
    edgelist = []
    for line in nx.generate_adjlist(nxtree):
        my_list = line.split(" ")
        my_list = [int(i) for i in my_list]
        for i in range(len(my_list)-1):
            edgelist.append([my_list[0],my_list[i+1]])
    return edgelist

def nxtree_to_matrix(nxtree,nodes):
    temp = []
    for line in nx.generate_adjlist(nxtree):
        my_list = line.split(" ")
        my_list.pop(0)
        my_list = [int(i) for i in my_list]
        
        temp.append(my_list)
    # fill a matrix with zeroes
    matrix = [[0]*(nodes) for i in range(nodes)]
    
    # place the 1s
    for i in range(nodes):
        for j in range(nodes):
            if j in temp[i]:
                matrix[i][j] = 1
                matrix[j][i] = 1
    return matrix

### matrix operations ###

def reorder(order_matrix, tree):
    OM = mmult(T(order_matrix), tree)
    OMO = mmult(OM, order_matrix)
    return OMO
    
def mmult(a,b):
    product = []
    for i in range(N):
        product.append([])
        for j in range(N):
            prodsum = 0
            for k in range(N):
                prodsum += a[i][k] * b[k][j]
            product[i].append(prodsum)
    return product

def T(a): # Transpose
  T = [[a[j][i] for j in range(N)] for i in range(N)]
  #credit for this solution goes to https://www.geeksforgeeks.org/transpose-matrix-single-line-python/
  return T

def print_matrix(matrix):
    max_len = 1
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            this_num = matrix[i][j]
            if len(str(this_num)) > max_len:
                max_len = len(str(this_num))
    
    for i in range(len(matrix)):
        rowtext = ""
        for j in range(len(matrix[i])):
            this_num = matrix[i][j]
            space = max_len - len(str(this_num))
            rowtext = rowtext + space*' ' + str(this_num) + " "
        print(rowtext)

def find_distances(matrix):
    N = len(matrix)
    distances = [row[:] for row in matrix]
    for d in range(2,N):
        for i in range(N):
            distances[i][i] = -1
            for j in range(N):
                if distances[i][j] == d-1:
                    for k in range(N):
                        if matrix[j][k] == 1 and distances[i][k] == 0:
                            distances[i][k] = d
    for i in range(N):
        distances[i][i] = 0
    return distances

def find_row_sums(matrix):
    N = len(matrix)
    distances = find_distances(matrix)
    
    row_sums = []
    for i in range(N):
        row_sum = sum(distances[i])
        row_sums.append(row_sum)
    return row_sums

def edgelist_distances(edgelist):
    matrix = edgelist_to_matrix(edgelist)
    distance_matrix = find_distances(matrix)
    root_distances = find_row_sums(distance_matrix)
    return root_distances

def is_box(matrix):
    N = len(matrix)
    # look at a solution and check if each half of the adjacency matrix
    # has a box with an upper-right and lower-left corner filled in
    
    # this happens when the edge label "one" is a corner
    # connecting nodes x and y, x > y
    # where all other connections have a > b and
    # a >= x and b <= y
    
    # confirm that alpha labeling is the same as being a box
    
    cel = corner_edge_label = 1 # nothing interesting with 2
    corner = -1
    
    # find the corner
    for i in range(cel,N): # column
        if matrix[i][i-cel] == 1:
            print("Corner edge label at",i,i-cel)
            corner = i
    if corner == -1: "didn't find an edge label using 1"
    # check for outliers
    for i in range(1,N):
        for j in range(0,i):
            if matrix[i][j] == 1:
                if i < corner or j > corner-cel:
                    print("edge",i,j,"is an outlier compared to",corner,corner-1)

if __name__ == '__main__':
    print("don't run me directly")
    
    # edgelist = [[0,28],[28,1],[1,27],[1,26],[27,3],[27,4],[27,5],[27,6], \
    #             [27,7],[27,8],[27,9],[3,20],[5,21],[7,22],[9,23],[3,16], \
    #             [5,17],[7,18],[4,14],[6,15],[27,19],[6,13],[19,25],  \
    #             [19,24],[8,12],[8,11],[4,2],[9,10]]
    # edgelist = [[0,7],[7,3],[3,2],[2,4],[4,1],[1,6],[6,0]] # 7-cycle, not alpha
    # edgelist = [[0,8],[8,1],[1,7],[7,3],[3,6],[6,4],[4,5],[5,0]] # 8-cycle, is alpha
    
    # the 5 solutions for the same basic lobster
    # edgelist = [[0,6],[6,1],[1,5],[5,2],[1,3],[3,4]]
    # edgelist = [[2,0],[0,6],[6,1],[1,5],[6,3],[3,4]]
    # edgelist = [[4,0],[0,6],[6,1],[1,2],[6,3],[3,5]]
    # edgelist = [[5,0],[0,6],[6,2],[2,3],[6,4],[4,1]]
    # edgelist = [[4,0],[0,6],[6,1],[1,3],[6,5],[5,2]]
    
    # matrix = edgelist_to_matrix(edgelist)
    # print_matrix(matrix)
    # is_box(matrix)
    
    