#!/usr/bin/env python3

from Gaugi import LoggingLevel, Logger
from Gaugi import expand_folders, save, load, progressbar
from Gaugi.macros import *
from kepler.dumper import MergeNpz
from pprint import pprint

import numpy as np
import argparse
import sys,os


parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-f', '--files', action='store',  dest='files', required = True, 
    help = "Files to be merged.", nargs='+',)

parser.add_argument('-o', '--output', action='store',  dest='output', required = True,
    help = "The output merged file.")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()
merge_these_keys = ["data_float","data_bool","data_int", "target"]
merger = MergeNpz( merge_these_keys )
merger.run(args.files, args.output)
