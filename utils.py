#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:55:15 2019

@author: smc
"""

"""
Calculates the size of the union of the variables of all the tables in a list
"""

def tam(l):
    tot = set()
    for h in l:
        tot.update(set(h.listavar))
    return len(tot)
    



