from RandomNumberGenerator import RandomNumberGenerator
from KnackpackSolver import KnapsackSolver

def main():
    SEED = 124151243
    rng = RandomNumberGenerator(SEED)
    N = 15
    items = [(rng.nextInt(1, 30), rng.nextInt(1, 30)) for _ in range(N)]
    B = rng.nextInt(5 * N, 10 * N)

    print(f"Capacity={B}")

    solver = KnapsackSolver(items, B)
    max_value, items_taken = solver.solve()
    print("Max value:", max_value)
    print("Items taken:", items_taken)

if __name__ == '__main__':
    main()
