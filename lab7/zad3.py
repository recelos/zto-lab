import math
import matplotlib.pyplot as plt
import numpy as np
from RandomNumberGenerator import RandomNumberGenerator
from visualize import drawFace
from sklearn.preprocessing import MinMaxScaler
import matplotlib

SEED = 12345
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
    total_lateness = 0
    
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
        total_lateness += lateness
    return total_flowtime, max_tardiness, max_lateness, total_lateness

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
    return ((obj1[0] <= obj2[0] and obj1[1] <= obj2[1] and obj1[2] <= obj2[2] and obj1[3] <= obj2[3]) and (obj1[0] < obj2[0] or obj1[1] < obj2[1] or obj1[2] < obj2[2] or obj1[3] < obj2[3]))

def simulated_annealing(processing_times, due_dates, max_iter, initial_solution) -> tuple:
    N = len(processing_times[0])
    current_solution = initial_solution
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


def create_bar_charts(data, labels):
    y1 = [d[0] for d in data]
    y2 = [d[1] for d in data]
    y3 = [d[2] for d in data]
    y4 = [d[3] for d in data]

    xticklabels = ['rozw 1', 'rozw 2', 'rozw 3', 'rozw losowe']
    x = np.arange(len(xticklabels))
    width = 0.2

    fig, ax = plt.subplots()
    ax.bar(x - 1.5*width, y1, width, label=labels[0])
    ax.bar(x - 0.5*width, y2, width, label=labels[1])
    ax.bar(x + 0.5*width, y3, width, label=labels[2])
    ax.bar(x + 1.5*width, y4, width, label=labels[3])

    ax.set_xlabel('Rozwiązania')
    ax.set_ylabel('Wartości')
    ax.set_xticks(x)
    ax.set_xticklabels(xticklabels)
    ax.legend()

    fig.tight_layout()
    plt.show()

def plot_multiway_dotplots(solutions, criteria_labels):
    _, ax = plt.subplots(figsize=(10, 8))
    colors = ['red', 'blue', 'green', 'orange']
    solution_labels = ['rozw 1', 'rozw 2', 'rozw 3', 'rozw losowe']

    num_solutions = len(solutions)
    num_criteria = len(criteria_labels)
    
    min_value = np.min(solutions)
    max_value = np.max(solutions)

    legend_handles = [] 

    for i, solution in enumerate(solutions):
        for criterion_idx, value in enumerate(solution):
            y = criterion_idx + i * (num_criteria + 1)
            ax.plot([min_value, max_value], [y, y], color='gray')
            ax.plot(value, y, 'o', color=colors[i])
        handle = ax.plot(value, y, 'o', color=colors[i], label=solution_labels[i])
        
        legend_handles.append(handle[0]) # Collect handles for legend

    y_ticks = [i + j * (num_criteria + 1) for j in range(num_solutions) for i in range(num_criteria)]
    y_ticklabels = [f'{criteria_labels[i % num_criteria]}' for i in range(num_solutions * num_criteria)]
    
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticklabels)
    ax.set_xlabel('wartości')
    ax.legend()
    plt.tight_layout()
    plt.show()

def plot_star_coordinate_system_with_line_segments(solutions, criteria_labels):
    fig, axs = plt.subplots(1, len(solutions), figsize=(len(solutions) * 5, 5), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(criteria_labels), endpoint=False).tolist()
    colors = ['red', 'blue', 'green', 'orange']
    solution_labels = ['rozw 1', 'rozw 2', 'rozw 3', 'rozw losowe']
    for i, solution in enumerate(solutions):
        values = list(solution)
        if len(solutions) == 1:
            ax = axs
        else:
            ax = axs[i]
        
        for j in range(len(criteria_labels)):
            ax.plot([angles[j], angles[(j + 1) % len(criteria_labels)]],
                    [values[j], values[(j + 1) % len(criteria_labels)]],
                    color=colors[i % len(colors)], alpha=0.75)
        
        ax.fill(angles, values, color=colors[i % len(colors)], alpha=0.4)
        
        ax.set_yticklabels([])
        ax.set_xticks(angles)
        ax.set_xticklabels(criteria_labels)
        ax.set_title(solution_labels[i])
        ax.spines['polar'].set_visible(False)
        
    plt.tight_layout()    
    plt.show()

def normalize_data(data):
    normalized_data = []
    final_normalized_data = []
    all_values = [value for tuple in data for value in tuple]
    min_val = min(all_values)
    max_val = max(all_values)
    print(min_val)
    print(max_val)
    for criterion_values in zip(*data):
        normalized_data = []
        for val in criterion_values:
            normalized_criterion = (val - min_val) / (max_val - min_val)
            print(f"Normalizowanie wartości {val}: ({val} - {min_val}) / ({max_val} - {min_val}) = {normalized_criterion}")
            normalized_data.append(normalized_criterion)
        final_normalized_data.append(normalized_data)
    final_normalized_data = [list(x) for x in zip(*final_normalized_data)]
    return final_normalized_data 

def normalize_values(data):
    data_array = np.array(data)
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data_array)
    normalized_data_tuples = [tuple(row) for row in normalized_data]
    return normalized_data_tuples

def normalize_tuples(tuples):
    # Znajdź minimalne i maksymalne wartości dla każdego elementu krotki
    min_vals = [min(t[i] for t in tuples) for i in range(len(tuples[0]))]
    max_vals = [max(t[i] for t in tuples) for i in range(len(tuples[0]))]
    
    # Znormalizuj wartości
    normalized_tuples = []
    for t in tuples:
        normalized_tuple = tuple(
            (t[i] - min_vals[i]) / (max_vals[i] - min_vals[i]) if max_vals[i] != min_vals[i] else 0
            for i in range(len(t))
        )
        normalized_tuples.append(normalized_tuple)
    
    return normalized_tuples

def draw_faces(values, file_name):
    drawFace(values[0],values[1],values[2],values[3], file_name)

def main() -> None:
    N = 10
    a = 0
    processing_times, due_dates = generate_instance(N, a)
    initial_solution = initialize_solution(N)
    max_iters = [100,200,400,800,1600,3200]
    
    fronts = []
    
    for max_iter in max_iters:
        p = simulated_annealing(processing_times, due_dates, max_iter, initial_solution)
        f = pareto_front(p, processing_times, due_dates)   
        fronts.append((max_iter, f))
        initial_solution = initialize_solution(N)


    fronts = [item for sublist in fronts for item in sublist[1]][-3:]
    objectives = [calculate_objectives(sol, processing_times, due_dates) for sol in fronts]
    objectives.append(calculate_objectives(initial_solution, processing_times, due_dates))
    print(objectives)
    labels = ['Total Flowtime', 'Max Tardiness', 'Max Lateness', 'Total Lateness']
    sol_labels = ['rozw1.png', 'rozw2.png', 'rozw3.png', 'rozw_losowe.png']
    matplotlib.use('TkAgg')
    create_bar_charts(objectives, labels)
    plot_multiway_dotplots(objectives, labels)
    normalized_objectives = normalize_tuples(objectives)
    plot_star_coordinate_system_with_line_segments(normalized_objectives, labels)
    
    for i in range(4):
        draw_faces(normalized_objectives[i], sol_labels[i])


if __name__ == '__main__':
    main()