# 🚂 Day 2 Progress Report: MILP-Based Routing Optimization Engine

**Date:** December 3, 2025  
**Focus:** Railway network modeling and multi-commodity flow optimization  
**Status:** 🟢 In Progress  
**Project:** Railway Freight Car Routing & Delay Prediction System

---

## 📋 Day 2 Objectives & Status

### Morning Session: Railway Network Model Design ✅
- [x] Design railway network model (nodes = yards, edges = routes)
- [x] Understand multi-commodity flow problem structure
- [x] Define decision variables and parameters
- [x] Formulate mathematical model for MILP

### Afternoon Session: Implementation & Testing 🔄
- [ ] Implement Pyomo model with GLPK solver
- [ ] Create flow conservation constraints
- [ ] Add edge capacity constraints
- [ ] Implement objective function (cost minimization)
- [ ] Build 3-5 test scenarios (increasing complexity)
- [ ] Benchmark performance metrics

---

## 🏗️ Network Design Specifications

### Network Topology Overview
```
Network Size:
├── Nodes (Rail Yards): 20 (Yard_AA through Yard_AT)
├── Edges (Rail Routes): 50 directed connections
├── Commodities: 4 types (Coal, Grain, Containers, Chemicals)
└── Demands: 30 freight shipments
```

### Node Attributes (Rail Yards)
Each rail yard has the following properties:

| Property | Range/Type | Description |
|----------|-----------|-------------|
| Yard ID | Yard_AA - Yard_AT | Unique identifier |
| Latitude | Float | Geographic coordinate |
| Longitude | Float | Geographic coordinate |
| Storage Capacity | 50-200 units | Maximum simultaneous storage |
| Operational Status | Active | Currently operational |

### Edge Attributes (Rail Connections)
Each directed rail connection has:

| Property | Range | Description |
|----------|-------|-------------|
| Capacity | 50-150 units | Maximum simultaneous freight volume |
| Distance | 100-500 miles | Physical route length |
| Base Cost | $5-25 per unit | Transportation cost baseline |
| Transit Time | Calculated | Based on distance and speed |

**Commodity-Specific Cost Multipliers:**
- **Coal:** 1.0x (baseline commodity)
- **Grain:** 1.2x (requires covered cars)
- **Containers:** 1.5x (intermodal handling)
- **Chemicals:** 2.0x (hazmat regulations)

### Demand Specifications
Each freight shipment demand includes:

| Property | Range/Options | Description |
|----------|---------------|-------------|
| Origin Yard | Random from network | Starting location |
| Destination Yard | Random (≠ origin) | Delivery location |
| Quantity | 20-100 units | Freight volume |
| Commodity Type | {Coal, Grain, Containers, Chemicals} | Freight category |
| Priority | {High, Medium, Low} | Delivery urgency |
| Deadline | 12-72 hours | Maximum delivery time |

**Priority Weight Mapping:**
- High Priority: 1.0 (must satisfy)
- Medium Priority: 0.7 (important but flexible)
- Low Priority: 0.5 (best effort)

---

## 📐 Mathematical Formulation

### MILP Formulation for Static Multi-Commodity Flow

**Phase 1 Approach:** Static routing without time windows (simplified initial version)

#### Sets and Indices
- **N**: Set of rail yards (nodes) = {Yard_AA, ..., Yard_AT}
- **A**: Set of directed edges (rail connections) ⊆ N × N
- **K**: Set of commodities = {Coal, Grain, Containers, Chemicals}
- **D**: Set of freight demands = {0, 1, ..., 29}

#### Parameters

**Network Parameters:**
- `c_ij^k`: Cost per unit of commodity k on edge (i,j) = base_cost × commodity_multiplier
- `u_ij`: Capacity of edge (i,j) in units
- `d_ij`: Distance of edge (i,j) in miles
- `cap_i`: Storage capacity of yard i (optional for Phase 1)

**Demand Parameters:**
- `o_d`: Origin yard for demand d
- `dest_d`: Destination yard for demand d
- `q_d`: Quantity demanded (units)
- `k_d`: Commodity type for demand d
- `w_d`: Priority weight for demand d

**Cost Structure:**
```
Total edge cost = base_cost × commodity_multiplier × quantity
Example: 
  - Coal on $10 base cost edge: $10 × 1.0 = $10/unit
  - Chemicals on same edge: $10 × 2.0 = $20/unit
```

#### Decision Variables

**Primary Variables:**
- `y_ijd ≥ 0`: Continuous variable = amount of demand d flowing on edge (i,j)
- `z_d ∈ {0,1}`: Binary variable = 1 if demand d is satisfied, 0 otherwise

