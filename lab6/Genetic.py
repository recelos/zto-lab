import time
from RandomNumberGenerator import RandomNumberGenerator

class Genetic:
    def __init__(self, flow_matrix, distance_matrix) -> None:
        self.rng = RandomNumberGenerator(123)
        self.flow_matrix = flow_matrix
        self.distance_matrix = distance_matrix

    def calculate_cost(self, solution) -> int:
        cost = 0
        n = len(solution)
        for i in range(n):
            for j in range(n):
                cost += self.flow_matrix[i][j] * self.distance_matrix[solution[i]][solution[j]]
        return cost

    def initialize_population(self, population_size, n) -> list:
        population = []
        for _ in range(population_size):
            individual = self.generate_permutation(n)
            population.append(individual)
        return population

    def generate_permutation(self, n) -> list:
        perm = list(range(n))
        for i in range(n):
            j = self.rng.nextInt(0, n - 1)
            perm[i], perm[j] = perm[j], perm[i]
        return perm

    def tournament_selection(self, population, k) -> list:
        selected = [population[self.rng.nextInt(0, len(population) - 1)] for _ in range(k)]
        selected.sort(key=self.calculate_cost)
        return selected[0]

    def order_crossover(self, parent1, parent2) -> list:
        n = len(parent1)
        start, end = sorted([self.rng.nextInt(0, n - 1) for _ in range(2)])
        child = [None] * n
        child[start:end + 1] = parent1[start:end + 1]
 
        pointer = 0
        for i in range(n):
            if pointer == start:
                pointer = end + 1
            if parent2[i] not in child:
                child[pointer] = parent2[i]
                pointer += 1
        return child
 
    def mutate(self, individual, mutation_rate) -> list:
        if self.rng.nextFloat(0, 1) < mutation_rate:
            i, j = self.rng.nextInt(0, len(individual) - 1), self.rng.nextInt(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def solve(self, population_size=100, generations=500,
        mutation_rate=0.1, tournament_size=5, max_time=60) -> tuple:
        n = len(self.flow_matrix)
        population = self.initialize_population(population_size, n)

        best_solution = min(population, key=self.calculate_cost)
        best_cost = self.calculate_cost(best_solution)

        print(f"0    {best_cost}")

        start_time = time.time()

        for generation in range(1, generations + 1):
            current_time = time.time()
            if current_time - start_time > max_time:
                break

            new_population = []
            for _ in range(population_size):
                parent1 = self.tournament_selection(population, tournament_size)
                parent2 = self.tournament_selection(population, tournament_size)
                child = self.order_crossover(parent1, parent2)
                child = self.mutate(child, mutation_rate)
                new_population.append(child)

            population = new_population

            current_best_solution = min(population, key=self.calculate_cost)
            current_best_cost = self.calculate_cost(current_best_solution)

            if current_best_cost < best_cost:
                best_solution = current_best_solution
                best_cost = current_best_cost
                print(f"{generation}    {best_cost}")

        return best_solution, best_cost
