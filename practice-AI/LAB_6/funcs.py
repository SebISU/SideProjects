import numpy as np
import random
import sys
from math import sqrt
from datetime import datetime


def genetic_1(population, mutation_prob, many_generations=1):
    '''Return the best pair from population by amount of ones. LAB_6_1

        population = size of population
        mutation_prob = mutation probability
        many_generations = how many generation cycles to do
    '''

    generation = []

    for x in range(population):

        chromosome  = 0
        i = 0
        for y in range(10):

            LSB = random.randint(0, 1)
            chromosome |= LSB

            if LSB == 1:
                i += 1

            if y < 9:
                chromosome <<= 1
        
        generation.append((chromosome, i))

    for x in range(many_generations):

        generation.sort(key = lambda x: x[1], reverse=True)
        
        i = random.randint(0, 10)
        new_1, new_2 = 0, 0
        ones_1, ones_2 = 0, 0

        for y in range(10):
            
            if y >= i:
                a1 = ((generation[1][0] >> y) & 1)
                a2 = ((generation[0][0] >> y) & 1)

            else:
                a1 = ((generation[0][0] >> y) & 1)
                a2 = ((generation[1][0] >> y) & 1)

            if a1 == 1:
                ones_1 += 1
            if a2 == 1:
                ones_2 += 1

            new_1 |= a1 << y
            new_2 |= a2 << y

        generation[-1] = (new_2, ones_2)
        generation[-2] = (new_1, ones_1)

        for a in range(2):

            i = random.random()

            if i <= mutation_prob:

                index = random.randint(0, 9)
                if ((generation[a][0] >> index) & 1) == 1:
                    generation[a] = (generation[a][0] ^ (1 << index), generation[a][1] - 1)
                else:
                    generation[a] = (generation[a][0] ^ (1 << index), generation[a][1] + 1)

    generation.sort(key = lambda x: x[1], reverse=True)

    return [bin(gen[0]) for gen in generation[0:2]]


def genetic_2(population, mutation_prob, expected_result, many_generations=1):
    '''Return a generation list with mismatch for each value. LAB_6_2

        population = size of population
        mutation_prob = mutation probability
        expected_result = expected function result
        many_generations = how many generation cycles
    '''


    # create a list of values
    generation = []

    for x in range(population):

        chromosome  = 0
        for y in range(8):

            LSB = random.randint(0, 1)
            chromosome |= LSB

            if y < 7:
                chromosome <<= 1
        
        generation.append(chromosome)

    # create new generations
    for x in range(many_generations):

        deltas = [abs(expected_result - (2 * ((gen >> 4) ** 2) + (gen & 15))) for gen in generation]

        delta_without_equal = sum(deltas)

        likelyhood = [0]

        # list for roulette selection
        for delta in deltas:

            if delta == 0:

                likelyhood.append(likelyhood[-1] + 2 * delta_without_equal)
            else:
                likelyhood.append(likelyhood[-1] + delta_without_equal/delta)

        new_generation = []

        # create a new genereation using the roulette list

        # In a real genentic algoritms should be a likelyhood
        # actualization and a member removal from generation
        # list after each choice. You can't simply copy
        # x times the same item because it has the highest probability.
        # You can't create a new member from pair like father1xfather1
        # because he has the best coefficients
        # works only when you want to select a smaller population than actual one
        for y in range(population):

            rand_val = random.uniform(0.0, likelyhood[-1])

            for a in range(len(likelyhood)-1):

                if likelyhood[a] <= rand_val <= likelyhood[a+1]:
                    break

            new_generation.append(generation[a])

        random.shuffle(new_generation)
        generation = new_generation

        # crossing on 50% members
        many = population

        if many % 2 != 0:
            many -= 1

        if many % 4 != 0:
            many -= 2


        for a in range(0, many, 2):

            i = random.randint(0, 8)
            new_1 = 0

            for y in range(8):
                
                if y >= i:

                    new_1 |= ((generation[a] >> y) & 1) << y

                else:

                    new_1 |= ((generation[a+1] >> y) & 1) << y

            i = random.randint(0, 1)

            generation[a+i] = new_1

        # mutation on mutation_prob of list values
        for a in range(population):

            if random.random() <= mutation_prob:

                index = random.randint(0, 7)
                generation[a] = generation[a] ^ (1 << index)

    return list(zip(generation, [ '{0:08b}'.format(gen) for gen in generation], [abs(expected_result - (2 * ((gen >> 4) ** 2) + (gen & 15))) for gen in generation]))