**Variable Interpretation:**
```python
# Example:
y[('Yard_AA', 'Yard_AB', 5)] = 45.0  # 45 units of demand 5 flows from AA to AB
z[5] = 1                              # Demand 5 is satisfied
```

#### Objective Function

**Minimize:** Total transportation cost + penalties for unmet demands

```
minimize: Σ_{(i,j)∈A} Σ_{d∈D} c_ij^{k_d} × y_ijd + M × Σ_{d∈D} w_d(1 - z_d)
```

Where:
- First term: Total routing cost across all edges and demands
- Second term: Penalty for unmet demands (M = large constant, e.g., 10,000)
- `w_d`: Priority weight (high priority demands have higher penalty)

#### Constraints

**1. Flow Conservation (at each node for each demand)**

For demand d at **origin node** `o_d`:
```
Σ_{j:(o_d,j)∈A} y_{o_d,j,d} - Σ_{j:(j,o_d)∈A} y_{j,o_d,d} = q_d × z_d
```
(Net outflow from origin = demand quantity if satisfied)

For demand d at **destination node** `dest_d`:
```
Σ_{j:(j,dest_d)∈A} y_{j,dest_d,d} - Σ_{j:(dest_d,j)∈A} y_{dest_d,j,d} = q_d × z_d
```
(Net inflow to destination = demand quantity if satisfied)

For demand d at **intermediate node** i (neither origin nor destination):
```
Σ_{j:(j,i)∈A} y_{j,i,d} - Σ_{j:(i,j)∈A} y_{i,j,d} = 0
```
(Flow in = flow out; conservation at intermediate nodes)

**2. Edge Capacity Constraints**
```
Σ_{d∈D} y_{ijd} ≤ u_ij    ∀(i,j) ∈ A
```
(Total flow on each edge cannot exceed its capacity)

**3. Flow-Satisfaction Coupling**
```
Σ_{(i,j)∈A} y_{ijd} ≤ q_d × z_d    ∀d ∈ D
```
(Flow for demand d can only occur if demand is satisfied)

**4. Non-negativity**
```
y_{ijd} ≥ 0    ∀(i,j) ∈ A, d ∈ D
z_d ∈ {0,1}    ∀d ∈ D
```

---

## 🔧 Implementation Architecture

### Solver Stack
```
Technology Stack:
├── Pyomo 6.7.0+ (MILP modeling framework)
├── GLPK (GNU Linear Programming Kit) ✅ INSTALLED
├── NetworkX (graph data structure)
└── Python 3.9+
```

**Why GLPK?**
- Open-source (no licensing issues)
- Handles MILP problems efficiently
- Good performance for medium-scale problems (20 nodes, 50 edges)
- Easy installation: `sudo apt-get install glpk-utils`

### File Structure
```
railway-optimization/
├── data/
│   ├── raw/
│   │   ├── network_graph.pkl          # NetworkX graph object
│   │   └── demands.json                # Freight demand records
│   └── processed/
│       └── (solver results will go here)
├── src/
│   ├── optimization/
│   │   ├── __init__.py
│   │   ├── network_builder.py          # Network construction
│   │   ├── milp_model.py               # Pyomo model definition
│   │   └── solver.py                   # Solver interface
│   └── utils/
│       └── visualization.py            # Network plotting
├── tests/
│   ├── test_scenario_1_simple.py       # 2 nodes, 1 demand
│   ├── test_scenario_2_multihop.py     # 5 nodes, 1 demand
│   ├── test_scenario_3_multiple.py     # 10 nodes, 5 demands
│   ├── test_scenario_4_capacity.py     # Capacity conflicts
│   └── test_scenario_5_full.py         # All 30 demands
├── notebooks/
│   └── Day2_MILP_Development.ipynb     # Interactive development
└── reports/
    └── figures/
        └── network_visualization.png    # Network topology map
```

---

## 🎯 Test Scenarios (Incremental Complexity)

### Test Scenario 1: Single Direct Route ✅ PLANNED
**Purpose:** Validate basic model setup and solver integration

```python
Test Configuration:
├── Nodes: 2 (Yard_AA → Yard_AB)
├── Edges: 1 direct connection
├── Demands: 1 shipment
├── Commodity: Coal (50 units)
└── Expected: Direct routing with cost = 50 × edge_cost

Success Criteria:
✓ Model builds without errors
✓ Solver finds feasible solution
✓ Flow conservation satisfied
✓ z_d = 1 (demand satisfied)
```

