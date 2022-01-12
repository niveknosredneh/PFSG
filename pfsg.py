#!/usr/bin/env python3
# Kevin Matthew Henderson - 2022

directory="~/Code" 
output="twopi.jpg"

# scan Init process tree if True, instead of filesystem if False
process=True 

layout="fdp" # neato|twopi|sfdp|fdp|dot|circo
width=1920
height=1080

background_colour="#000000FF"
image="./debian.png" # path of background image to underlay, or None
#image=None
opacity=40

max_depth=7 # currently crashes (for me) with huge number of files / dirs
label_size=12
label_colour="#000000FF"
label_depth=10
label_size_reduce=1.0
label_alpha_reduce=0.3
label_alpha=1.0

edge_colour="#666666FF" #RRGGBBAA' or matplotlib colormap
edge_width=1.0
edge_style="dotted" #solid|dashed|dotted|dashdot
edge_width_reduce=0
edge_length=10.0 #fdp/neato only

node_colour="#222222FF" #RRGGBBAA' or matplotlib colormap
node_size=1.0

file_node_colour="#22FF22FF"
file_node_size=1.0
file_label_colour="#FF2222FF"
file_label_size=12
show_file_labels=False 
map_by_size=False
colourmap_soften=0
show_files=False # if False only shows directories

set_wallpaper=True # uses 'feh'
verbose=True



"""
PFSG - Python Filesystem Grapher

Uses matplotlib and networkx to create graph of a directory structure and exports to png image for use as desktop wallpaper
"""


from networkx.drawing.nx_pydot import graphviz_layout
#from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
import networkx as nx
import os
import subprocess

import psutil

# throw error early if colormap not valid
if edge_colour[0]=="#": edge_colourmap = None
else: edge_colourmap = plt.get_cmap(edge_colour)
if node_colour[0]=="#": node_colourmap = None
else: node_colourmap = plt.get_cmap(node_colour)
if file_node_colour[0]=="#": file_node_colourmap = None
else: file_node_colourmap = plt.get_cmap(file_node_colour)

print("Creating Network and Adding Nodes ...")
G = nx.Graph() # create graph

deepest = 0 # keeps track of max folder depth
largest = 0
num_nodes = 1
if not process:
    base_depth = len(directory.split("/"))

    files = {}
    G.add_node(directory,  file='False',  depth=0,  label=directory.split("/")[-1],  size=0)
    for (dirpath, dirnames, filenames) in os.walk(directory):
        cur_depth = len(dirpath.split("/"))-base_depth + 1
        if cur_depth > deepest: 
            deepest = cur_depth
        if cur_depth < max_depth:
            for f in filenames: # FILES
                new_label = ""
                size = 0
                if map_by_size: 
                    size=os.path.getsize(os.path.join(dirpath, f))
                    files[os.path.join(dirpath, f)] = size
                if size > largest: largest = size
                if cur_depth < label_depth and show_file_labels: new_label = f
                if show_files:
                    G.add_node(os.path.join(dirpath, f),  file='True',  depth=cur_depth,  label=new_label,   size=size)
                    G.add_edge(dirpath ,  os.path.join(dirpath, f), file='True',  depth=cur_depth, label=size,  size=size)
                    num_nodes+=1

            for d in dirnames: # DIRECTORIES
                    new_label = ""
                    size = 0
                    if map_by_size: size=os.path.getsize(os.path.join(dirpath, d))
                    if cur_depth < label_depth: new_label = d
                    G.add_node(os.path.join(dirpath, d),  file='False', depth=cur_depth,  label=new_label,  size=size)
                    G.add_edge(dirpath ,  os.path.join(dirpath, d),  file='False',  depth=cur_depth,   label=size,  size=size)
                    num_nodes+=1
    print("Added " + str(num_nodes) + " Nodes")
    
