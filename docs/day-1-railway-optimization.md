# Railway Optimization: Discrete Optimization Fundamentals

> **About This Guide:** This document provides the theoretical foundation and practical implementation guide for the railway freight car routing optimization system. It covers MILP formulation, network flow problems, multi-commodity flows, and Pyomo implementation with working code examples.

## 🎯 Learning Objectives

1. Understand MILP (Mixed Integer Linear Programming) formulation
2. Master network flow problems and their properties
3. Implement basic optimization models in Pyomo
4. Prepare datasets for railway routing applications

---

## 📘 Part 1: Core Concepts from Network Optimization

### 1.1 Mixed Integer Linear Programming (MILP)

**Canonical Form:**
```
maximize c^T x + d^T y
subject to:
    Ax + By ≤ b
    x ∈ Z^n    (integer variables)
    y ≥ 0      (continuous variables)
```

**Key Components:**
- **Decision Variables:** x (integer), y (continuous)
- **Objective Function:** Linear combination of variables to optimize
- **Constraints:** Linear inequalities defining feasible region
- **Coefficient Matrices:** A, B define constraint structure

**Why MILP for Railway Routing?**
- Binary variables model discrete decisions (route selection, timing)
- Continuous variables handle flows (freight volume)
- Linear constraints efficiently model network topology
- Proven solvers (GLPK, CBC, Gurobi) scale well

### 1.2 Network Flow Problems

**Network Components:**
- **Nodes (N):** Rail yards, stations, terminals
- **Arcs (A):** Railway connections with capacity
- **Flow (x_ij):** Freight moving from node i to node j
- **Capacity (u_ij):** Maximum flow on arc (i,j)
- **Cost (c_ij):** Per-unit cost on arc (i,j)

**Flow Conservation:**
For each node i:
```
∑_{j: (i,j)∈A} x_ij - ∑_{j: (j,i)∈A} x_ji = b_i
```
where b_i is the supply (+) or demand (-) at node i.

**Minimum Cost Flow Problem:**
```
minimize  ∑_{(i,j)∈A} c_ij * x_ij
subject to:
    Flow conservation at each node
    0 ≤ x_ij ≤ u_ij  (capacity constraints)
```

**Total Unimodularity:**
- Network flow constraint matrices are totally unimodular
- **Key Property:** If supplies are integers, optimal flows are integers
- **Implication:** No need for explicit integer constraints on flow variables!
- This makes network flow problems computationally efficient

### 1.3 Multi-Commodity Flow

Railway networks must route MULTIPLE commodities (freight types) simultaneously:

**Variables:** x_ij^k = flow of commodity k on arc (i,j)

**Formulation:**
```
minimize  ∑_k ∑_{(i,j)} c_ij^k * x_ij^k

subject to:
    # Flow conservation per commodity
    ∑_j x_ij^k - ∑_j x_ji^k = b_i^k,  ∀i, k
    
    # Shared arc capacity
    ∑_k x_ij^k ≤ u_ij,  ∀(i,j)
    
    x_ij^k ≥ 0
```

**Railway Application:**
- k = different freight types (coal, grain, containers)
- Each commodity has origin-destination pairs
- Arcs have shared capacity limits
- Different commodities may have different priorities/costs

### 1.4 Time-Expanded Networks

For routing WITH TIMING (arrival windows, scheduling):

**Concept:** Create a node for each (location, time) pair
- Node (i, t) represents being at location i at time t
- Arc (i,t) → (j,t+τ) represents traveling from i to j taking τ time
- Arc (i,t) → (i,t+1) represents waiting at location i

**Advantages:**
- Naturally handles time windows
- Models waiting vs. moving decisions
- Can incorporate time-dependent costs

---

## 📙 Part 2: State-Task Networks (STN)

From the MILP Scheduling paper, STN provides a framework for resource scheduling:

**STN Components:**
- **States:** Queued freight, available cars, delivered goods
- **Tasks:** Transportation operations, loading, unloading
- **Resources:** Rail cars, track segments, yards

**Binary Decision Variables:**
```python
x_{p,c,t} ∈ {0,1}  # 1 if project p uses chamber c at time t
```

**Complexity:** O(|Projects| × |Time Periods| × |Resources|)

**Railway Adaptation:**
- States: Cars at yards, freight waiting, cars in transit
- Tasks: Route assignments, departures
- Resources: Track capacity, yard space

---

## 🔧 Part 3: Pyomo Implementation

### 3.1 Installation