### Test Scenario 2: Multi-Hop Routing 🔄 PLANNED
**Purpose:** Test path-finding across multiple edges

```python
Test Configuration:
├── Nodes: 5 (Yard_AA → Yard_AE)
├── Edges: 6 connections (multiple paths available)
├── Demands: 1 shipment
├── Commodity: Containers (40 units)
└── Expected: Shortest cost path found

Success Criteria:
✓ Flow follows physically connected path
✓ No "teleportation" (flow on non-existent edges)
✓ Intermediate nodes satisfy flow conservation
✓ Solution cost ≤ manual calculation
```

### Test Scenario 3: Multiple Non-Competing Demands ⏳ PLANNED
**Purpose:** Test simultaneous routing without capacity conflicts

```python
Test Configuration:
├── Nodes: 10 yards
├── Edges: 20 connections
├── Demands: 5 shipments (different routes)
├── Commodities: Mix of all 4 types
└── Expected: All demands satisfied, no edge conflicts

Success Criteria:
✓ All 5 demands satisfied (z_d = 1 for d=0..4)
✓ No edge exceeds capacity
✓ Total cost = sum of individual optimal routes
✓ Solve time < 5 seconds
```

### Test Scenario 4: Capacity Conflicts ⏳ PLANNED
**Purpose:** Test capacity constraint enforcement and demand prioritization

```python
Test Configuration:
├── Nodes: 10 yards
├── Edges: 15 connections (including bottleneck edges)
├── Demands: 8 shipments competing for same route
├── Commodities: Mix with varying priorities
└── Expected: High priority demands satisfied first

Success Criteria:
✓ Edge capacity never exceeded
✓ High priority demands satisfied over low priority
✓ Some demands may be unsatisfied (z_d = 0)
✓ Penalty costs applied correctly
```

### Test Scenario 5: Full Network Stress Test ⏳ PLANNED
**Purpose:** Benchmark performance on realistic scale

```python
Test Configuration:
├── Nodes: 20 yards (full network)
├── Edges: 50 connections (full topology)
├── Demands: 30 shipments (all demands)
├── Commodities: All 4 types with realistic distribution
└── Expected: Near-optimal solution in reasonable time

Success Criteria:
✓ Solver completes within 60 seconds
✓ At least 80% of demands satisfied
✓ Capacity constraints respected
✓ Solution cost documented for baseline
```

---

## 📊 Performance Benchmarking Plan

### Metrics to Track

**Solution Quality Metrics:**
1. **Satisfaction Rate:** % of demands successfully routed
   - Target: ≥80% for full network scenario
2. **Total Cost:** Sum of routing costs + penalties
   - Compare against greedy baseline (shortest path per demand)
3. **Capacity Utilization:** % of edge capacity used
   - Identify bottleneck edges
4. **Priority Satisfaction:** % of high/medium/low priority demands met
   - High priority should be ≥90%

**Computational Performance Metrics:**
1. **Solve Time:** Wall clock time to optimal/feasible solution
   - Target: <60 seconds for full network
2. **Number of Variables:** Scale with network size
3. **Number of Constraints:** Track formulation complexity
4. **Optimality Gap:** MIP gap at termination (if time-limited)
   - Target: <5% gap acceptable

### Comparison Baselines

**Baseline 1: Greedy Shortest Path**
- Route each demand independently on shortest cost path
- Ignore capacity constraints initially
- Check how many demands violate capacity

**Baseline 2: First-Come-First-Served**
- Route demands in order of priority
- Stop when capacity exhausted
- Simple but suboptimal

**Expected Improvement:**
- MILP should achieve 15-30% cost reduction vs greedy
- Higher satisfaction rate for low priority demands

---

## 🔍 Implementation Checklist

### Phase 1: Core Model (Today's Focus)
- [ ] Load network graph from `network_graph.pkl`
- [ ] Load demands from `demands.json`
- [ ] Extract edge attributes (capacity, cost, distance)
- [ ] Define Pyomo ConcreteModel
- [ ] Define sets (nodes, edges, demands)
- [ ] Define parameters (costs, capacities, demand quantities)
- [ ] Define decision variables (flow, satisfied)
- [ ] Implement objective function
- [ ] Implement flow conservation constraints
- [ ] Implement edge capacity constraints
- [ ] Implement flow-satisfaction coupling
- [ ] Configure GLPK solver
- [ ] Test on Scenario 1

### Phase 2: Testing & Validation
- [ ] Run Test Scenario 1 (single direct route)
- [ ] Run Test Scenario 2 (multi-hop routing)
- [ ] Run Test Scenario 3 (multiple demands)
- [ ] Validate flow conservation manually for one demand
- [ ] Check edge capacity never exceeded
- [ ] Verify objective value calculation

