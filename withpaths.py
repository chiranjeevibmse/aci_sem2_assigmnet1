import random
import math

def calculate_distance(coord1, coord2):
    # Function to calculate the Euclidean distance between two coordinates
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def fitness(chromosome, locations, path_map, path_restrictions, supplies):
    # Function to calculate the fitness of a distribution plan

    dhal_count, milk_count, flour_count, rice_count, bread_count = supplies

    milk_per_child = 3
    bread_per_child = 1
    flour_per_adult = 3
    rice_per_adult = 3
    dhal_per_adult = 1

    num_commutes = 0
    for i in range(len(chromosome) - 1):
        current_location_idx = chromosome[i]
        current_location = locations[current_location_idx]
        next_location_idx = chromosome[i + 1]
        next_location = locations[next_location_idx]

        # Check if the path is allowed based on path restrictions
        if not path_restrictions[current_location_idx][next_location_idx]:
            # Penalize the fitness score for illegal paths
            num_commutes += 9999
            continue

        num_adults = current_location[current_location_idx][0]
        num_children = current_location[current_location_idx][1]

        required_milk = num_children * milk_per_child
        required_bread = num_children * bread_per_child
        required_flour = num_adults * flour_per_adult
        required_rice = num_adults * rice_per_adult
        required_dhal = num_adults * dhal_per_adult

        while (
            required_milk > 0 or
            required_bread > 0 or
            required_flour > 0 or
            required_rice > 0 or
            required_dhal > 0
        ):
            milk_to_carry = min(milk_count, required_milk)
            bread_to_carry = min(bread_count, required_bread)
            flour_to_carry = min(flour_count, required_flour)
            rice_to_carry = min(rice_count, required_rice)
            dhal_to_carry = min(dhal_count, required_dhal)

            milk_count -= milk_to_carry
            bread_count -= bread_to_carry
            flour_count -= flour_to_carry
            rice_count -= rice_to_carry
            dhal_count -= dhal_to_carry

            required_milk -= milk_to_carry
            required_bread -= bread_to_carry
            required_flour -= flour_to_carry
            required_rice -= rice_to_carry
            required_dhal -= dhal_to_carry

            num_commutes += 1

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

def genetic_algorithm(locations, path_map, path_restrictions, supplies, population_size=50, num_generations=100, mutation_rate=0.2):
    num_locations = len(locations)
    population = [generate_chromosome(locations) for _ in range(population_size)]

    for generation in range(num_generations):
        fitness_scores = [fitness(chromosome, locations, path_map, path_restrictions, supplies) for chromosome in population]
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
        ((3, 2), (0, 0), (0, 0), (12, 0), (2, 3),(0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0),(4, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0),(0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0),(0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0),(3, 2)),
        ((0, 0), (0, 0), (2, 3), (2, 1), (0, 0),(0, 0))
    ]

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

    supplies = [15, 28, 12, 20, 10]

    optimal_distribution_plan = genetic_algorithm(locations, path_map, path_restrictions, supplies)
    print("Optimal Distribution Plan:", optimal_distribution_plan)
