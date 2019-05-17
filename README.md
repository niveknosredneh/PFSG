# PFSG - Python Filesystem Grapher

Uses matplotlib and networkx to create graph of given directory structure and exports to png image for use as desktop wallpaper

## Examples

```
./pfsg.py /dev dot.png -w 1920 -h 1080 -b '#333333FF' -l dot --edge-width 3 --edge-colour '#CCCCCCFF' --label-depth 2 --label-size 12 --label-colour '#000000FF'
```
<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/dot.png" width="640" align="middle">

```
./pfsg.py /dev twopi.png -w 1920 -h 1080 -b '#333333FF' -l twopi --edge-width 3 --edge-colour '#CCCCCCFF' --label-depth 2 --label-size 12 --label-colour '#000000FF'
```
<img src="https://github.com/niveknosredneh/PFSG/blob/master/img/twopi.png" width="640" align="middle">

### Prerequisites

hypothetically works on any modern linux distribution
but so far tested only on ubuntu 18.04

mandatory dependencies:
```
sudo apt-get install python3 python3-pip
sudo pip3 install matplotlib networkx pydot graphviz click
```

### Installing
```
git clone https://github.com/niveknosredneh/PFSG.git
...

```

## Authors

* **Kevin Henderson**

## Contributors

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
