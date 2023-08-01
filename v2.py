import random
import math

# City map and path restrictions
path_map = [
        [1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 0, 0]
    ]

path_restrictions = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0]
    ]
# Constants for the problem
MAX_WEIGHT = 15
MAX_CARTONS_MILK = 15
MAX_BREAD_LOAVES = 15

# Number of individuals in the population
POPULATION_SIZE = 50

# Number of generations
NUM_GENERATIONS = 100

# Number of coordinates in a path
NUM_COORDINATES = 15

# Food consumption per week for children and adults
FOOD_CONSUMPTION_CHILD = {
    "milk": 3,
    "bread": 1
}

FOOD_CONSUMPTION_ADULT = {
    "flour": 3,
    "rice": 3,
    "dhal": 1
}

# Calculate the total food required for all people
def total_food_required(people):
    total_milk = people["children"] * FOOD_CONSUMPTION_CHILD["milk"]
    total_bread = people["children"] * FOOD_CONSUMPTION_CHILD["bread"]
    total_flour = people["adults"] * FOOD_CONSUMPTION_ADULT["flour"]
    total_rice = people["adults"] * FOOD_CONSUMPTION_ADULT["rice"]
    total_dhal = people["adults"] * FOOD_CONSUMPTION_ADULT["dhal"]

    return total_milk, total_bread, total_flour, total_rice, total_dhal

# Function to calculate the distance between two points
def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

# Function to calculate the fitness of a path based on the total distance traveled
# and whether all tents are supplied
def calculate_fitness(path, total_food):
    food_weight = total_food[0] + total_food[1]
    distance_travelled = 0
    tents_supplied = set()

    for i in range(1, len(path)):
        x1, y1 = path[i-1]
        x2, y2 = path[i]
        distance_travelled += distance((x1, y1), (x2, y2))

        if path_map[y2][x2] == 1:
            tents_supplied.add((x2, y2))
            if len(tents_supplied) == len(total_food):
                break

    return len(tents_supplied), distance_travelled, food_weight

# Function to generate a random path respecting path restrictions
def generate_random_path():
    path = []
    while len(path) < NUM_COORDINATES:
        x = random.randint(0, len(path_map[0]) - 1)
        y = random.randint(0, len(path_map) - 1)
        if path_restrictions[y][x] == 1:
            path.append((x, y))
    return path

# Function to perform crossover between two paths
def crossover(parent1, parent2):
    crossover_point = random.randint(1, NUM_COORDINATES - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# Function to perform mutation on a path
def mutate(path):
    mutated_path = path.copy()
    mutation_point = random.randint(0, NUM_COORDINATES - 1)
    x = random.randint(0, len(path_map[0]) - 1)
    y = random.randint(0, len(path_map) - 1)
    if path_restrictions[y][x] == 1:
        mutated_path[mutation_point] = (x, y)
    return mutated_path

# Genetic algorithm
def genetic_algorithm():
    population = [generate_random_path() for _ in range(POPULATION_SIZE)]

    # Number of people living in each tent
    people_in_tents = {
        (0, 0): {"children": 2, "adults": 3},
        (0, 3): {"children": 0, "adults": 12},
        (0, 4): {"children": 3, "adults": 2},
        (1, 5): {"children": 0, "adults": 4},
        (0, 2): {"children": 1, "adults": 3},
        (4, 5): {"children": 3, "adults": 2},
        (5, 2): {"children": 3, "adults": 2},
        (5, 3): {"children": 1, "adults": 2}
    }

    total_food = total_food_required(people_in_tents)

    for generation in range(NUM_GENERATIONS):
        # Calculate fitness for each individual
        fitness_scores = [calculate_fitness(path, total_food) for path in population]
        max_tents_supplied, _, _ = max(fitness_scores, key=lambda x: x[0])
        best_paths = [path for path, fitness in zip(population, fitness_scores) if fitness[0] == max_tents_supplied]

        # Selection
        selected_parents = random.choices(best_paths, k=POPULATION_SIZE)

        # Crossover and Mutation to create new generation
        new_generation = []
        while len(new_generation) < POPULATION_SIZE:
            parent1, parent2 = random.sample(selected_parents, k=2)
            child = crossover(parent1, parent2)
            if random.random() < 0.5:
                child = mutate(child)
            new_generation.append(child)

        population = new_generation

    return max(best_paths, key=lambda path: calculate_fitness(path, total_food)[0])

# Run the genetic algorithm and get the best path
best_path = genetic_algorithm()
print("Best path:", best_path)
