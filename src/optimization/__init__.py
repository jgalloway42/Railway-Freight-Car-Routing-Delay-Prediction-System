"""
Railway freight car routing optimization module.

This package contains optimization models for railway routing using mixed-integer
linear programming (MILP) with Pyomo and GLPK solver.

Modules:
    assignment_example: Simple assignment problem demonstration (worker-task matching)
    railway_routing_simple: Multi-commodity flow example on 4-node railway network
    dataset_preparation: Utilities for generating synthetic and real railway datasets

For theoretical background and implementation details, see:
    docs/railway-optimization.md

Example usage:
    >>> from optimization import assignment_example
    >>> # Run the assignment problem example
    >>> assignment_example.solve_assignment_problem()
"""

__version__ = "0.1.0"
__author__ = "Railway Optimization Team"

# Module-level constants
SUPPORTED_SOLVERS = ["glpk", "cbc", "gurobi", "cplex"]
DEFAULT_SOLVER = "glpk"
