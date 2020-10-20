#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:16:54 2020

@author: smc
"""
from pysat.formula import CNFPlus
from pysat.solvers import Solvers,SolversNames
g = Glucose3()
g.add_clause([-2, 3])