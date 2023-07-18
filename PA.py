import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import concurrent.futures

def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

def read_tsp_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    coordinates = []
    for line in lines:
        if line.strip() == "NODE_COORD_SECTION":
            break
    else:
        raise ValueError("NODE_COORD_SECTION not found in the .tsp file.")
    
    for line in lines:
        if line.strip() == "EOF":
            break
        parts = line.strip().split()
        if len(parts) == 3:
            coordinates.append((float(parts[1]), float(parts[2])))
    
    return np.array(coordinates)

def ant_tour(ant,n_points,pheromone):
    visited = [False] * n_points
    current_point = np.random.randint(n_points)
    visited[current_point] = True
    path = [current_point]
    path_length = 0

    while False in visited:
        unvisited = np.where(np.logical_not(visited))[0]
        probabilities = np.zeros(len(unvisited))

        for i, unvisited_point in enumerate(unvisited):
            probabilities[i] = pheromone[current_point, unvisited_point]**alpha / distance(points[current_point], points[unvisited_point])**beta

        probabilities /= np.sum(probabilities)

        next_point = np.random.choice(unvisited, p=probabilities)
        path.append(next_point)
        path_length += distance(points[current_point], points[next_point])
        visited[next_point] = True
        current_point = next_point

    return path, path_length

def ant_colony_optimization_thread(points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q, pheromone_share):
    start_time = time.time()

    n_points = len(points)
    pheromone = np.ones((n_points, n_points))
    best_path = None
    best_path_length = np.inf
    convergence_rates = []

    for iteration in range(n_iterations):
        paths = []
        path_lengths = []

        for ant in range(n_ants):
            path, path_length = ant_tour(ant,n_points,pheromone)
            paths.append(path)
            path_lengths.append(path_length)

            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length

        pheromone_iteration = np.zeros((n_points, n_points))
        for path, path_length in zip(paths, path_lengths):
            for i in range(n_points - 1):
                pheromone_iteration[path[i], path[i + 1]] += Q / path_length
            pheromone_iteration[path[-1], path[0]] += Q / path_length

        pheromone *= evaporation_rate
        pheromone += pheromone_share * pheromone_iteration

    
        end_time = time.time()
        runtime = end_time - start_time
        print("Runtime: {:.2f} seconds".format(runtime))



# Example usage:
file_path = r'lin318.tsp'  # Replace with the path to your lin318 .tsp file
points = read_tsp_file(file_path)
n_ants = 10
n_iterations = 100
alpha = 1
beta = 1
evaporation_rate = 0.5
Q = 1
pheromone_share = 0.1

num_threads = 4
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = []

    for _ in range(num_threads):
        # Submit the ant_colony_optimization_thread function as a separate thread
        future = executor.submit(ant_colony_optimization_thread, points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q, pheromone_share)
        futures.append(future)

    # Wait for all threads to complete
    concurrent.futures.wait(futures)

ant_colony_optimization_thread(points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q, pheromone_share)