```bash
pip install pyomo --break-system-packages
# Install solver
sudo apt-get install glpk-utils  # or use conda
```

### 3.2 Basic Pyomo Structure

```python
from pyomo.environ import *

# Create model
model = ConcreteModel(name="MyModel")

# Define sets
model.Nodes = Set(initialize=['A', 'B', 'C'])
model.Arcs = Set(initialize=[('A','B'), ('B','C'), ('A','C')])

# Define parameters
costs = {('A','B'): 10, ('B','C'): 15, ('A','C'): 30}
model.cost = Param(model.Arcs, initialize=costs)

# Define variables
model.x = Var(model.Arcs, domain=Binary)

# Define objective
def obj_rule(model):
    return sum(model.cost[i,j] * model.x[i,j] for (i,j) in model.Arcs)
model.obj = Objective(rule=obj_rule, sense=minimize)

# Define constraints
def flow_conservation(model, node):
    inflow = sum(model.x[i,node] for (i,j) in model.Arcs if j==node)
    outflow = sum(model.x[node,j] for (i,j) in model.Arcs if i==node)
    return inflow == outflow  # for transit nodes
model.flow_con = Constraint(model.Nodes, rule=flow_conservation)

# Solve
solver = SolverFactory('glpk')
result = solver.solve(model)

# Extract solution
for arc in model.Arcs:
    print(f"Arc {arc}: {model.x[arc].value}")
```

### 3.3 Key Pyomo Concepts

**Concrete vs Abstract Models:**
- **ConcreteModel:** Data provided upfront (easier for Python programmers)
- **AbstractModel:** Data loaded separately (traditional AML style)

**Indexed Components:**
```python
# Indexed variables
model.x = Var(model.Nodes, model.Time, bounds=(0,100))
# Access: model.x['A', 5].value

# Indexed constraints
def capacity_rule(model, i, j):
    return model.flow[i,j] <= model.capacity[i,j]
model.cap_con = Constraint(model.Arcs, rule=capacity_rule)
```

**Construction Rules:**
- Used to define constraints and objectives systematically
- Accept model and index parameters
- Return expressions or constraints

---

## 🎮 Part 4: Hands-On Examples

### Example 1: Simple Assignment Problem

**Problem:** Assign 3 workers to 3 tasks, minimize total cost.

```python
from pyomo.environ import *

model = ConcreteModel()

# Data
workers = ['Alice', 'Bob', 'Carol']
tasks = ['Task1', 'Task2', 'Task3']
cost = {
    ('Alice', 'Task1'): 10, ('Alice', 'Task2'): 15, ('Alice', 'Task3'): 12,
    ('Bob', 'Task1'): 14, ('Bob', 'Task2'): 11, ('Bob', 'Task3'): 13,
    ('Carol', 'Task1'): 12, ('Carol', 'Task2'): 13, ('Carol', 'Task3'): 10
}

model.Workers = Set(initialize=workers)
model.Tasks = Set(initialize=tasks)
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
solver = SolverFactory('glpk')
result = solver.solve(model)

# Display results
print(f"Total Cost: {model.obj()}")
for w in model.Workers:
    for t in model.Tasks:
        if model.x[w,t].value > 0.5:
            print(f"{w} → {t} (cost: {model.cost[w,t]})")
```

### Example 2: Simplified Railway Routing

**Problem:** Route 2 freight types through 4-node network.

