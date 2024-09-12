import z3
from z3 import Solver, Int, Or, If


# ==== Constants ====
# Number of sides of the dice
N = 8

# Probabilities
ps = [i + 1 for i in range(N - 1)]
ps = [0] + ps + [N] + ps[::-1]
P = list(ps)

# Range of the number of pips
L = 1
U = 2*N


# ==== Free variables ====
# Values of d1
xs = [Int('x_' + str(i + 1))
      for i in range(N)]

# Values of d2
ys = [Int('y_' + str(i + 1))
      for i in range(N)]


# ==== Equations ====
s = Solver()

# Range of x_i
for i in range(N):
    s.add(L <= xs[i])
    s.add(xs[i] <= U)

# Range of y_i
for i in range(N):
    s.add(L <= ys[i])
    s.add(ys[i] <= U)

# Sorted values
for i in range(N - 1):
    s.add(xs[i] <= xs[i + 1])
    s.add(ys[i] <= ys[i + 1])

# Probabilities
for n in range(2*N):
    count_n = sum([If(xs[i] + ys[j] == n + 1, 1, 0)
                   for i in range(N) for j in range(N)])
    s.add(count_n == P[n])


# ==== Solution ====
# print(s.sexpr())

running = True
sol_count = 0
while running:
    # Check whether the problem is sat or unsat
    check = s.check()

    # If sat, print model
    if (check == z3.sat):
        sol_count += 1

        print('================================================================')
        print(f'Solution {sol_count}:')

        m = s.model()
        res_x = [int(str(m[x])) for x in xs]
        res_y = [int(str(m[y])) for y in ys]

        print(f'Die 1: {res_x}')
        print(f'Die 2: {res_y}')

        # Add constraint to disallow current solution
        s.add(Or([xs[i] != res_x[i] for i in range(N)]))
        s.add(Or([ys[i] != res_x[i] for i in range(N)]))

    else:
        running = False
