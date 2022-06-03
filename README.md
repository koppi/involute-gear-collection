This collection contains dxf and stl files of involute gears

* [pressure angle 14.5°](angle-14.5):
  ![angle-14.5.png](angle-14.5.png)

  https://github.com/koppi/involute-gear-collection/tree/main/angle-14.5#readme
  
* [pressure angle 20°](angle-20):
  ![angle-20.png](angle-20.png)

  https://github.com/koppi/involute-gear-collection/tree/main/angle-20#readme

## HOWTO create your own involute gear collection

### download and prepare programs and libraries

```bash
$ sudo npm install -g involute-gear-generator
$ sudo apt-get -y install git python-pip
$ git clone https://github.com/koppi/involute-gear-collection
$ pip install ezdxf dxfgrabber
$ sudo apt-get -y install imagemagick openscad
```

Adjust [bin/create-involute-gear-collection.sh](bin/create-involute-gear-collection.sh) and rerun [update.sh](update.sh):

```bash
$ editor bin/create-involute-gear-collection.sh
$ ./update.sh
```

## warning

* this is an early release
* expect errors
* do not use these gears for production

## credits

* Dr. Rainer Hessmer's blog – [Online Involute Spur Gear Builder](http://www.hessmer.org/blog/2014/01/01/online-involute-spur-gear-builder/)

