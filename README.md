# PFSG - Python Filesystem Grapher

Uses matplotlib and networkx to create graph of given directory structure and exports to png image for use as desktop wallpaper

## Examples

```
./pfsg.py ~/polybar dot.png --image /home/odroid/opportunity.png -l dot --file-node-colour "#BBBBBBFF" --show-files --file-node-size 15 --node-size 15 --label-size 20 --label-colour "#FFFFFFFF" --edge-colour "#999999FF" --edge-style dotted --edge-width 3 --label-depth 1
```
<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/dot.png" width="640" align="middle">

```
./pfsg.py /home/odroid/Code twopi.png -b "#000000FF" -l twopi --edge-colour "#666666FF" --edge-width 1 --label-colour "#FFFFFFFF" -f --file-node-colour "#55FF55FF" --file-node-size 5 --label-depth 3
```
<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/twopi.png" width="640" align="middle">

```
./pfsg.py /home/odroid/Code sfdp.png -b "#000000FF" -l sfdp --edge-colour "#222222FF" --edge-width 1 --label-colour "#FFFFFFFF" -f --file-node-colour "#FF5555FF" --file-node-size 25 --label-size 8
```
<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/sfdp.png" width="640" align="middle">


### Prerequisites

hypothetically works on any modern linux distribution
but so far tested only on ubuntu 18.04

mandatory dependencies:

Ubuntu and Debian:
```
sudo apt-get install python3 python3-pip imagemagick feh
sudo pip3 install matplotlib networkx pydot graphviz click
```
Arch:
```
sudo sudo pacman -S python3 python3-pip imagemagick feh python-pygraphviz
sudo pip3 install matplotlib networkx pydot graphviz click
```

### Installing
```
git clone https://github.com/niveknosredneh/PFSG.git
cd PFSG && sudo chmod +x pfsg.py
...
```

### Options
```
  -w, --width INTEGER           Graph width
  -h, --height INTEGER          Graph height
  -l, --layout TEXT             Layout style: dot|twopi|neato|fdp|sfdp|circo
  -i, --image TEXT              Image file for graph to overlay ontop of
  -b, --background-colour TEXT  Background colour in form '#RRGGBBAA'
  -d, --depth INTEGER           Max node depth
  --label-depth INTEGER         Max depth to draw labels
  --label-size INTEGER          Font size for labels
  --label-colour TEXT           Font colour in form '#RRGGBBAA'
  --file-label-size INTEGER     Font size for file labels
  --file-label-colour TEXT      Font colour in form '#RRGGBBAA'
  --edge-width FLOAT            Edge line width
  --edge-colour TEXT            Edge colour in form '#RRGGBBAA'
  --edge-style TEXT             Edge style: solid|dashed|dotted|dashdot
  --node-size INTEGER           Node dot size, set to zero to disable
  --node-colour TEXT            Node colour in form '#RRGGBBAA'
  --file-node-size INTEGER      Node dot size, set to zero to disable
  --file-node-colour TEXT       Node colour in form '#RRGGBBAA'
  -f, --show-files              Shows file nodes
  --show-file-labels            Shows file labels, restricted by label-depth
  -s, --set-wallpaper           Sets output image as wallpaper using feh
  -v, --verbose                 Display more output than necessary
  --help                        Show this message and exit.

```

## Authors

* **Kevin Henderson**

## Contributors

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/niveknosredneh/PFSG/blob/master/LICENSE) file for details
