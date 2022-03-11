import re

'''
find_pharmacy(): will find all the possible available Pharmacies with the minimum containment zones
                 with respect to the Harsh's House (which is a source node)
                 
                 This function takes 3 parameters:
                     (i) nodes - means total no of Pharmacies
                     (ii) edges - consists of no of containment zones lying between 2 Pharmacies
                     (iii) source_index - Harsh's House
''' 

def find_pharmacy(nodes, edges, source_index = 1):
    
    # marking all Pharmacies having infinite containment zones initially
    path_lengths = {v: float('inf') for v in nodes}
    path_trace = {v: 'a' for v in nodes}
    
    # marking Harsh's house having 0 containment zone as it's the source node
    path_lengths[source_index] = 0
    
    # storing all the Pharmacy and containment zone details in 2D dictionary format
    adjacent_nodes = {v: {} for v in nodes}
    for (u,v), c_uv in edges.items():
        adjacent_nodes[u][v] = c_uv
        adjacent_nodes[v][u] = c_uv
    
    # calculating actual containment zones lying between each pair of Pharmacies
    temporary_nodes = [v for v in nodes]
    while len(temporary_nodes) > 0:
        upper_bounds = {v: path_lengths[v] for v in temporary_nodes}
        
        # finding a Pharmacy having the minimum containment zones and then removing that node from temporary nodes
        u = min(upper_bounds, key=upper_bounds.get)
        temporary_nodes.remove(u)
        
        # updating the containment zone no if we found another path having minimum containment zone value
        for v, c_uv in adjacent_nodes[u].items():
            if path_lengths[v] > (path_lengths[u] + c_uv):
                path_trace[v] = path_trace[u] + " " + chr(v+96)
            path_lengths[v] = min(path_lengths[v], path_lengths[u] + c_uv)
    
    # finally returning details of all Pharmacies along with their minimum containment zones
    return path_lengths, path_trace


# reading the input file
input_file = open("inputPS4.txt","r")
src = input_file.read()

# Data Extraction from Input File
pattern01 = "([a-z])\s/\s([a-z])\s/\s(\d+)"
pattern02 = "Harsh\Ss House:\s([a-z])"
pattern03 = "Pharmacy\s(\d+):\s([a-z])"
details01 = re.findall(pattern01, src)
details02 = re.findall(pattern02, src)
details03 = re.findall(pattern03, src)
input_file.close()

# storing the edges and nodes details from the input file
edges = {}
nodes = []
for x,y,z in details01:
    edges[(ord(x)-96,ord(y)-96)] = float(z)
    if ord(x)-96 not in nodes:
        nodes.append(ord(x)-96)
    if ord(y)-96 not in nodes:
        nodes.append(ord(y)-96)
        
# storing harsh house, pharmacy 1 and pharmacy 2 details
harsh_house = ord(details02[0])-96
pharmacy_data = {k: v for k,v in details03}

# executing the algorithm
containment_zone, trace = find_pharmacy(nodes, edges, harsh_house)
final_containment_zone = {}
final_trace = {}
for k,v in containment_zone.items():
    final_containment_zone[chr(k+96)] = v
for k,v in trace.items():
    final_trace[chr(k+96)] = v

# generating the output file
output_file = open("outputPS4.txt","w")

safer_pharmacy = pharmacy_data[min(pharmacy_data, key=pharmacy_data.get)]
safer_pharmacy_no = "Pharmacy " + str(min(pharmacy_data, key=pharmacy_data.get))

path_to_follow = final_trace[safer_pharmacy]
total_containment_zones = str(int(final_containment_zone[safer_pharmacy]))

final_result = "Safer Pharmacy is: " + safer_pharmacy_no + "\n" + "Path to follow: " + path_to_follow + "\n" + "Containment zones on this path: " + total_containment_zones

output_file.write(final_result)
output_file.close()
