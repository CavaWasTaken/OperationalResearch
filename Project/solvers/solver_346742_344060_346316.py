from .abstract_solver import AbstractSolver
import numpy as np
import gurobipy as gp
from gurobipy import GRB

class solver_346742_344060_346316(AbstractSolver):
    def __init__(self, env):
        super().__init__(env)
        self.name = 'solver_346742_344060_346316'
    
    def solve(self):
        super().solve()

        distances = self.env.inst.distances
        service = self.env.inst.service
        N_deposits = service.shape[0]
        N_supermarkets = service.shape[1]
        dailyWarehouseCost = self.env.inst.weights['construction']
        dailyPenaltyCost = self.env.inst.weights['missed_supermarket']
        travelCost = self.env.inst.weights['travel']

        model = gp.Model(self.name)

        # X - binary array sized as the number of possible warehouse locations, x[i] = 1 means that a warehouse is located at i
        X = model.addVars(N_deposits, vtype=GRB.BINARY, name="X")
        # Y - binary quadratic matrix sized as the number of warehouses plus the company, x[i][j] = 1 means that the path from i to j is used
        Y = model.addVars(N_deposits+1, N_deposits+1, vtype=GRB.BINARY, name="Y")
        # Z - binary array sized as the number of supermarkets, z[i] = 1 means that supermarket i is unserved
        Z = model.addVars(N_supermarkets, vtype=GRB.BINARY, name="Z")
        # P - integer array sized as the number of warehouses, u[i] is rappresent the position order of the warehouse i in the path
        P = model.addVars(N_deposits, vtype=GRB.INTEGER, lb=1, ub=N_deposits, name="P")

        # Objective function is composed by three parts to be minimized:
        model.setObjective(
            gp.quicksum(dailyWarehouseCost * X[i] for i in range(N_deposits)) + # 1. The cost of opening warehouses
            gp.quicksum(dailyPenaltyCost * Z[i] for i in range(N_supermarkets)) +   # 2. The penalty for not serving supermarkets
            gp.quicksum(travelCost * Y[i, j] * distances[i,j] for i in range(N_deposits + 1) for j in range(N_deposits + 1)),    # 3. The cost of the paths used
            GRB.MINIMIZE
        )

        # Constraints
        # 1. Each supermarket must be served by at least one warehouse or a penalty is incurred
        for s in range(N_supermarkets):
            model.addConstr(
                gp.quicksum(service[w][s] * X[w] for w in range(N_deposits)) >= 1 - Z[s],
                name=f"unserved_def_{s}"
            )
        # 2. The vehicle starts from the company
        model.addConstr(
            gp.quicksum(Y[0, j] for j in range(1, N_deposits + 1)) == 1,
            name="start_at_company"
        )
        # 3. The vehicle ends at the company
        model.addConstr(
            gp.quicksum(Y[i, 0] for i in range(1, N_deposits + 1)) == 1,
            name="end_at_company"
        )
        # 4. Each warehouse can only be visited if it is open
        for i in range(1, N_deposits + 1):
            model.addConstr(
                gp.quicksum(Y[i, j] for j in range(N_deposits+1) if j != i) == X[i-1], name=f"out_{i}"
            )
            model.addConstr(
                gp.quicksum(Y[j, i] for j in range(N_deposits+1) if j != i) == X[i-1], name=f"in_{i}"
            )

        # 5. Avoid sub-tours
        for i in range(1, N_deposits + 1):
            for j in range(1, N_deposits + 1):
                if i != j:
                    model.addConstr(
                        P[i-1] - P[j-1] + N_deposits * Y[i, j] <= N_deposits - 1,
                        name=f"subtour_{i}_{j}"
                    )

        # 6. Avoid self-loops
        for i in range(N_deposits + 1):
            model.addConstr(
                Y[i, i] == 0,
                name=f"no_self_loop_{i}"
            )

        # solve the model
        model.optimize()

        X = np.array([int(X[i].X) for i in range(N_deposits)])
        Y = np.array([[int(Y[i, j].X) for j in range(N_deposits + 1)] for i in range(N_deposits + 1)])

        return X, Y