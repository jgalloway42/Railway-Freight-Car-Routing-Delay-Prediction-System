"""
Simplified Railway Routing - Multi-Commodity Flow
==================================================
Route multiple freight types through a simple 4-node network.

Network topology:
    A → B → D
    ↓   ↓
    C → D

Commodities:
- Coal: 50 units from A to D
- Grain: 40 units from A to D

Each arc has capacity and commodity-specific costs.
"""

from pyomo.environ import *

def solve_railway_routing():
    """Solve simplified multi-commodity railway routing problem."""
    
    model = ConcreteModel(name="SimplifiedRailway")
    
    # Network topology
    nodes = ['A', 'B', 'C', 'D']
    arcs = [('A','B'), ('A','C'), ('B','D'), ('C','D'), ('B','C')]
    commodities = ['Coal', 'Grain']
    
    # Arc data: (capacity, cost_coal, cost_grain)
    arc_data = {
        ('A','B'): (100, 5, 6),
        ('A','C'): (80, 7, 5),
        ('B','D'): (90, 4, 7),
        ('C','D'): (70, 6, 4),
        ('B','C'): (50, 3, 3)
    }
    
    # Demand: (origin, destination, amount)
    demand = {
        'Coal': ('A', 'D', 50),
        'Grain': ('A', 'D', 40)
    }
    
    # Sets
    model.Nodes = Set(initialize=nodes)
    model.Arcs = Set(initialize=arcs)
    model.Commodities = Set(initialize=commodities)
    
    # Parameters
    model.capacity = Param(model.Arcs, initialize={a: arc_data[a][0] for a in arcs})
    
    # Commodity-specific costs
    cost_dict = {}
    for k_idx, k in enumerate(commodities):
        for a in arcs:
            cost_dict[k, a] = arc_data[a][k_idx + 1]
    model.cost = Param(model.Commodities, model.Arcs, initialize=cost_dict)
    
    # Variables: flow[k, i, j] = amount of commodity k on arc (i,j)
    model.flow = Var(model.Commodities, model.Arcs, domain=NonNegativeReals)
    
    # Objective: minimize total transportation cost
    def obj_rule(model):
        return sum(model.cost[k,i,j] * model.flow[k,i,j]
                   for k in model.Commodities for (i,j) in model.Arcs)
    model.obj = Objective(rule=obj_rule, sense=minimize)
    
    # Flow conservation constraints
    def flow_conservation(model, k, node):
        origin, destination, amount = demand[k]
        
        # Inflow: sum of flows coming into this node
        inflow = sum(model.flow[k,i,node] for (i,j) in model.Arcs if j == node)
        # Outflow: sum of flows leaving this node
        outflow = sum(model.flow[k,node,j] for (i,j) in model.Arcs if i == node)
        
        if node == origin:
            return outflow - inflow == amount  # Source node
        elif node == destination:
            return inflow - outflow == amount  # Sink node
        else:
            return inflow == outflow  # Transit node (flow in = flow out)
            
    model.flow_con = Constraint(model.Commodities, model.Nodes, 
                                rule=flow_conservation)
    
    # Capacity constraints: total flow on each arc cannot exceed capacity
    def capacity_constraint(model, i, j):
        return sum(model.flow[k,i,j] for k in model.Commodities) <= model.capacity[i,j]
    model.cap_con = Constraint(model.Arcs, rule=capacity_constraint)
    
    # Display problem setup
    print("=" * 70)
    print("SIMPLIFIED RAILWAY ROUTING - MULTI-COMMODITY FLOW")
    print("=" * 70)
    
    print("\n📊 Network Topology:")
    print("    A → B → D")
    print("    ↓   ↓")
    print("    C → D")
    
    print("\n🚂 Freight Demand:")
    for k in commodities:
        origin, destination, amount = demand[k]
        print(f"  {k:8}: {amount:3} units from {origin} to {destination}")
    
    print("\n🛤️  Arc Data (Capacity, Cost_Coal, Cost_Grain):")
    for arc in arcs:
        cap, c_coal, c_grain = arc_data[arc]
        print(f"  {arc[0]} → {arc[1]}: capacity={cap:3}, coal_cost=${c_coal}, grain_cost=${c_grain}")
    
    # Solve
    print("\n⚙️  Solving optimization problem...")
    solver = SolverFactory('glpk')
    result = solver.solve(model, tee=False)
    
    # Check solver status
    if result.solver.status == SolverStatus.ok and \
       result.solver.termination_condition == TerminationCondition.optimal:
        print("✓ Optimal solution found!\n")
        
        print(f"💰 Optimal Total Cost: ${model.obj():.2f}\n")
        
        # Display routing for each commodity
        for k in model.Commodities:
            print(f"🔹 {k} Routing:")
            total_flow = 0
            for (i,j) in model.Arcs:
                flow_val = model.flow[k,i,j].value
                if flow_val > 0.01:
                    cost = model.cost[k,i,j] * flow_val
                    total_flow += flow_val
                    print(f"    {i} → {j}: {flow_val:5.1f} units " + 
                          f"(unit cost=${model.cost[k,i,j]}, total=${cost:.2f})")
            origin, destination, amount = demand[k]
            print(f"  Total routed: {total_flow:.1f} / {amount} units\n")
        
        # Display arc utilization
        print("📈 Arc Utilization:")
        for (i,j) in model.Arcs:
            total_flow = sum(model.flow[k,i,j].value for k in model.Commodities)
            capacity = model.capacity[i,j]
            utilization = (total_flow / capacity) * 100
            bar_length = int(utilization / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"  {i} → {j}: [{bar}] {total_flow:5.1f}/{capacity:3} ({utilization:5.1f}%)")
        
    else:
        print("✗ Solver failed to find optimal solution")
        print(f"Status: {result.solver.status}")
        print(f"Termination: {result.solver.termination_condition}")
    
    print("\n" + "=" * 70 + "\n")
    
    return model

if __name__ == "__main__":
    model = solve_railway_routing()
