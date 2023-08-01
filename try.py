import random
import math

def calculate_distance(coord1, coord2):
    # Function to calculate the Euclidean distance between two coordinates
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def fitness(chromosome, locations, supplies):
    # Function to calculate the fitness of a distribution plan
    
    # ... (Same as before)

    num_commutes = 0
    for i in range(len(chromosome) - 1):
        current_location = locations[chromosome[i]]
        next_location = locations[chromosome[i + 1]]
        num_commutes += calculate_distance(current_location[0], next_location[0])

    return 1.0 / num_commutes

def generate_chromosome(locations):
    # Function to generate a random chromosome (order of locations)
    chromosome = list(range(len(locations)))
    random.shuffle(chromosome)
    return chromosome

def crossover(parent1, parent2):
    # Function to perform crossover between two parents to create offspring
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

def mutate(chromosome, mutation_rate):
    # Function to apply mutation to a chromosome
    if random.random() < mutation_rate:
        index1, index2 = random.sample(range(len(chromosome)), 2)
        chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
    return chromosome

def genetic_algorithm(locations, supplies, population_size=50, num_generations=100, mutation_rate=0.2):
    num_locations = len(locations)
    population = [generate_chromosome(locations) for _ in range(population_size)]

    for generation in range(num_generations):
        fitness_scores = [fitness(chromosome, locations, supplies) for chromosome in population]
        best_chromosome = population[fitness_scores.index(max(fitness_scores))]
        print(f"Generation {generation}: Best Fitness = {max(fitness_scores)}")

        next_generation = [best_chromosome]

        while len(next_generation) < population_size:
            parent1, parent2 = random.choices(population, weights=fitness_scores, k=2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            next_generation.extend([child1, child2])

        population = next_generation

    return best_chromosome

if __name__ == "__main__":
    locations = [
        ((0, 0), 3, 2),
        ((3, 0), 12,0),
        ((4, 0), 2,3),
        ((5, 1), 4,0),
        ((5, 4), 3,2),
        ((5, 4), 3,2),
        ((2, 6), 2,3),
        ((3, 6), 2,1),
        # Add other location information as needed
    ]

    supplies = [15, 28, 12, 20, 10]

    optimal_distribution_plan = genetic_algorithm(locations, supplies)
    print("Optimal Distribution Plan:", optimal_distribution_plan)
