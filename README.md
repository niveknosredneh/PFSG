# PFSG - Python Filesystem Grapher

Uses matplotlib and networkx to create graph of given directory structure and exports to png image for use as desktop wallpaper

## Examples

```
./pfsg.py /dev/disk dot.png --image /home/odroid/opportunity.png -l dot --file-node-colour "#AA2222FF" --show-files --file-node-size 145 --label-size 12 --label-colour "#CCCCCCFF" --edge-colour "#666666FF" --edge-width 5

```
<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/dot.png" width="640" align="middle">

```
./pfsg.py /dev twopi.png --image /home/odroid/eclipse.jpg -l twopi
```
<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/twopi.png" width="640" align="middle">

```
./pfsg.py /dev/disk sfdp.png --image /home/odroid/Grey-Wall.png -l sfdp --label-depth 12 --file-node-colour "#AA2222FF" --show-files --file-node-size 0 --show-file-labels --label-size 24 --file-label-size 14 --file-label-colour "#FF2222FF" --label-colour "#AA2222FF" --edge-colour "#662222FF" --edge-width 2
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

## Options
```
  -w, --width INTEGER            Graph width
  -h, --height INTEGER           Graph height
  --image TEXT                   Image file for graph to overlay ontop of
  -b, --background-colour TEXT   Background colour in form '#RRGGBBAA'
  -f, --label-size INTEGER       Font size for labels
  --label-colour TEXT            Font colour in form '#RRGGBBAA'
  --label-depth INTEGER          Max depth to draw labels
  -f, --file-label-size INTEGER  Font size for file labels
  --file-label-colour TEXT       Font colour in form '#RRGGBBAA'
  --edge-width FLOAT             Edge line width
  --edge-colour TEXT             Edge colour in form '#RRGGBBAA'
  --node-size INTEGER            Node dot size, set to zero to disable
  --file-node-size INTEGER       Node dot size, set to zero to disable
  --node-colour TEXT             Node colour in form '#RRGGBBAA'
  --file-node-colour TEXT        Node colour in form '#RRGGBBAA'
  --show-files                   Shows files
  --show-file-labels             Shows file labels
  -l, --layout TEXT              Layout style: ‘dot’, ‘twopi’, ‘fdp’, ‘sfdp’,
                                 ‘circo’
  --set-wallpaper                Sets output image as wallpaper using feh
  -v, --verbose                  Display more output than necessary
  --help                         Show this message and exit.


```

## Authors

* **Kevin Henderson**

## Contributors

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/niveknosredneh/PFSG/blob/master/LICENSE) file for details
