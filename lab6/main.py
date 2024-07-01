from RandomNumberGenerator import RandomNumberGenerator
from Genetic import Genetic

def main():
    SEED = 1
    SIZE = 40
    rng = RandomNumberGenerator(SEED)

    flow_matrix = [[rng.nextInt(0,50) for _ in range(SIZE)] for _ in range(SIZE)]
    distance_matrix = [[rng.nextInt(0,50) for _ in range(SIZE)] for _ in range(SIZE)]

    genetic = Genetic(flow_matrix, distance_matrix)

    best_solution, best_cost = genetic.solve(population_size=60, generations=500, mutation_rate=0.3, tournament_size=5, max_time=600)
    print(f"Best Solution: {best_solution}, Best Cost: {best_cost}")

if __name__=='__main__':
    main()
