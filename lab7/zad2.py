import math
import matplotlib.pyplot as plt
from RandomNumberGenerator import RandomNumberGenerator

SEED = 13412
rng = RandomNumberGenerator(SEED)

def shuffle(arr):
    n = len(arr)
    for i in range(n-1, 0, -1):
        j = rng.nextInt(0, i)
        arr[i], arr[j] = arr[j], arr[i]

def initialize_solution(N):
    solution = list(range(N))
    shuffle(solution)
    return solution

def calculate_objectives(solution, processing_times, due_dates) -> tuple[int, int, int]:
    num_machines = len(processing_times)
    num_jobs = len(solution)
    completion_times = [[0] * num_jobs for _ in range(num_machines)]
    total_flowtime = 0
    max_tardiness = 0
    max_lateness = 0
    
    for i in range(num_machines):
        for j in range(num_jobs):
            job = solution[j]
            if i == 0 and j == 0:
                completion_times[i][j] = processing_times[i][job]
            elif i == 0:
                completion_times[i][j] = completion_times[i][j-1] + processing_times[i][job]
            elif j == 0:
                completion_times[i][j] = completion_times[i-1][j] + processing_times[i][job]
            else:
                completion_times[i][j] = max(completion_times[i-1][j], completion_times[i][j-1]) + processing_times[i][job]
    
    for j in range(num_jobs):
        job = solution[j]
        total_flowtime += completion_times[-1][j]
        lateness = completion_times[-1][j] - due_dates[j]
        tardiness = max(0, lateness)
        max_tardiness = max(max_tardiness, tardiness)
        max_lateness = max(max_lateness, lateness)
    
    return total_flowtime, max_tardiness, max_lateness

def scalarized_objective(solution, processing_times, due_dates, weights):
    total_flowtime, max_tardiness, max_lateness = calculate_objectives(solution, processing_times, due_dates)
    return weights[0] * total_flowtime + weights[1] * max_tardiness + weights[2] * max_lateness

def generate_neighbour(solution):
    new_solution = solution[:]
    i, j = 0, 0
    while i == j:
        i = rng.nextInt(0,len(solution)-1)
        j = rng.nextInt(0,len(solution)-1)
    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
    return new_solution

def simulated_annealing(processing_times, due_dates, max_iter) -> tuple:
    N = len(processing_times[0])
    current_solution = initialize_solution(N)
    P = [current_solution]
    
    weights = [0.33, 0.33, 0.34] 
    
    probability = 0.995
    it = 0
    for _ in range(max_iter):
        it += 1
        neighbour_solution = generate_neighbour(current_solution)
        current_obj = scalarized_objective(current_solution, processing_times, due_dates, weights)
        neighbour_obj = scalarized_objective(neighbour_solution, processing_times, due_dates, weights)
        
        if neighbour_obj < current_obj:
            current_solution = neighbour_solution
            P.append(neighbour_solution)
        else:
            if probability > rng.nextFloat(0, 1):
                current_solution = neighbour_solution
                P.append(neighbour_solution)
        probability = math.pow(probability, it)
    return P

def plot_pareto_front(P, processing_times, due_dates) -> None:
    objectives = [calculate_objectives(sol, processing_times, due_dates) for sol in P]
    
    plt.scatter([obj[0] for obj in objectives], [obj[1] for obj in objectives], label='Solutions', color='blue')
    
    plt.xlabel('Total Flowtime')
    plt.ylabel('Max Tardiness & Max Lateness')
    plt.title('Objective Space')
    plt.show()

def main() -> None:
    N = 10
    a = 0
    processing_times, due_dates = generate_instance(N, a)
    max_iter = 400
    
    p = simulated_annealing(processing_times, due_dates, max_iter)
    
    print('Solution Set P:', p)
    plot_pareto_front(p, processing_times, due_dates)

def generate_instance(N, a):
    processing_times = [[None]*N for _ in range(3)]
    for i in range(3):
        for j in range(N):
            processing_times[i][j] = rng.nextInt(1,99)
            a+=processing_times[i][j]
    b = math.floor(a/2)
    a = math.floor(a/6)
    due_dates = []
    for j in range(N):
        due_dates.append(rng.nextInt(a,b))
    return processing_times,due_dates

if __name__ == '__main__':
    main()