### Phase 3: Full Network & Benchmarking
- [ ] Run Test Scenario 4 (capacity conflicts)
- [ ] Run Test Scenario 5 (full network)
- [ ] Implement greedy baseline solver
- [ ] Compare MILP vs baseline results
- [ ] Document performance metrics
- [ ] Create performance visualization plots

### Phase 4: Documentation & Git
- [ ] Comment code thoroughly
- [ ] Write docstrings for all functions
- [ ] Create README for optimization module
- [ ] Commit working code to GitHub
- [ ] Update main project README

---

## 🐛 Common Implementation Pitfalls (Watch Out!)

### Pyomo-Specific Issues

**1. Indexing Mismatches**
```python
# WRONG: Creating variables with tuples
model.edges = Set(initialize=[(i,j) for i,j in G.edges()])
model.flow = Var(model.edges, model.demands)  # Won't work!

# RIGHT: Use separate indices
model.nodes = Set(initialize=G.nodes())
model.flow = Var(model.nodes, model.nodes, model.demands, domain=NonNegativeReals)
# Then check if (i,j) in G.edges() in constraints
```

**2. Constraint Rule Returns**
```python
# WRONG: Forgetting to return constraint expression
def capacity_rule(m, i, j):
    sum(m.flow[i,j,d] for d in m.demands) <= m.capacity[i,j]  # Missing return!

# RIGHT:
def capacity_rule(m, i, j):
    return sum(m.flow[i,j,d] for d in m.demands) <= m.capacity[i,j]
```

**3. Flow Conservation Node Identification**
```python
# WRONG: Hardcoding node names
if node == 'Yard_AA':  # Fragile!

# RIGHT: Using demand attributes
if node == demands[d]['origin']:  # Robust
```

### NetworkX Graph Issues

**4. Directed vs Undirected**
```python
# Ensure directed graph
assert isinstance(G, nx.DiGraph), "Network must be directed!"

# Getting edges correctly
out_edges = G.out_edges(node)  # Edges leaving node
in_edges = G.in_edges(node)    # Edges entering node
```

**5. Edge Attribute Access**
```python
# WRONG: Assuming edge exists
cost = G[i][j]['cost']  # KeyError if edge doesn't exist!

# RIGHT: Check first
if G.has_edge(i, j):
    cost = G[i][j]['cost']
```

### Solver Issues

**6. GLPK Solver Not Found**
```python
# Check solver availability
solver = SolverFactory('glpk')
if not solver.available():
    print("GLPK not found! Install: sudo apt-get install glpk-utils")
```

**7. Infeasible Models**
```python
# Always check solver status
results = solver.solve(model)
if results.solver.termination_condition != TerminationCondition.optimal:
    print(f"Warning: {results.solver.termination_condition}")
    # Model may be infeasible - check constraints!
```

---

## 💡 Key Insights & Decisions

### Why Start with Static Model?
1. **Faster Development:** Get working solver in hours, not days
2. **Easier Debugging:** Fewer variables and constraints to troubleshoot
3. **Incremental Complexity:** Add time windows after core logic works
4. **Interview-Ready:** Can demo and explain core concepts clearly

### Simplifications for Phase 1
- **No time windows:** Ignore delivery deadlines (add in Day 3)
- **No transit times:** Assume instantaneous travel (unrealistic but simplifies)
- **No yard capacity:** Only track edge capacity (node capacity is harder)
- **Static demands:** All demands known upfront (no dynamic arrivals)

### When to Add Complexity
- ✅ **After Test Scenario 3 passes:** Model is solid, ready for extensions
- ✅ **Tomorrow (Day 3):** Add time-indexed formulation with deadlines
- ⏳ **If time permits today:** Add yard capacity constraints

---

## 📈 Expected Results Summary

### Test Scenario Results (Predicted)

| Scenario | Demands | Satisfied | Total Cost | Solve Time |
|----------|---------|-----------|------------|------------|
| 1. Direct | 1 | 1 (100%) | ~$500 | <1s |
| 2. Multi-hop | 1 | 1 (100%) | ~$1,200 | <1s |
| 3. Multiple | 5 | 5 (100%) | ~$4,500 | <5s |
| 4. Capacity | 8 | 6-7 (75-88%) | ~$8,000 | <10s |
| 5. Full Network | 30 | 24-27 (80-90%) | ~$25,000 | <60s |

