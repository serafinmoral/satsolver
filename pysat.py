#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:16:54 2020

@author: smc
"""

from pysat.solvers import Glucose3
g = Glucose3()
g.add_clause([-2, 3])