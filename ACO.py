import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

best_values = []

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

def ant_colony_optimization(points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q):
    start_time = time.time()  # Record the start time
    
    n_points = len(points)
    pheromone = np.ones((n_points, n_points))
    best_path = None
    best_path_length = np.inf
    
    for iteration in range(n_iterations):
        paths = []
        path_lengths = []
        convergence_rates=[]
        
        for ant in range(n_ants):
            visited = [False]*n_points
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
            
            paths.append(path)
            path_lengths.append(path_length)
            
            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length
                #print(best_path_length)
            
            best_values.append(best_path_length)
            
            if iteration > 0:
                convergence_rate = best_values[iteration-1] - best_values[iteration]
                convergence_rates.append(convergence_rate)
                #print(best_values[iteration-1] - best_values[iteration])
            
        pheromone *= evaporation_rate
        #print(" convergence rate: ".format(convergence_rates))    
        for path, path_length in zip(paths, path_lengths):
            for i in range(n_points-1):
                pheromone[path[i], path[i+1]] += Q/path_length
            pheromone[path[-1], path[0]] += Q/path_length
    
        end_time = time.time()  # Record the end time
        runtime = end_time - start_time  # Calculate the runtime
        print("Runtime: {:.2f} seconds".format(runtime))  
        
    
   
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:,0], points[:,1], points[:,2], c='r', marker='o')
    
    for i in range(n_points-1):
        ax.plot([points[best_path[i],0], points[best_path[i+1],0]],
                [points[best_path[i],1], points[best_path[i+1],1]],
                [points[best_path[i],2], points[best_path[i+1],2]],
                c='g', linestyle='-', linewidth=2, marker='o')
        
    ax.plot([points[best_path[0],0], points[best_path[-1],0]],
            [points[best_path[0],1], points[best_path[-1],1]],
            [points[best_path[0],2], points[best_path[-1],2]],
            c='g', linestyle='-', linewidth=2, marker='o')
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()

# Example usage:
file_path = r'lin318.tsp'  # Replace with the path to your lin318 .tsp file
points = read_tsp_file(file_path)
ant_colony_optimization(points, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, Q=1)
