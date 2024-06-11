from docplex.mp.model import Model
from RandomNumberGenerator import RandomNumberGenerator

SEED = 9412
N = 10
rng = RandomNumberGenerator(SEED)
Objects = range(N)

weights1 = [rng.nextInt(1, 10) for _ in Objects]
weights2 = [rng.nextInt(1, 10) for _ in Objects]
values = [rng.nextInt(1, 10) for _ in Objects]
capacity = rng.nextInt(N, 4*N)

m = Model(name='double_backpack')

x1 = {i: m.continuous_var(name=f'x1[{i}]', lb=0, ub=1) for i in Objects}
x2 = {i: m.continuous_var(name=f'x2[{i}]', lb=0, ub=1) for i in Objects}

m.maximize(m.sum(values[i] * (x1[i] + x2[i]) for i in Objects))

m.add_constraint(m.sum(weights1[i] * x1[i] for i in Objects) <= capacity)
m.add_constraint(m.sum(weights2[i] * x2[i] for i in Objects) <= capacity)

for i in Objects:
    m.add_constraint(x1[i] + x2[i] <= 1)

solution = m.solve(log_output=True)
m.print_solution()
