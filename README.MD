
# Running

`/home/daniel/dev/pynaoqi/bin/python2 /home/daniel/dev/drs-naoqi-client/main.py`

# Python Situation

PiNaoQi comes with Python 2.7 executable, configure that as the interpreter in VSCode for this project, otherwise `naoqi` will not be found. It also comes with a `site-packages `folder that includes all the modules available for us, but it lacks `pip`, so we cannot install new ones until we obtain a copy of `pip`. [Python 2.7.15](https://www.linuxfromscratch.org/blfs/view/basic/python2.html) comes with it, so you can just install that, and use `sudo python2.7 -m pip install numpy --target .` to install numpy or anything else in that directory. To install `python2.7.15`, just download the source, then run 

```bash
./configure --prefix=/usr       \
            --enable-shared     \
            --with-system-expat \
            --with-system-ffi   \
            --with-ensurepip=yes \
            --enable-unicode=ucs4 &&
make
```
and then 

```bash
sudo make install &&
chmod -v 755 /usr/lib/libpython2.7.so.1.0
```
