from instances import *
from environments import *
from solvers import *
from solutions import *

instance_name = 'very_big_very_instance'

inst = Instance(instance_name)
env = Environment(inst)
solver = solver_346742_344060_346316.solver_346742_344060_346316(env)

X, Y = solver.solve()

sol = Solution(X, Y)
sol.write(instance_name)