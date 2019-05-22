#!/usr/bin/env python3
# Kevin Matthew Henderson - May 18, 2019

from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import os
import subprocess
import click

@click.command()
@click.argument('directory', nargs=1)
@click.argument("output", nargs=1)
@click.option("--width", "-w",  default=1920, help="Graph width")
@click.option("--height", "-h",  default=1080, help="Graph height")
@click.option("--layout", "-l",  default="neato", help="Layout style: dot|twopi|neato|fdp|sfdp|circo ")
@click.option("--image",  "-i",  default=None, help="Image file for graph to overlay ontop of")
@click.option("--opacity",  "-o",  default=60, help="Opacity of graph when overlaid on image")
@click.option("--background-colour", "-b",   default="#222222FF", help="Background colour in form '#RRGGBBAA'")
@click.option("--max-depth",  "-d", default=48, help="Max node depth")
@click.option("--show-files", "-f",  default=False, is_flag=True, help="Shows file nodes")
@click.option("--show-file-labels", default=False, is_flag=True, help="Shows file labels, restricted by label-depth")
@click.option("--label-depth",  default=10, help="Max depth to draw labels")
@click.option("--label-size",  default=12, help="Font size for labels")
@click.option("--label-size-reduce",  default=1.0, help="Amount to reduce label size by depth")
@click.option("--label-alpha",  default=1, help="Label alpha")
@click.option("--label-alpha-reduce",  default=0.1, help="Amount to reduce label alpha by depth")
@click.option("--label-colour",  default="#FFFFFFFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--file-label-size", default=8, help="Font size for file labels")
@click.option("--file-label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--edge-width", default=0.5, help="Edge line width")
@click.option("--edge-width-reduce", default=0.3, help="Amount to reduce edge width by depth")
@click.option("--edge-colour", default="#555555FF", help="Edge colour '#RRGGBBAA' or matplotlib colormap")
@click.option("--edge-style", default="solid", help="Edge style: solid|dashed|dotted|dashdot ")
@click.option("--node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--node-colour", default="#555555FF", help="Node colour '#RRGGBBAA' or matplotlib colormap")
@click.option("--file-node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--file-node-colour", default="#FF5555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--colourmap-soften", default="0", help="Adds buffer to colourmap range")
@click.option("--map-by-size", "-m",  default=False, is_flag=True, help="Maps colours by file size rather than depth")
@click.option("--set-wallpaper", "-s",  default=False, is_flag=True, help="Sets output image as wallpaper using feh")
@click.option("--verbose", "-v",  default=False, is_flag=True, help="Display more output than necessary")
def main(
directory, output, layout, 
width, height, max_depth, 
label_size, label_colour, label_depth, label_size_reduce, label_alpha_reduce, label_alpha, 
background_colour, image, opacity,   
edge_colour, edge_width, edge_style, edge_width_reduce, 
node_colour, node_size, map_by_size, colourmap_soften, 
show_files, file_node_colour, file_node_size, file_label_colour, file_label_size, show_file_labels, 
set_wallpaper, verbose):
    """ 
    PFSG - Python Filesystem Grapher
    
    Uses matplotlib and networkx to create graph of a directory structure and exports to png image for use as desktop wallpaper
    """
    # throw error early if colormap not valid
    if edge_colour[0]=="#": edge_colourmap = None
    else: edge_colourmap = plt.get_cmap(edge_colour)
    if node_colour[0]=="#": node_colourmap = None
    else: node_colourmap = plt.get_cmap(node_colour)
    if file_node_colour[0]=="#": file_node_colourmap = None
    else: file_node_colourmap = plt.get_cmap(file_node_colour)
    
    print("Creating Network and Adding Nodes ...")
    G = nx.Graph() # create graph
    base_depth = len(directory.split("/"))
    deepest = 0 # keeps track of max folder depth
    largest = 0
    num_nodes = 1
    files = []
    G.add_node(directory,  file='False',  depth=0,  label=directory.split("/")[-1],  size=0)
    for (dirpath, dirnames, filenames) in os.walk(directory):
        cur_depth = len(dirpath.split("/"))-base_depth + 1
        if cur_depth > deepest: 
            deepest = cur_depth
        if cur_depth < max_depth:
            if show_files:
                for f in filenames: # FILES
                    new_label = ""
                    size=os.path.getsize(os.path.join(dirpath, f))
                    if size > largest: largest = size
                    if cur_depth < label_depth: new_label = f
                    G.add_node(os.path.join(dirpath, f),  file='True',  depth=cur_depth,  label=new_label,   size=size)
                    G.add_edge(dirpath ,  os.path.join(dirpath, f), file='True',  depth=cur_depth, label=size,  size=size)
                    num_nodes+=1
                    files.append(os.path.join(dirpath, f))
            for d in dirnames: # DIRECTORIES
                    new_label = ""
                    size=os.path.getsize(os.path.join(dirpath, d))
                    if cur_depth < label_depth: new_label = d
                    G.add_node(os.path.join(dirpath, d),  file='False', depth=cur_depth,  label=new_label,  size=size)
                    G.add_edge(dirpath ,  os.path.join(dirpath, d),  file='False',  depth=cur_depth,   label=size,  size=size)
                    num_nodes+=1

    print("Added " + str(num_nodes) + " Nodes")
    print("Calculating Layout ...")
    pos = graphviz_layout(G, prog=layout)#, root=1) # use layout
    fig = plt.figure(figsize=(width/100.0, height/100.0)) # set figure size
    
    # DRAW
    print("Drawing Graph ...")
    #nodes
    node_depth = nx.get_node_attributes(G,'depth')
    edge_depth = nx.get_edge_attributes(G,  'depth')
    node_labels =  nx.get_node_attributes(G,  'label')
    edge_labels =  nx.get_edge_attributes(G,  'label')
    node_size = nx.get_node_attributes(G,'size')
    edge_size = nx.get_edge_attributes(G,'size')
    is_file = nx.get_node_attributes(G,'file')
    
    vmin=0
    if map_by_size: vmax = largest + int(colourmap_soften)
    else: vmax = deepest + int(colourmap_soften)
    
    for file in files:
        path = file
        while len(path.split("/")) > base_depth:
            edge_size[(os.path.dirname(path), path)]= int(edge_size[(os.path.dirname(path), path)])+int(node_size[file]) 
            path = os.path.dirname(path)
            new_size = int(node_size[path])+int(node_size[file]) 
            if new_size > largest:# and path != directory: 
                largest = new_size # 
            node_size[path]= new_size

    for node, depth in node_depth.items():
        if map_by_size: var = node_size[node]
        else: var = depth
        if node_colourmap: node_colour = [var]
        if file_node_colourmap: file_node_colour = [var]
        if is_file[node]==False: # is dir
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=node_size, node_color=node_colour, cmap=node_colourmap, vmin=vmin, vmax=vmax)
        else: # is file
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=file_node_size, node_color=file_node_colour, cmap=file_node_colourmap, vmin=vmin, vmax=vmax)
    #edges
    for edge, depth in edge_depth.items():
            if map_by_size: var = node_size[edge[0]]
            else: var = depth
            width=(edge_width-depth*edge_width_reduce)
            if edge_colourmap: edge_colour = [var]
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=edge_colour, width=width, edge_cmap=edge_colourmap, style=edge_style,  edge_vmin=vmin,edge_vmax=vmax,  alpha=1)
   #labels
    for node, label in node_labels.items():
        #label = node_size[node]#debug
        if map_by_size:
            new_label_size = int( int(label_size) * (node_size[node] / largest) )
            new_label_alpha = label_alpha * (node_size[node] / largest)
        else:    
            new_label_size = int(int(label_size) - int(node_depth[node]) * int(label_size_reduce))
            new_label_alpha = label_alpha / (label_alpha_reduce*int(node_depth[node]) + 1)
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
    if image:
        print("Overlaying Over Image ...") 
        out = subprocess.call(['composite',  '-blend',  str(opacity),  output, image,  output])
    # depends on feh
    if set_wallpaper: 
        print("Setting Wallpaper ...") 
        out = subprocess.call(['feh',  '--bg-scale',  output])
        print("Done!")
        
if __name__ == '__main__':
    main()
