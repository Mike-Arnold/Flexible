
import csv

### file handling ###

def start_new_file(filename,line_info):
    with open(filename, mode='w', newline='') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(line_info)

def write_line_to_file(filename,line_info):
    with open(filename, mode='a+', newline='') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(line_info)

def write_results(filename,results_data):
    with open(filename, mode='a+', newline='') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line_info in results_data:
            results_writer.writerow(line_info)

def read_sample_trees(filename):
    sample_trees = {}
    
    with open(filename, newline='') as csvfile:
        tree_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(tree_csv, None)  # skip the headers
        for row in tree_csv:
            level = eval(row[1])
            num_nodes = len(level)
            if num_nodes not in sample_trees.keys(): # add keys as necessary
                sample_trees[num_nodes] = []
            sample_trees[num_nodes].append(level)
    return sample_trees

if __name__ == '__main__':
    print("don't run me directly")