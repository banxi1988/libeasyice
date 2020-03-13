#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/Workspace/libeasyice/sdk/lib
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:~/.pyenv/versions/3.7.4/lib/pkgconfig
rm -rf build
python3 setup.py build
cp build/lib.linux-x86_64-3.7/_easyice.cpython-37m-x86_64-linux-gnu.so .