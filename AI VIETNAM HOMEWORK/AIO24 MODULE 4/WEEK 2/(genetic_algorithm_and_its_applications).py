# -*- coding: utf-8 -*-
"""(Genetic Algorithm and Its Applications)

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nteTqq8_lluhphX9-5eHWhv9r8lPI3fr
"""

import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(0)
path = '/content/advertising (1).csv'
def load_data_from_file(path):
    data = np.genfromtxt(path, dtype=None, delimiter=',', skip_header=1)
    features_X = data[:,:3]  # Get first 3 columns (TV, Radio, Newspaper)
    # Add column of 1s for bias term
    ones = np.ones((features_X.shape[0], 1))
    features_X = np.hstack((features_X, ones))
    sales_Y = data[:,3]  # Get last column (Sales)
    return features_X, sales_Y

def create_individual(n=4, bound=10):
    individual = []
    for _ in range(n):
        # Generate random value between -bound/2 and bound/2
        gene = random.uniform(-bound/2, bound/2)
        individual.append(gene)
    return individual

def compute_loss(individual):
    theta = np.array(individual)
    y_hat = features_X.dot(theta)
    loss = np.multiply((y_hat - sales_Y), (y_hat - sales_Y)).mean()
    return loss

def compute_fitness(individual):
    loss = compute_loss(individual)
    fitness_value = 1 / (loss + 1)  # Add 1 to avoid division by zero
    return fitness_value

def crossover(individual1, individual2, crossover_rate=0.9):
    individual1_new = individual1.copy()
    individual2_new = individual2.copy()

    if random.random() < crossover_rate:
        # Select random crossover point
        point = random.randint(1, len(individual1)-1)
        # Swap genes after crossover point
        individual1_new[point:], individual2_new[point:] = individual2_new[point:], individual1_new[point:]

    return individual1_new, individual2_new

def mutate(individual, mutation_rate=0.05):
    individual_m = individual.copy()
    for i in range(len(individual_m)):
        if random.random() < mutation_rate:
            # Add random value between -1 and 1 to the gene
            individual_m[i] += random.uniform(-1, 1)
    return individual_m

def initializePopulation(m):
    population = [create_individual() for _ in range(m)]
    return population

def selection(sorted_old_population, m=100):
    index1 = random.randint(0, m-1)
    while True:
        index2 = random.randint(0, m-1)
        if index2 != index1:
            break

    # Tournament selection - return the better individual
    individual_s = sorted_old_population[index1]
    if index2 > index1:
        individual_s = sorted_old_population[index2]
    return individual_s

def create_new_population(old_population, elitism=2, gen=1):
    m = len(old_population)
    sorted_population = sorted(old_population, key=compute_fitness)
    if gen % 1 == 0:
        print("Best loss:", compute_loss(sorted_population[m-1]), "with chromosome:", sorted_population[m-1])

    new_population = []
    while len(new_population) < m - elitism:
        # Selection
        parent1 = selection(sorted_population, m)
        parent2 = selection(sorted_population, m)

        # Crossover
        child1, child2 = crossover(parent1, parent2)

        # Mutation
        child1 = mutate(child1)
        child2 = mutate(child2)

        new_population.extend([child1, child2])

    # Copy elitism chromosomes
    for ind in sorted_population[m-elitism:]:
        new_population.append(ind.copy())

    return new_population, compute_loss(sorted_population[m-1])

def run_GA():
    n_generations = 100
    m = 600
    global features_X, sales_Y
    features_X, sales_Y = load_data_from_file()

    population = initializePopulation(m)
    losses_list = []

    for i in range(n_generations):
        population, best_loss = create_new_population(population, elitism=2, gen=i)
        losses_list.append(best_loss)

    return losses_list