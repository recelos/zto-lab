from docplex.mp.model import Model
from RandomNumberGenerator import RandomNumberGenerator

#initialize data
SEED = 3123

N = 250

rng = RandomNumberGenerator(SEED)

values = []
for i in range(0, N):
    values.append(rng.nextInt(-100, 100))

t = rng.nextInt(-50 * N, 50 * N)

#prepare model
m = Model(name='subset_sum_problem')

x = m.binary_var_list(len(values), name='x')

#solution
m.minimize(m.abs(m.sum(x[i] * values[i] for i in range(len(values))) - t))
solution = m.solve(log_output=True)

m.print_solution()