def genetic_3(population, mutation_prob, elitarism_level, max_weight, many_generations=1):
    '''Return a generation list with price for each value. LAB_6_3

        population = size of population
        mutation_prob = mutation probability
        elitarism_level = what % of the best members in the next generation
        max_weight = max backpack weigth
        many_generations = how many generation cycles
    '''

    inventory = {0:(3, 266), 1:(13, 442), 2:(10, 671), 3:(9, 526),
                4:(7, 388), 5:(1, 245), 6:(8, 210),
                7:(8, 145), 8:(2, 126), 9:(9, 322)}

    # create a list of values
    generation = []

    for x in range(population):

        chromosome  = 0
        for y in range(10):

            LSB = random.randint(0, 1)
            chromosome |= LSB

            if y < 9:
                chromosome <<= 1
        
        generation.append(chromosome)

    # create new generations

    #calculate a backpack's weight and price
    bp_price_weight = backpack_price_weight_helper_3(generation, inventory)

    fitness = [i if j <= max_weight else 0 for i, j in bp_price_weight]
    
    generation = list(zip(generation, fitness))

    for x in range(many_generations):

        fitness_sum = sum(fitness)

        likelyhood = [0]

        # list for roulette selection
        for fit in fitness:

            if fit == 0:

                likelyhood.append(likelyhood[-1])
            else:
                likelyhood.append(likelyhood[-1] + fit/fitness_sum)

        new_generation = []

        # create a new genereation using the roulette list
        for y in range(population):

            rand_val = random.uniform(0.0, likelyhood[-1])

            for a in range(len(likelyhood)-1):

                if likelyhood[a] <= rand_val <= likelyhood[a+1]:
                    break

            new_generation.append(generation[a])

        # crossing generation
        for a in range(0, population, 2):

            i = random.randint(0, 10)
            new_1, new_2 = 0, 0

            for y in range(10):
            
                if y >= i:

                    new_1 |= ((new_generation[a+1][0] >> y) & 1) << y
                    new_2 |= ((new_generation[a][0] >> y) & 1) << y
                else:

                    new_1 |= ((new_generation[a][0] >> y) & 1) << y
                    new_2 |= ((new_generation[a+1][0] >> y) & 1) << y

            new_generation[a] = new_2
            new_generation[a+1] = new_1

        if population % 2 != 0:
            new_generation[-1] = new_generation[-1][0]

        # mutation on mutation_prob of list values
        for a in range(population):

            if random.random() <= mutation_prob:

                index = random.randint(0, 9)
                new_generation[a] = new_generation[a] ^ (1 << index)

        # calculate fitness for the new generation
        bp_price_weight = backpack_price_weight_helper_3(new_generation, inventory)
        fitness = [i if j <= max_weight else 0 for i, j in bp_price_weight]
        new_generation = list(zip(new_generation, fitness))

        # copy members by elitarism
        new_generation.sort(key = lambda x: x[1])
        generation.sort(key = lambda x: x[1], reverse=True)

        for a in range(int(population * elitarism_level)):
            new_generation[a] = generation[a]

        generation = new_generation

    return [(gen[0], '{0:010b}'.format(gen[0]), gen[1]) for gen in generation]


def backpack_price_weight_helper_3(generation, inventory):
    '''Calculate a backpack's weight and price (proxy for LAB_6_3)

        generation = list of generation values
        inventory = dict of possible items
    '''

    backpack_price = []
    backpack_weight = []

    for gen in generation:

        backpack_item_price = [0]
        backpack_item_weight = [0]

        for a in range(10):

            if ((gen >> a) & 1) == 1:

                backpack_item_price.append(inventory[a][1])
                backpack_item_weight.append(inventory[a][0])

        backpack_price.append(sum(backpack_item_price))
        backpack_weight.append(sum(backpack_item_weight))

    return list(zip(backpack_price, backpack_weight))
    

