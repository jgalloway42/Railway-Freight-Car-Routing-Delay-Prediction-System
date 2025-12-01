"""
Assignment Problem Example
===========================
Assign workers to tasks to minimize total cost.
Each worker gets exactly one task, each task gets exactly one worker.
"""

from pyomo.environ import *

def solve_assignment_problem():
    """Solve a simple 3x3 assignment problem."""
    
    model = ConcreteModel(name="WorkerAssignment")
    
    # Data
    workers = ['Alice', 'Bob', 'Carol']
    tasks = ['Task1', 'Task2', 'Task3']
    cost = {
        ('Alice', 'Task1'): 10, ('Alice', 'Task2'): 15, ('Alice', 'Task3'): 12,
        ('Bob', 'Task1'): 14, ('Bob', 'Task2'): 11, ('Bob', 'Task3'): 13,
        ('Carol', 'Task1'): 12, ('Carol', 'Task2'): 13, ('Carol', 'Task3'): 10
    }
    
    # Sets
    model.Workers = Set(initialize=workers)
    model.Tasks = Set(initialize=tasks)
    
    # Parameters
    model.cost = Param(model.Workers, model.Tasks, initialize=cost)
    
    # Variables: x[w,t] = 1 if worker w assigned to task t
    model.x = Var(model.Workers, model.Tasks, domain=Binary)
    
    # Objective: minimize total cost
    def obj_rule(model):
        return sum(model.cost[w,t] * model.x[w,t] 
                   for w in model.Workers for t in model.Tasks)
    model.obj = Objective(rule=obj_rule, sense=minimize)
    
    # Constraint: each worker assigned to exactly one task
    def worker_constraint(model, w):
        return sum(model.x[w,t] for t in model.Tasks) == 1
    model.worker_con = Constraint(model.Workers, rule=worker_constraint)
    
    # Constraint: each task assigned to exactly one worker
    def task_constraint(model, t):
        return sum(model.x[w,t] for w in model.Workers) == 1
    model.task_con = Constraint(model.Tasks, rule=task_constraint)
    
    # Solve
    print("=" * 60)
    print("ASSIGNMENT PROBLEM")
    print("=" * 60)
    print("\nCost Matrix:")
    print(f"{'':8}", end="")
    for t in tasks:
        print(f"{t:>8}", end="")
    print()
    for w in workers:
        print(f"{w:8}", end="")
        for t in tasks:
            print(f"{cost[w,t]:8}", end="")
        print()
    
    solver = SolverFactory('glpk')
    result = solver.solve(model, tee=False)
    
    # Check solver status
    if result.solver.status == SolverStatus.ok and \
       result.solver.termination_condition == TerminationCondition.optimal:
        print("\n✓ Optimal solution found!\n")
        print(f"Minimum Total Cost: ${model.obj():.2f}\n")
        print("Optimal Assignments:")
        for w in model.Workers:
            for t in model.Tasks:
                if model.x[w,t].value > 0.5:
                    print(f"  {w:8} → {t:8} (cost: ${model.cost[w,t]:3})")
    else:
        print("\n✗ Solver failed to find optimal solution")
        print(f"Status: {result.solver.status}")
        print(f"Termination: {result.solver.termination_condition}")
    
    print("\n" + "=" * 60 + "\n")
    
    return model

if __name__ == "__main__":
    model = solve_assignment_problem()
