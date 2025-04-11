import xpress as xp

# number of nodes
n = 5
# decleare set of nodes
V = range(n)
# decleare set of edges
E = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [2, 3], [3, 4]]
# decleare set of colors
C = range(n)

prob = xp.problem(name='GraphColoring')

# decision variables
# x is a VxC matrix where where each element (x[v][c]) is a binary value equal to 1 if the v node is colored with the c color
x = prob.addVariables(V, C, name="x", vartype=xp.binary)
# y is a C binary vector where each element (y[c]) is a binary value equal to 1 if the c color is used
y = prob.addVariables(C, name="y", vartype=xp.binary)

# objective function (minimize the number of colors used)
prob.setObjective(xp.Sum(y), sense=xp.minimize)

# constraints
# each node must be colored with exactly one color
horizontal_sum = [xp.Sum(x[v,c] for c in C) == 1 for v in V]

# adjacent nodes must have different colors
adjacent = [x[u, c] + x[v, c] <= 1 for (u, v) in E for c in C]

# if a color is used for a node, then it must be used
used_colors = [x[v, c] <= y[c] for v in V for c in C]

prob.addConstraint(horizontal_sum + adjacent + used_colors)

# solve the problem
prob.solve()

# print the solution
for v in V:
    for c in C:
        if prob.getSolution(x[v, c]) > 0.5:
            print(f"Node {v} is colored with {c}")

# print the number of colors used
num_colors = sum(prob.getSolution(y[c]) for c in C)
print(f"Minimum number of colors used: {num_colors}")

# model GraphColoring
# uses "mmxprs"

# ! Declare sets and parameters
# declarations
#     n: integer
#     V: set of integer
#     E: set of (integer, integer)
#     C: set of integer
#     x: array(V, C) of mpvar
#     y: array(C) of mpvar
# end-declarations

# ! Define the number of nodes and edges
# n := 5
# V := {1..n}
# E := {(0,1), (0,2), (0,3), (0,4), (1,2), (2,3), (3,4)}
# C := {1..n}  ! Colors

# ! Create decision variables
# x(V, C) := array(V, C) of mpvar
# y(C) := array(C) of mpvar

# ! Objective function: Minimize the number of colors used
# minimize(sum(c in C) y[c])

# ! Constraints:
# ! 1. Each node must be colored with exactly one color
# forall(v in V) do
#     sum(c in C) x[v, c] = 1
# end-do

# ! 2. Adjacent nodes must have different colors
# forall((u, v) in E, c in C) do
#     x[u, c] + x[v, c] <= 1
# end-do

# ! 3. If a color is used for a node, it must be marked as used
# forall(v in V, c in C) do
#     x[v, c] <= y[c]
# end-do

# ! Solve the problem
# maximize(sum(c in C) y[c])

# ! Output the solution
# writeln("Optimal Coloring:")
# forall(v in V) do
#     forall(c in C) do
#         if getsol(x[v,c]) > 0.5 then
#             writeln("Node ", v, " is colored with color ", c)
#         end-if
#     end-do
# end-do

# ! Output the number of colors used
# num_colors := 0
# forall(c in C) do
#     if getsol(y[c]) > 0.5 then
#         num_colors := num_colors + 1
#     end-if
# end-do
# writeln("Minimum number of colors used: ", num_colors)

# end-model