### Performance Targets
- **Satisfaction Rate:** ≥80% of demands routed successfully
- **Cost Improvement:** 15-25% better than greedy baseline
- **Solve Time:** <60 seconds for full network (20 nodes, 30 demands)
- **Scalability:** Linear growth in solve time with network size

---

## 📚 Learning Resources Used

### Primary References
1. **Network Optimization PDF** - Chapters 1-3
   - Min-cost flow formulation
   - Flow conservation constraints
   - Multi-commodity network flows

2. **Pyomo Optimization Book** - Chapters 1-3
   - ConcreteModel vs AbstractModel
   - Constraint rule syntax
   - Solver interface usage

### Key Concepts Mastered
- ✅ Flow conservation at nodes
- ✅ Capacity constraints formulation
- ✅ Binary variables for demand satisfaction
- ✅ Penalty costs for unmet demands
- 🔄 Pyomo model construction (in progress)
- ⏳ Solution extraction and validation

---

## ⏭️ Next Steps (Day 3 Preview)

### Tomorrow's Focus: Time Windows & ML Integration
1. **Add time-indexed formulation**
   - Discretize time into periods (e.g., hourly)
   - Add transit time on edges
   - Implement delivery deadline constraints

2. **Machine Learning Component**
   - Feature engineering for delay prediction
   - Train XGBoost model on historical patterns
   - Integrate predicted delays into routing costs

3. **Geospatial Visualization**
   - Plot network on actual map coordinates
   - Show optimal routes with flow thickness
   - Color-code by commodity type

---

## 🎯 Day 2 Deliverables Checklist

### Must Complete Today
- [ ] Working MILP optimization model in Pyomo
- [ ] GLPK solver successfully integrated
- [ ] Test Scenarios 1-3 passing
- [ ] Basic validation of results (flow conservation check)
- [ ] Code committed to GitHub with clear comments

### Nice to Have (If Time Permits)
- [ ] Test Scenarios 4-5 completed
- [ ] Baseline greedy algorithm implemented
- [ ] Performance comparison table
- [ ] Network visualization with solution overlay
- [ ] Detailed code documentation

### Can Move to Day 3
- [ ] Time window constraints
- [ ] Transit time modeling
- [ ] Advanced visualization (geospatial maps)
- [ ] ML integration preparation

---

## 📝 Notes & Observations

### Development Environment
- **Platform:** Ubuntu 24.04 (laptop preferred for solver dependencies)
- **Python Version:** 3.9+
- **Pyomo Installation:** `pip install pyomo --break-system-packages`
- **GLPK Installation:** `sudo apt-get install glpk-utils` ✅ COMPLETED
- **NetworkX Version:** 3.x (for Python 3.9+ compatibility)

### Git Repository Structure
```
Repository: railway-optimization-bnsf/
Branch: main
Recent Commits:
├── [Day 1] Initial commit - project structure
├── [Day 1] Add network generation and visualization
└── [Day 2] <pending> MILP model implementation
```

---

## 🚀 Motivation & Strategic Value

### Why This Project Matters for BNSF Interview

**Demonstrates Key Skills:**
1. ✅ **Discrete Optimization:** MILP formulation and solving
2. ✅ **Problem Decomposition:** Complex problem → mathematical model
3. 🔄 **Implementation Ability:** Theory → working code
4. ⏳ **ML Integration:** (Day 3) Delay prediction
5. ⏳ **Domain Expertise:** (Day 5) Railway-specific considerations

**Interview Talking Points:**
- "I built this to understand BNSF's routing optimization challenges"
- "Demonstrates ability to learn new domains quickly"
- "Combines OR techniques with modern ML approaches"
- "Ready to discuss trade-offs: optimality vs computation time"

---

## ✅ End of Day 2 Success Criteria

### Minimum Viable Product (MVP)
1. ✅ Pyomo model builds without errors
2. ✅ GLPK solver runs successfully
3. ✅ At least 1 test scenario solves correctly
4. ✅ Code committed to GitHub

### Stretch Goals
1. 🎯 All 5 test scenarios passing
2. 🎯 Performance benchmarking completed
3. 🎯 Baseline comparison implemented
4. 🎯 Solution validation thoroughly tested

### Ready for Day 3 If:
- ✅ Core routing optimization working
- ✅ Can explain MILP formulation clearly
- ✅ Have working code to build upon
- ✅ Know what to add next (time windows)

---

**Remember:** Done is better than perfect. Ship a working static router today, enhance it tomorrow.

---

*Progress Log*  
*Started: 9:00 AM, December 3, 2025*  
*Last Updated: [To be updated throughout the day]*  
*Target Completion: 6:00 PM, December 3, 2025*
