#!/usr/bin/env python2
import os 

def makefnames(dates1, dates2, sensor):
    root = os.path.join(dates1+'_'+dates2)
    iname = os.path.join(root, 'aligned.unw.vrt')
    cname = os.path.join(root, 'aligned.cor.vrt')
    return iname, cname
