#!/usr/bin/env python3

# Kevin Matthew Henderson - May 17, 2019

from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import networkx as nx
import os
import click

@click.command()
@click.argument('directory', nargs=1)
@click.argument("output", nargs=1)
@click.option("--width", "-w",  default=1920, help="Graph width")
@click.option("--height", "-h",  default=1080, help="Graph height")
@click.option("--label-size", "-f",  default=12, help="Font size")
@click.option("--label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--label-depth",  default=-1, help="Max depth to draw labels")
@click.option("--background-colour", "-b",   default="#333333FF", help="Background colour in form '#RRGGBBAA'")
@click.option("--edge-width", default=0.5, help="Edge line width")
@click.option("--edge-colour", default="#555555FF", help="Edge colour in form '#RRGGBBAA'")
@click.option("--node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--node-colour", default="#555555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--layout", "-l",  default="dot", help="Layout style: 'dot' or 'twopi'")
@click.option("--verbose", "-v",  default=False, is_flag=True, help="Display more output than necessary")
def main(directory, width,  height, label_size, label_colour, label_depth, background_colour,  edge_width,  node_colour , node_size,  edge_colour,  layout,  verbose, output):
    """ 
    PFSG - Python Filesystem Grapher
    
    Uses matplotlib and networkx to create graph of given directory structure and exports to png image for use as desktop wallpaper
    
    """

    G = nx.Graph() # create graph
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:
            if verbose: print('FILE :', os.path.join(dirpath, f))
            #G.add_edge(dirpath ,  os.path.join(dirpath, f))
        for d in dirnames:
            if verbose: print('DIRECTORY :', os.path.join(dirpath, d))
            G.add_edge(dirpath ,  os.path.join(dirpath, d))

    labels = {}
    base_depth = len(directory.split("/"))
    for idx, node in enumerate(G.nodes()):
        path_list =  node.split("/")
        if len(path_list)< label_depth + base_depth or label_depth == -1:
            labels[node] = path_list[-1]
            

    #use layout
    pos_twopi = graphviz_layout(G, prog=layout, root=1)
    fig = plt.figure(figsize=(width/100.0, height/100.0))

    nx.draw_networkx_nodes(G, pos_twopi, node_size=node_size, node_color=node_colour)
    nx.draw_networkx_edges(G, pos_twopi, edge_color=edge_colour, width=edge_width)
    #draw node labels
    nx.draw_networkx_labels(G, pos=graphviz_layout(G, prog=layout, root=1), labels=labels ,  font_color=label_colour, font_size=label_size,  alpha=1)
    plt.axis('off')
    #plt.axis('equal')

    #img = plt.imread("opportunity.png")
    #plt.imshow(img)
    #nx.draw(G, pos_twopi, node_color="#33333300" )#,  with_labels=True)
    
    fig.set_facecolor(background_colour)
    plt.savefig(output, facecolor=fig.get_facecolor() )
    plt.close()


if __name__ == '__main__':
    main()