def genetic_4(population, mutation_prob, elitarism_level, many_generations=1):
    '''Return a generation list with a total length for each value. LAB_6_4

        population = size of population
        mutation_prob = mutation probability
        elitarism_level = what % of the best members in the next generation
        many_generations = how many generation cycles

        the shortest path length => 836.4117
    '''

    cities = {0:(119, 38), 1:(37, 38), 2:(197, 55), 3:(85,165),
                4:(12, 50), 5:(100, 53), 6:(81, 142),
                7:(121, 137), 8:(85, 145), 9:(80, 197),
                10:(91, 176), 11:(106, 55), 12:(123, 57),
                13:(40,81), 14:(78, 125), 15:(190, 46),
                16:(187, 40), 17:(37, 107), 18:(17, 11),
                19:(67, 56), 20:(78, 133), 21:(87, 23),
                22:(184, 197), 23:(111, 12), 24:(66, 178)}

    # create a list of values
    generation = []

    for x in range(population):

        chromosome  = 0
        values = [a for a in range(25)]
        random.shuffle(values)

        for y in range(25):


            chromosome |= values.pop()

            if y < 24:
                chromosome <<= 5
        
        generation.append(chromosome)

    # create new generations

    #calculate a total road length
    total_lengths = total_legth_helper_4(generation, cities)
    
    generation = list(zip(generation, total_lengths))

    for x in range(many_generations):

        total_lengths_sum = sum(total_lengths)

        likelyhood = [0]

        # list for roulette selection
        for length in total_lengths:

            if length == 0:

                likelyhood.append(likelyhood[-1])
            else:
                likelyhood.append(likelyhood[-1] + total_lengths_sum/length)

        new_generation = []

        # create a new generation using the roulette list
        for y in range(population):

            rand_val = random.uniform(0.0, likelyhood[-1])

            for a in range(len(likelyhood)-1):

                if likelyhood[a] <= rand_val <= likelyhood[a+1]:
                    break

            new_generation.append(generation[a])

        # crossing generation
        for a in range(0, population, 2):

            i = random.randint(0, 25)

            if i == 25:
                temp = new_generation[a][0]
                new_generation[a] = new_generation[a+1][0]
                new_generation[a+1] = temp
    
            else:
                j = random.randint(i+1, 25)
                new_1, new_2 = 0, 0

                values1 = []
                values2 = []

                for b in range(24, -1, -1):
                    values1.append((new_generation[a][0] >> (5*b)) & 31) 
                    values2.append((new_generation[a+1][0] >> (5*b)) & 31)

                values_after_1 = values2[j:] + values2[:j]
                values_after_2 = values1[j:] + values1[:j]

                for b, c in zip(values2[i:j], values1[i:j]):
                    values_after_1.pop(values_after_1.index(c))
                    values_after_2.pop(values_after_2.index(b))

                values_after_1 = values_after_1[25-j:] + values1[i:j] + values_after_1[:25-j]
                values_after_2 = values_after_2[25-j:] + values2[i:j] + values_after_2[:25-j]

                for b in range(25):

                    new_1 |= values_after_1[b]
                    new_2 |= values_after_2[b]

                    if b < 24:
                        new_1 <<= 5
                        new_2 <<= 5

                new_generation[a] = new_1
                new_generation[a+1] = new_2

        if population % 2 != 0:
            new_generation[-1] = new_generation[-1][0]

        # mutation on mutation_prob of list values
        for a in range(population):

            if random.random() <= mutation_prob:

                index = random.randint(0, 23)
                temp1 = (new_generation[a] >> (5*(index+1))) & 31
                temp2 = (new_generation[a] >> (5*index)) & 31
                new_generation[a] &= ~(31 << (5*index))
                new_generation[a] &= ~(31 << (5*(index+1)))
                new_generation[a] |= (temp1 << (5*index))
                new_generation[a] |= (temp2 << (5*(index+1)))

        # calculate total length for the new generation
        total_lengths = total_legth_helper_4(new_generation, cities)
        new_generation = list(zip(new_generation, total_lengths))

        # copy members by elitarism
        new_generation.sort(key = lambda x: x[1], reverse=True)
        generation.sort(key = lambda x: x[1])

        for a in range(int(population * elitarism_level)):
            new_generation[a] = generation[a]

        generation = new_generation

    return [([((gen[0] >> (5*a)) & 31) for a in range(24, -1, -1)], gen[1]) for gen in generation]


def total_legth_helper_4(generation, cities):
    '''Calculate a road length for each in generation (proxy for LAB_6_4)

        generation = list of generation values
        cities = dict of cities' coefficients

    '''

    road_lengths = []

    for gen in generation:

        road = []

        for a in range(24):

            value1 = (gen >> (a*5)) & 31
            value2 = (gen >> ((a+1)*5)) & 31

            road.append(sqrt((cities[value1][0] - cities[value2][0]) ** 2 + (cities[value1][1] - cities[value2][1]) ** 2))

        value1 = gen & 31
        road.append(sqrt((cities[value1][0] - cities[value2][0]) ** 2 + (cities[value1][1] - cities[value2][1]) ** 2))

        road_lengths.append(sum(road))

    return road_lengths