else: # Processes, not filesystem
        
        root = psutil.Process(1)
        G.add_node(root.pid,  size=1,  file='False', depth=0,  label=f"{root.name()}")
        for p in root.children(recursive=True):
        #for p in psutil.process_iter(['pid', 'name', 'username']):
        
            if p.memory_percent()<1: mem=""
            else: mem = f"{int(p.memory_percent())}%"
            G.add_node(p.pid,  size=1,  file='False', depth=nx.shortest_path_length(G,root.pid,p.parent().pid),  label=f"{p.name()} {mem}")
            if not (p.parent() is None): G.add_edge(p.pid , p.parent().pid, depth=3)
            
            #par = p.parent().pid
            #while par is not root.pid:
            
print("Calculating Layout ...")
pos = graphviz_layout(G, prog=layout)#, root=1) # use layout
fig = plt.figure(figsize=(width/100.0, height/100.0)) # set figure size

# DRAW
print("Drawing Graph ...")
#nodes
node_depths = nx.get_node_attributes(G,'depth')
edge_depths = nx.get_edge_attributes(G,  'depth')
node_labels =  nx.get_node_attributes(G,  'label')
edge_labels =  nx.get_edge_attributes(G,  'label')
node_sizes = nx.get_node_attributes(G,'size')
edge_sizes = nx.get_edge_attributes(G,'size')
is_file = nx.get_node_attributes(G,'file')

vmin=0
if map_by_size: vmax = largest + int(colourmap_soften)
else: vmax = deepest + int(colourmap_soften)

if map_by_size:
    for file, size in files.items():
        path = file
        while len(path.split("/")) > base_depth:
            if G.has_edge(os.path.dirname(path), path):
                edge_sizes[(os.path.dirname(path), path)]= int(edge_sizes[(os.path.dirname(path), path)])+int(size) 
            path = os.path.dirname(path)
            new_size = int(node_sizes[path])+int(size) 
            if new_size > largest and path != directory: 
                largest = new_size # 
            if G.has_node(path):
                node_sizes[path]= new_size

for node, depth in node_depths.items():
    if map_by_size: var = node_sizes[node]
    else: var = depth
    if node_colourmap: node_colour = [var]
    if file_node_colourmap: file_node_colour = [var]
    if is_file[node]=="False": # is dir
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=node_size, node_color=node_colour, cmap=node_colourmap, vmin=vmin, vmax=vmax)
    else: # is file
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=file_node_size, node_color=file_node_colour, cmap=file_node_colourmap, vmin=vmin, vmax=vmax)
#edges
for edge, depth in edge_depths.items():
        if map_by_size: var = node_sizes[edge[1]]
        else: var = depth*3
        new_width=(edge_width- depth*edge_width_reduce)
        if edge_colourmap: edge_colour = [var]
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=edge_colour, width=new_width, edge_cmap=edge_colourmap, style=edge_style,  edge_vmin=vmin,edge_vmax=vmax,  alpha=1.0)
#labels
for node, label in node_labels.items():
    if map_by_size:
        new_label_size = int( int(label_size) * (node_sizes[node] / largest) )
        new_label_alpha = label_alpha * (node_sizes[node] / largest)
    else: # map by depth
        new_label_size = int(int(label_size) - (int(node_depths[node]) * int(label_size_reduce)))
        new_label_alpha = label_alpha / (label_alpha_reduce*int(node_depths[node]) + 1)
    nx.draw_networkx_labels(G, pos, labels={node:label} ,  font_color=label_colour, font_size=new_label_size,  alpha=new_label_alpha)
    #if int(node_size[node]) > largest/20: nx.draw_networkx_labels(G, pos, labels={node:node.split("/")[-1]} ,  font_color=label_colour, font_size=new_label_size,  alpha=new_label_alpha)


plt.axis('off')
#plt.axis('equal')
        
if image: fig.set_facecolor('#00000000') # for transparency
else: fig.set_facecolor(background_colour)

# SAVE
print("Saving File ...")
plt.savefig(output, facecolor=fig.get_facecolor() )
plt.close()

# depends on imagemagick
if image is not None:
    print("Overlaying Over Image ...") 
    out = subprocess.call(['composite',  '-blend',  str(opacity),  output, image,  output])
# depends on feh
if set_wallpaper: 
    print("Setting Wallpaper ...") 
    out = subprocess.call(['feh',  '--bg-scale',  output])
    print("Done!")
    
        
#if __name__ == '__main__':
#    main()
