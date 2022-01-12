# PFSG - Python Filesystem Grapher

Uses matplotlib, networkx and graphviz to create a beautiful graph of directory structure and exports as a png image for use as desktop wallpaper

## Examples

<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/dot.png" width="640" align="middle">

<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/twopi.png" width="640" align="middle">

<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/sfdp.png" width="640" align="middle">

<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/neato.png" width="640" align="middle">

## Prerequisites

Ubuntu and Debian based:
```
# Mandatory dependencies:
sudo apt-get install python3 python3-pip
sudo pip3 install matplotlib networkx pydot graphviz

# Optional dependencies:
sudo apt-get install imagemagick feh
```
(untested) Arch based:
```
# Mandatory dependencies:
sudo pacman -S python3 python3-pip python-pygraphviz
sudo pip3 install matplotlib networkx pydot graphviz

# Optional dependencies:
sudo pacman -S imagemagick feh
```

## Installing
```
wget https://raw.githubusercontent.com/niveknosredneh/PFSG/master/pfsg.py
sudo chmod +x pfsg.py
./pfsg.py
```

## Options

All options have been moved to top of pfsg.py file

<img src="https://matplotlib.org/_images/sphx_glr_colormap_reference_003.png" width="640" align="middle">

See [https://matplotlib.org](https://matplotlib.org/gallery/color/colormap_reference.html) for full colourmap reference

## Authors

* **Kevin Matthew Henderson**

## Contributors

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/niveknosredneh/PFSG/blob/master/LICENSE) file for details
