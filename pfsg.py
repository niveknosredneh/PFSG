#!/usr/bin/env python3

# Kevin Matthew Henderson - May 18, 2019

from networkx.drawing.nx_pydot import graphviz_layout
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
@click.option("--background-colour", "-b",   default="#333333FF", help="Background colour in form '#RRGGBBAA'")
@click.option("--depth",  "-d", default=48, help="Max node depth")
@click.option("--label-depth",  default=10, help="Max depth to draw labels")
@click.option("--label-size",  default=12, help="Font size for labels")
@click.option("--label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--file-label-size", default=8, help="Font size for file labels")
@click.option("--file-label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--edge-width", default=0.5, help="Edge line width")
@click.option("--edge-colour", default="#555555FF", help="Edge colour in form '#RRGGBBAA'")
@click.option("--edge-colourmap", help="Edge colourmap based on depth, see readme for list")
@click.option("--edge-style", default="solid", help="Edge style: solid|dashed|dotted|dashdot ")
@click.option("--node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--node-colour", default="#555555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--file-node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--file-node-colour", default="#FF5555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--show-files", "-f",  default=False, is_flag=True, help="Shows file nodes")
@click.option("--show-file-labels", default=False, is_flag=True, help="Shows file labels, restricted by label-depth")
@click.option("--set-wallpaper", "-s",  default=False, is_flag=True, help="Sets output image as wallpaper using feh")
@click.option("--verbose", "-v",  default=False, is_flag=True, help="Display more output than necessary")
def main(
directory, output, layout, 
width, height, depth, 
label_size, label_colour, label_depth, 
background_colour, image, opacity,   
edge_colour, edge_width, edge_style, edge_colourmap, 
node_colour, node_size, 
show_files, file_node_colour, file_node_size, file_label_colour, file_label_size, show_file_labels, 
set_wallpaper, verbose):
    """ 
    PFSG - Python Filesystem Grapher
    
    Uses matplotlib and networkx to create graph of given directory structure and exports to png image for use as desktop wallpaper
        
    """
    G = nx.Graph() # create graph
    base_depth = len(directory.split("/"))-1
    deepest = 0 # keeps track of max folder depth
    
    file_nodes = []
    file_edges = []
    file_labels = {}
    dir_nodes = []
    dir_edges = []
    dir_labels = {}
    
    edge_colours = []
    
    G.add_node(directory,  file='False',  depth=0,  label=directory.split("/")[-1])
    dir_nodes.append(directory)
    dir_labels[directory] = directory.split("/")[-1]
    for (dirpath, dirnames, filenames) in os.walk(directory):
        cur_depth = len(dirpath.split("/"))-base_depth
        if cur_depth > deepest: deepest = cur_depth
        print(cur_depth)
        if show_files:
            for f in filenames: # FILES
                new_label = ""
                if cur_depth < label_depth: new_label = f
                G.add_node(os.path.join(dirpath, f),  file='True',  depth=cur_depth,  label=new_label)
                G.add_edge(dirpath ,  os.path.join(dirpath, f), file='True',  depth=cur_depth)
                file_nodes.append(os.path.join(dirpath, f))
                file_edges.append((dirpath ,  os.path.join(dirpath, f)))
                file_labels[os.path.join(dirpath, f)] = new_label
                file_edges.append((dirpath ,  os.path.join(dirpath, f)))
                edge_colours.append(cur_depth)
        for d in dirnames: # DIRECTORIES
                new_label = ""
                if cur_depth < label_depth: new_label = d
                print(new_label)
                G.add_node(os.path.join(dirpath, d),  file='False', depth=cur_depth,  label=new_label)
                G.add_edge(dirpath ,  os.path.join(dirpath, d),  file='False',  depth=cur_depth)
                dir_nodes.append(os.path.join(dirpath, d))
                dir_edges.append((dirpath ,  os.path.join(dirpath, d)))
                dir_labels[os.path.join(dirpath, d)] = new_label   
                dir_edges.append((dirpath ,  os.path.join(dirpath, d)))
                edge_colours.append(cur_depth)
    
    
    pos = graphviz_layout(G, prog=layout, root=1) # use layout
    fig = plt.figure(figsize=(width/100.0, height/100.0)) # set figure size
    
    # DRAW
    nx.draw_networkx_nodes(G, pos, nodelist=dir_nodes, node_size=node_size, node_color=node_colour)
    nx.draw_networkx_nodes(G, pos, nodelist=file_nodes, node_size=file_node_size, node_color=file_node_colour)
    
    nx.draw_networkx_edges(G, pos, cmap=plt.get_cmap(edge_colourmap),  edge_color=edge_colours, width=edge_width,  style=edge_style,  edge_vmin=0,edge_vmax=deepest)
    
    if show_file_labels: nx.draw_networkx_labels(G, pos, labels=file_labels ,  font_color=file_label_colour, font_size=file_label_size,  alpha=1)
    nx.draw_networkx_labels(G, pos, labels=dir_labels ,  font_color=label_colour, font_size=label_size,  alpha=1)
    plt.axis('off')
    #plt.axis('equal')
    
    if image: fig.set_facecolor('#00000000') # for transparency
    else: fig.set_facecolor(background_colour)
    
    # SAVE
    plt.savefig(output, facecolor=fig.get_facecolor() )
    plt.close()
    
    
    # depends on imagemagick
    if image: out = subprocess.call(['composite',  '-blend',  opacity,  output, image,  output])
    # depends on feh
    if set_wallpaper: out = subprocess.call(['feh',  '--bg-scale',  output])

if __name__ == '__main__':
    main()
