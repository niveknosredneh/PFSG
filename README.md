# PFSG - Python Filesystem Grapher

Uses matplotlib, networkx and graphviz to create a beautiful graph of directory structure and exports as a png image for use as desktop wallpaper

## Prerequisites

Tested only on ubuntu 18.04

Ubuntu and Debian based:
```
# Dependencies:
sudo apt-get install python3 python3-pip imagemagick feh
sudo pip3 install networkx graphviz click
```
(untested) Arch based:
```
# Mandatory dependencies:
sudo pacman -S python3 python3-pip python-pygraphviz imagemagick feh
sudo pip3 install networkx graphviz click
```

## Installing
```
git clone https://github.com/niveknosredneh/PFSG.git
cd PFSG && sudo chmod +x pfsg.py
...
```

## Options
```
  -w, --width INTEGER           Graph width
  -h, --height INTEGER          Graph height
  -l, --layout TEXT             Layout style: dot|twopi|neato|fdp|sfdp|circo
  -i, --image TEXT              Image file for graph to overlay ontop of
  -o, --opacity INTEGER         Opacity of graph when overlaid on image
  -b, --background-colour TEXT  Background colour in form '#RRGGBBAA'
  -d, --max-depth INTEGER       Max node depth
  -f, --show-files              Shows file nodes
  --show-file-labels            Shows file labels
  --label-size INTEGER          Font size for labels
  --label-size-reduce FLOAT     Amount to reduce label size by depth
  --label-colour TEXT           Font colour in form '#RRGGBBAA'
  --label-depth INTEGER         Max depth to draw labels
  --file-label-size INTEGER     Font size for file labels
  --file-label-colour TEXT      Font colour in form '#RRGGBBAA'
  --edge-width FLOAT            Edge line width
  --edge-width-reduce FLOAT     Amount to reduce edge width by depth
  --edge-length FLOAT           Minimum edge length in inches
  --edge-colour TEXT            Edge colour in form '#RRGGBBAA'
  --edge-style TEXT             Edge style: solid|dashed|dotted|dashdot
  --splines TEXT                Edge style: none|line|curved|ortho
  --node-size FLOAT             Node dot size, set to zero to disable
  --node-colour TEXT            Node colour in form '#RRGGBBAA'
  --file-node-size FLOAT        Node dot size, set to zero to disable
  --file-node-colour TEXT       Node colour in form '#RRGGBBAA'
  --dim INTEGER                 Number of dimensions to graph in
  -s, --set-wallpaper           Sets output image as wallpaper using feh
  --help                        Show this message and exit.
```

## Authors

* **Kevin Matthew Henderson**

## Contributors

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/niveknosredneh/PFSG/blob/master/LICENSE) file for details
