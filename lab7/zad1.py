import math
import matplotlib.pyplot as plt
from RandomNumberGenerator import RandomNumberGenerator

SEED = 3423
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

def calculate_objectives(solution, processing_times, due_dates) -> tuple[int, int]:
    num_machines = len(processing_times)
    num_jobs = len(solution)
    completion_times = [[0] * num_jobs for _ in range(num_machines)]
    total_flowtime = 0
    max_tardiness = 0
    
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
        tardiness = max(0, completion_times[-1][j] - due_dates[j])
        max_tardiness = max(max_tardiness, tardiness)
    
    return total_flowtime, max_tardiness

def generate_neighbour(solution):
    new_solution = solution[:]
    i, j = 0, 0
    while i == j:
        i = rng.nextInt(0,len(solution)-1)
        j = rng.nextInt(0,len(solution)-1)
    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
    return new_solution

def dominates(sol1, sol2, processing_times, due_dates) -> bool:
    obj1 = calculate_objectives(sol1, processing_times, due_dates)
    obj2 = calculate_objectives(sol2, processing_times, due_dates)
    return ((obj1[0] <= obj2[0] and obj1[1] <= obj2[1]) and (obj1[0] < obj2[0] or obj1[1] < obj2[1]))

def simulated_annealing(processing_times, due_dates, max_iter) -> tuple:
    N = len(processing_times[0])
    current_solution = initialize_solution(N)
    P = [current_solution]
    probability = 0.995
    it = 0

    for _ in range(max_iter):
        it += 1
        neighbour_solution = generate_neighbour(current_solution)

        if dominates(neighbour_solution, current_solution, processing_times, due_dates):
            current_solution = neighbour_solution
            P.append(neighbour_solution)
        else:
            current_solution = neighbour_solution
            if probability > rng.nextFloat(0, 1):
                P.append(neighbour_solution)

        probability = math.pow(probability, it)
    return P

def pareto_front(P, processing_times, due_dates) -> list:
    f = []
    for solution in P:
        if not any(dominates(other_solution, solution, processing_times, due_dates) for other_solution in P):
            f.append(solution)
    
    return f

def plot_pareto_front(P, F, processing_times, due_dates, reference_point = None) -> None:
    all_objectives = [calculate_objectives(sol, processing_times, due_dates) for sol in P]
    pareto_objectives = [calculate_objectives(sol, processing_times, due_dates) for sol in F]
    
    plt.scatter([obj[0] for obj in all_objectives], [obj[1] for obj in all_objectives], label='All Solutions')
    plt.scatter([obj[0] for obj in pareto_objectives], [obj[1] for obj in pareto_objectives], color='red', label='Pareto Front')
    
    if(reference_point is not None):
        plt.scatter(reference_point[0], reference_point[1], color='black', label='Reference point')
        

    plt.xlabel('Total Flowtime')
    plt.ylabel('Max Tardiness')
    plt.title('Pareto Front Visualization')
    plt.legend()
    plt.show()

def calculate_hypervolume(front, reference_point):
    sorted_front = sorted(front, key=lambda x: x[0])
    hvi = 0.0
    for i in range(len(sorted_front)):
        if i == 0:
            hvi += (reference_point[0] - sorted_front[i][0]) * (reference_point[1] - sorted_front[i][1])
        else:
            hvi += (reference_point[0] - sorted_front[i][0]) * (sorted_front[i-1][1] - sorted_front[i][1])
    return hvi

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
    return processing_times, due_dates


def main() -> None:
    N = 10
    a = 0
    processing_times, due_dates = generate_instance(N, a)
    max_iters = [100,200,400,800,1600,3200]
    
    fronts = []
    ps = []
    objectives = []
    
    for max_iter in max_iters:
        p = simulated_annealing(processing_times, due_dates, max_iter)
        f = pareto_front(p, processing_times, due_dates)   
        fronts.append(f)
        ps.append(p)
        objectives.append((max_iter, [calculate_objectives(sol, processing_times, due_dates) for sol in f]))

    flattened = [item for sublist in objectives for item in sublist[1]]
    reference_point = (max(obj[0] for obj in flattened), max(obj[1] for obj in flattened))

    print(reference_point)

    hs = []
    for i in range(len(max_iters)):
        max_iter, pareto_objectives = objectives[i] 

        hv = calculate_hypervolume(pareto_objectives, reference_point)
        hs.append((max_iter, hv))
        plot_pareto_front(ps[i], fronts[i], processing_times, due_dates, reference_point)

    print(hs)

if __name__ == '__main__':
    main()
