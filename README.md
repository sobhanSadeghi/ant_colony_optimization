# Ant Colony Optimization for TSP (LIN318)

This repository contains Python implementations of Ant Colony Optimization (ACO) algorithms for solving the Traveling Salesman Problem (TSP) using the LIN318 dataset. Additionally, it includes parallel Ant Colony and Independent Ant Colony algorithms for the same problem.

## Introduction

The Traveling Salesman Problem is a classic optimization problem in computer science and operations research. Given a list of cities and the distances between them, the objective is to find the shortest possible route that visits each city exactly once and returns to the starting city.

Ant Colony Optimization (ACO) is a metaheuristic algorithm inspired by the foraging behavior of ants. It involves simulating the behavior of a colony of ants as they search for the optimal path. The ants deposit pheromones on the edges of the graph, and the pheromone trails guide other ants in finding shorter paths.

## Features
* ACO Algorithm: Implementation of the Ant Colony Optimization algorithm specifically designed for solving the TSP using the LIN318 dataset.
* Parallel Ant Colony: Implementation of a parallel version of the ACO algorithm. Multiple colonies of ants work simultaneously, each updating its own pheromone trails.
* Independent Ant Colony: Implementation of an independent version of the ACO algorithm. Each ant works independently without communication, exploring the solution space.

## Dependencies
The following dependencies are required to run the code:

* Python 3.x
* numpy
* matplotlib



### You can install the dependencies using pip:
```pip install numpy matplotlib```


## Usage

```git clone https://github.com/sobhanSadeghi/ant_colony_optimization.git```


## Contributing

Contributions to this repository are welcome. If you find any issues or have any improvements to suggest, please feel free to open an issue or submit a pull request.