```python
from pyomo.environ import *

model = ConcreteModel(name="SimplifiedRailway")

# Network: 4 yards forming a simple network
# A → B → D
# ↓   ↓
# C → D

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

# Demand: commodity k needs to go from origin to destination
demand = {
    'Coal': ('A', 'D', 50),   # 50 units from A to D
    'Grain': ('A', 'D', 40)   # 40 units from A to D
}

model.Nodes = Set(initialize=nodes)
model.Arcs = Set(initialize=arcs)
model.Commodities = Set(initialize=commodities)

# Parameters
model.capacity = Param(model.Arcs, initialize={a: arc_data[a][0] for a in arcs})
model.cost = Param(model.Commodities, model.Arcs, 
                   initialize={
                       ('Coal', a): arc_data[a][1] for a in arcs
                   } | {
                       ('Grain', a): arc_data[a][2] for a in arcs
                   })

# Variables: flow[k, i, j] = amount of commodity k on arc (i,j)
model.flow = Var(model.Commodities, model.Arcs, domain=NonNegativeReals)

# Objective: minimize total cost
def obj_rule(model):
    return sum(model.cost[k,i,j] * model.flow[k,i,j]
               for k in model.Commodities for (i,j) in model.Arcs)
model.obj = Objective(rule=obj_rule, sense=minimize)

# Flow conservation constraints
def flow_conservation(model, k, node):
    origin, destination, amount = demand[k]
    
    inflow = sum(model.flow[k,i,node] for (i,j) in model.Arcs if j == node)
    outflow = sum(model.flow[k,node,j] for (i,j) in model.Arcs if i == node)
    
    if node == origin:
        return outflow - inflow == amount  # Source
    elif node == destination:
        return inflow - outflow == amount  # Sink
    else:
        return inflow == outflow  # Transit
        
model.flow_con = Constraint(model.Commodities, model.Nodes, 
                            rule=flow_conservation)

# Capacity constraints: total flow on each arc
def capacity_constraint(model, i, j):
    return sum(model.flow[k,i,j] for k in model.Commodities) <= model.capacity[i,j]
model.cap_con = Constraint(model.Arcs, rule=capacity_constraint)

# Solve
solver = SolverFactory('glpk')
result = solver.solve(model, tee=True)

# Display results
print(f"\nOptimal Total Cost: {model.obj():.2f}\n")
for k in model.Commodities:
    print(f"\n{k} Routing:")
    for (i,j) in model.Arcs:
        flow_val = model.flow[k,i,j].value
        if flow_val > 0.01:
            print(f"  {i} → {j}: {flow_val:.1f} units (cost: {model.cost[k,i,j]})")
```

---

## 📊 Part 5: Railway Datasets

### 5.1 Recommended Public Datasets

**1. OpenStreetMap Railway Data**
- Source: https://overpass-turbo.eu/
- Query for US rail network: `railway=rail`
- Provides: Node locations, track connections, station names
- Format: GeoJSON, can convert to networkx graph

**2. Bureau of Transportation Statistics**
- Source: https://www.bts.gov/freight
- Data: Freight flows between states, commodity types
- Useful for demand estimation

**3. Alternative: Synthetic Data**
For learning purposes, generate realistic scenarios:
```python
import networkx as nx
import random

# Create random rail network
G = nx.gnm_random_graph(n=20, m=40, directed=True)
# Assign random capacities and costs
for (u, v) in G.edges():
    G[u][v]['capacity'] = random.randint(50, 150)
    G[u][v]['cost'] = random.randint(5, 20)
```

### 5.2 Dataset Preparation Checklist

- [ ] Network topology (nodes, edges, capacities)
- [ ] Freight demand (origin, destination, volume, type)
- [ ] Historical delay data (for ML component tomorrow)
- [ ] Geospatial coordinates (for visualization)
- [ ] Time-dependent factors (peak hours, maintenance windows)

---

## ✅ Day 1 Deliverables Checklist

- [ ] GitHub repository structure created
- [ ] Pyomo installed and tested with simple example
- [ ] Assignment problem implemented and solved
- [ ] Simplified railway routing example working
- [ ] Dataset identified and downloaded/generated
- [ ] Understanding of MILP formulation documented
- [ ] Key concepts from Network Optimization book extracted
- [ ] Ready to build full routing model tomorrow

---

## 🔜 Preview: Day 2 Goals

Tomorrow you'll build the complete railway network optimization model:
1. Design full network graph from dataset
2. Implement multi-commodity flow with time windows
3. Add realistic constraints (priority, capacity, timing)
4. Create test scenarios with increasing complexity
5. Benchmark solver performance

---

## 📚 Key Takeaways

1. **MILP is perfect for railway routing:** Handles discrete decisions and continuous flows
2. **Network flows have nice properties:** Total unimodularity gives integer solutions naturally
3. **Pyomo structure:** ConcreteModel → Sets → Parameters → Variables → Objective → Constraints → Solve
4. **Multi-commodity flows:** Essential for real-world routing with multiple freight types
5. **Time expansion:** Crucial for scheduling and time-window constraints

## 💡 Interview Talking Points

- "I chose MILP because railway routing inherently involves discrete decisions—which routes to activate, when to dispatch—combined with continuous flow variables."
- "Network flow problems have the total unimodularity property, which guarantees integer solutions for integer supplies without explicit integer constraints, making them computationally efficient."
- "I implemented multi-commodity flows because railways must route multiple freight types simultaneously through shared infrastructure."
- "My optimization engine uses Pyomo because it provides algebraic modeling abstraction, supports multiple solvers, and integrates seamlessly with Python's ML ecosystem."
