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
@click.option("--layout", "-l",  default="dot", help="Layout style: dot|twopi|neato|fdp|sfdp|circo ")
@click.option("--image",  "-i",  default=None, help="Image file for graph to overlay ontop of")
@click.option("--opacity",  "-o",  default=60, help="Opacity of graph when overlaid on image")
@click.option("--background-colour", "-b",   default="#222222FF", help="Background colour in form '#RRGGBBAA'")
@click.option("--max-depth",  "-d", default=48, help="Max node depth")
@click.option("--show-files", "-f",  default=False, is_flag=True, help="Shows file nodes")
@click.option("--show-file-labels", default=False, is_flag=True, help="Shows file labels, restricted by label-depth")
@click.option("--label-depth",  default=10, help="Max depth to draw labels")
@click.option("--label-size",  default=12, help="Font size for labels")
@click.option("--label-size-reduce",  default=1.0, help="Amount to reduce label size by depth")
@click.option("--label-alpha",  default=0.8, help="Label alpha")
@click.option("--label-alpha-reduce",  default=0.07, help="Amount to reduce label alpha by depth")
@click.option("--label-colour",  default="#FFFFFFFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--file-label-size", default=8, help="Font size for file labels")
@click.option("--file-label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--edge-width", default=0.5, help="Edge line width")
@click.option("--edge-width-reduce", default=0.3, help="Amount to reduce edge width by depth")
@click.option("--edge-colour", default="#555555FF", help="Edge colour in form '#RRGGBBAA' or      matplotlib colormap, see readme")
@click.option("--edge-style", default="solid", help="Edge style: solid|dashed|dotted|dashdot ")
@click.option("--node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--node-colour", default="#555555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--file-node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--file-node-colour", default="#FF5555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--set-wallpaper", "-s",  default=False, is_flag=True, help="Sets output image as wallpaper using feh")
@click.option("--verbose", "-v",  default=False, is_flag=True, help="Display more output than necessary")
def main(
directory, output, layout, 
width, height, max_depth, 
label_size, label_colour, label_depth, label_size_reduce, label_alpha_reduce, label_alpha, 
background_colour, image, opacity,   
edge_colour, edge_width, edge_style, edge_width_reduce, 
node_colour, node_size, 
show_files, file_node_colour, file_node_size, file_label_colour, file_label_size, show_file_labels, 
set_wallpaper, verbose):
    """ 
    PFSG - Python Filesystem Grapher
    
    Uses matplotlib and networkx to create graph of a directory structure and exports to png image for use as desktop wallpaper
    """

    if edge_colour[0]=="#": edge_colourmap = None
    else: edge_colourmap = plt.get_cmap(edge_colour)
    if node_colour[0]=="#": node_colourmap = None
    else: node_colourmap = plt.get_cmap(node_colour)
    
    nodes_by_depth = []
    nodes_by_depth.append([])
    edges_by_depth = []
    edges_by_depth.append([])
    edge_colours_by_depth = []
    edge_colours_by_depth.append([])
    node_colours_by_depth = []
    node_colours_by_depth.append([])
    labels_by_depth = [{}]
    file_nodes = []
 
    print("Creating Network and Adding Nodes ...")
    G = nx.Graph() # create graph
    base_depth = len(directory.split("/"))
    deepest = 0 # keeps track of max folder depth
    num_nodes = 1
    G.add_node(directory,  file='False',  depth=0,  label=directory.split("/")[-1])
    nodes_by_depth[0].append(directory)
    labels_by_depth[0][directory] = directory.split("/")[-1]
    for (dirpath, dirnames, filenames) in os.walk(directory):
        cur_depth = len(dirpath.split("/"))-base_depth + 1
        if cur_depth > deepest: 
            deepest = cur_depth
            labels_by_depth.append({})
            edges_by_depth.append([])
            nodes_by_depth.append([])
            edge_colours_by_depth.append([])
        if cur_depth < max_depth:
            if show_files:
                for f in filenames: # FILES
                    new_label = ""
                    if cur_depth < label_depth: new_label = f
                    G.add_node(os.path.join(dirpath, f),  file='True',  depth=cur_depth,  label=new_label)
                    G.add_edge(dirpath ,  os.path.join(dirpath, f), file='True',  depth=cur_depth)
                    num_nodes+=1
                    file_nodes.append(os.path.join(dirpath, f))
                    edges_by_depth[cur_depth].append((dirpath ,  os.path.join(dirpath, f)))
                    if show_file_labels: labels_by_depth[cur_depth][os.path.join(dirpath, f)] = new_label
                    edge_colours_by_depth[cur_depth].append(cur_depth)

            for d in dirnames: # DIRECTORIES
                    new_label = ""
                    if cur_depth < label_depth: new_label = d
                    G.add_node(os.path.join(dirpath, d),  file='False', depth=cur_depth,  label=new_label)
                    G.add_edge(dirpath ,  os.path.join(dirpath, d),  file='False',  depth=cur_depth)
                    num_nodes+=1
                    nodes_by_depth[cur_depth].append(os.path.join(dirpath, d))
                    edges_by_depth[cur_depth].append((dirpath ,  os.path.join(dirpath, d)))
                    labels_by_depth[cur_depth][os.path.join(dirpath, d)] = new_label
                    edge_colours_by_depth[cur_depth].append(cur_depth)

    print("Added " + str(num_nodes) + " Nodes")
    print("Calculating Layout ...")
    pos = graphviz_layout(G, prog=layout)#, root=1) # use layout
    fig = plt.figure(figsize=(width/100.0, height/100.0)) # set figure size
    
    # DRAW
    print("Drawing Graph ...")
    #nodes
    for i, nodes in enumerate(nodes_by_depth):
        if node_colourmap: node_colour = [i] * len(nodes)
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=node_size, node_color=node_colour, cmap=node_colourmap, vmin=0, vmax=deepest)
    nx.draw_networkx_nodes(G, pos, nodelist=file_nodes, node_size=file_node_size, node_color=file_node_colour)
    #edges
    for i, edges in enumerate(edges_by_depth):
            width=(edge_width-i*edge_width_reduce)
            if edge_colourmap: edge_colour = [i] * len(edges)
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colour, width=width, edge_cmap=edge_colourmap, style=edge_style,  edge_vmin=0,edge_vmax=deepest,  alpha=1)
    #labels
    for i, labels in enumerate(labels_by_depth):
        new_label_size = int(int(label_size) - i * int(label_size_reduce))
        new_label_alpha = label_alpha / (label_alpha_reduce*i + 1)
        if i==0: new_label_alpha = 1
        nx.draw_networkx_labels(G, pos, labels=labels ,  font_color=label_colour, font_size=new_label_size,  alpha=new_label_alpha)
    
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

if __name__ == '__main__':
    main()
    print("Done!")
