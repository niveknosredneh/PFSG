#!/usr/bin/env python3
# Kevin Matthew Henderson - June 14, 2019

from networkx.drawing.nx_pydot import write_dot
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
@click.option("--show-file-labels", default=False, is_flag=True, help="Shows file labels")
@click.option("--label-size",  default=16, help="Font size for labels")
@click.option("--label-size-reduce",  default=2.0, help="Amount to reduce label size by depth")
@click.option("--label-colour",  default="#FFFFFFFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--label-depth",  default=10, help="Max depth to draw labels")
@click.option("--file-label-size", default=8, help="Font size for file labels")
@click.option("--file-label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--edge-width", default=2.0, help="Edge line width")
@click.option("--edge-width-reduce", default=0.03, help="Amount to reduce edge width by depth")
@click.option("--edge-length", default=1.0, help="Min edge length in inches, fdp/neato only")
@click.option("--edge-colour", default="#555555FF", help="Edge colour in form '#RRGGBBAA'")
@click.option("--edge-style", default="solid", help="Edge style: solid|dashed|dotted|dashdot ")
@click.option("--splines", default="curved", help="Edge style: none|line|curved|ortho ")
@click.option("--node-size", default=0.1, help="Node dot size, set to zero to disable")
@click.option("--node-colour", default="#555555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--file-node-size", default=0.05, help="Node dot size, set to zero to disable")
@click.option("--file-node-colour", default="#FF5555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--dim", default=2, help="Number of dimensions to graph in")
@click.option("--set-wallpaper", "-s",  default=False, is_flag=True, help="Sets output image as wallpaper using feh")
@click.option("--quiet", "-q",  default=False, is_flag=True, help="Restricts verbosity to errors and warnings")
def main(
directory, output, layout, width, height, max_depth, 
label_size, label_colour, label_size_reduce, label_depth, 
background_colour, image, opacity,   
edge_colour, edge_width, edge_style, edge_width_reduce, splines, edge_length, 
node_colour, node_size, show_files, file_node_colour, file_node_size, 
file_label_colour, file_label_size, show_file_labels, set_wallpaper,  dim,  quiet):
    """ 
    PFSG - Python Filesystem Grapher
    Uses networkx and graphviz to create graph of a directory structure and exports to png image for use as desktop wallpaper
    """
    if not quiet: print("Creating Network and Adding Nodes ...")
    G = nx.Graph( ) # create graph
    base_depth = len(directory.split("/"))
    deepest = 0 # keeps track of max folder depth
    num_dirs = 1
    num_files = 0 
    G.add_node(directory,  file='False',  depth=0,  label=directory.split("/")[-1],    shape="plain",  color=node_colour,  fontcolor=label_colour,  fontsize=int(label_size))
    for (dirpath, dirnames, filenames) in os.walk(directory):
        cur_depth = len(dirpath.split("/"))-base_depth + 1
        if cur_depth > deepest: deepest = cur_depth
        if cur_depth < max_depth:
            if show_files:
                for f in filenames: # FILES
                    new_label = ""
                    shape = "plain"
                    if cur_depth < label_depth and show_file_labels: new_label = f
                    else: shape = "point"
                    G.add_node(os.path.join(dirpath, f),  file='True',  depth=cur_depth,  label=new_label,   shape=shape,  color=file_node_colour,  fontcolor=file_label_colour,  fontsize=int(file_label_size),  width=file_node_size,  z=cur_depth,  group=2)
                    G.add_edge(dirpath ,  os.path.join(dirpath, f), file='True',  fontcolor=label_colour, style=edge_style, depth=cur_depth,  arrowsize=edge_width/3,  len=edge_length,  color=edge_colour,  penwidth=(edge_width-edge_width_reduce*cur_depth) )
                    num_files+=1
            for d in dirnames: # DIRECTORIES
                    new_label = ""
                    shape = "plain"
                    if cur_depth < label_depth: new_label = d
                    else: shape = "point"
                    G.add_node(os.path.join(dirpath, d),  file='False', depth=cur_depth,  label=new_label,  shape=shape,  color=node_colour,  fontcolor=label_colour,  fontsize=int(label_size - label_size_reduce * cur_depth), width=node_size,  z=cur_depth)
                    G.add_edge(dirpath ,  os.path.join(dirpath, d),  file='False',  fontcolor=label_colour,  style=edge_style, depth=cur_depth,  arrowsize=edge_width/3,  len=edge_length,  color=edge_colour,  penwidth=(edge_width-edge_width_reduce*cur_depth))
                    num_dirs+=1
    if not quiet: print("Added " + str(num_dirs) + " Directories and " + str(num_files) + " Files \nMaking " + str(num_dirs + num_files) + " total Nodes, " + str(deepest) + " directories deep")
    write_dot(G, 'graph.dot')
    
    if not quiet: print("Calculating Layout ...")
    with open(output, "w") as outfile: # uses outputfile as output for neato using stdout
        subprocess.call(['neato', '-Tpng', '-K'+layout,   f"-Gsplines={splines}",  f"-Gbgcolor={background_colour}", f"-Gdimen={dim}", "-GquadType=fast",  'graph.dot'], stdout=outfile)
        
    if not quiet: print("Using Imagemagick to resize ...")
    out = subprocess.call(['convert',  output,  '-background', background_colour , output])
    out = subprocess.call(['convert',  output,  '-fuzz',  '20%', '-transparent', background_colour, output])       
    #out = subprocess.call(['convert',  output,  "-sample",  f"{width}x{height}!" ,  output])
    out = subprocess.call(['convert',  output,  '-background', background_colour , "-gravity", "center", "-extent",  f"{width}x{height}>" ,  output])

    if image:
        if not quiet: print("Overlaying Over Image ...") 
        out = subprocess.call(['composite',  '-blend',  str(opacity),  output, image,  output])
    if set_wallpaper: 
        if not quiet: print("Setting Wallpaper ...") 
        out = subprocess.call(['feh',  '--bg-scale',  output])
        
if __name__ == '__main__':
    main()
