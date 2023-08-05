#!/usr/bin/env python

import argparse
from thsquant import config

def sayhello():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="ths", help="input a name")
    args = parser.parse_args()

    print("Hello,,,, {}! Start quant...\nversion={}".format(args.name, config.version))

if __name__ == '__main__':
    sayhello()
