#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:16:54 2020

@author: smc
"""
import sys
sys.path.append('/home/smc/programas/PyMiniSolvers-master')


import minisolvers
import unittest


class MinisatTest(unittest.TestCase):
    def setUp(self):
        self.solver = minisolvers.MinisatSolver()
        self.clauses = [ [1], [-2], [3, 4], [-3, 5], [-4, 6], [-5, 4], [-6] ]
        self.numvars = max([max(cl) for cl in [[abs(x) for x in cl] for cl in self.clauses]])

    def tearDown(self):
        del self.solver

    def test_newvars(self):
        for i in range(self.numvars):
            self.solver.new_var(True)
            self.assertEqual(self.solver.nvars(), i+1)

    def test_add_clause_without_vars(self):
        self.assertRaises(Exception, self.solver.add_clause, [-1, 2])

    def add_subset(self, subset):
        for i in range(self.numvars):
            self.solver.new_var()
        for cl in subset:
            self.solver.add_clause(cl)

    def test_sat(self):
        self.add_subset(self.clauses[:-1])
        self.assertEqual(self.solver.solve(), True)

    def test_unsat(self):
        self.add_subset(self.clauses)
        self.assertEqual(self.solver.solve(), False)

    def test_assumptions(self):
        self.add_subset(self.clauses[:-2])
        self.assertEqual(self.solver.solve([-5]), True)
        self.assertEqual(self.solver.solve([-6]), True)
        self.assertEqual(self.solver.solve([-5, -6]), False)

    def test_model(self):
        from math import copysign
        isPositive = lambda x: copysign(1, x) > 0
        subset = self.clauses[:-1]
        self.add_subset(subset)
        self.solver.solve()
        m = self.solver.get_model()
        self.assertEqual(len(m), self.solver.nvars())
        for cl in subset:
            self.assertTrue(any([ m[abs(x)-1] == isPositive(x) for x in cl ]))

    def test_implies(self):
        self.add_subset(self.clauses[:-1])
        implications = self.solver.implies()
        self.assertEqual(set(implications), set([1,-2]))

    def test_implies_assumptions(self):
        self.add_subset(self.clauses[:-1])
        implications = self.solver.implies([5])
        self.assertEqual(set(implications), set([1,-2,5,4,6]))

if __name__ == '__main__':
    unittest.main()
