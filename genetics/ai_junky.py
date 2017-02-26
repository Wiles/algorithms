#
# Based on AI Junkie tutorial
# http://www.ai-junkie.com/ga/intro/gat1.html
#

import random
import argparse

gene_pool_bin = {
    '0000': '0',
    '0001': '1',
    '0010': '2',
    '0011': '3',
    '0100': '4',
    '0101': '5',
    '0110': '6',
    '0111': '7',
    '1000': '8',
    '1001': '9',
    '1010': '+',
    '1011': '-',
    '1100': '*',
    '1101': '/',
    '1110': '',
    '1111': ''
}

gene_pool_grey = {
    '0000': '0',
    '0001': '1',
    '0011': '2',
    '0010': '3',
    '0110': '4',
    '0111': '5',
    '0101': '6',
    '0100': '7',
    '1100': '8',
    '1101': '9',
    '1111': '+',
    '1110': '-',
    '1010': '*',
    '1011': '/',
    '1001': '',
    '1000': ''
}

gene_pool = gene_pool_grey

class WinnerException(Exception):
    pass

def decode(chromosome):
    raw = ''.join(list(map(lambda x: gene_pool[x], list(map(''.join, zip(*[iter(chromosome)]*4))))))
    filtered = ''
    prev_type = 'op'
    for x in raw:
        if x.isdigit():
            if prev_type == 'op':
                filtered += x
                prev_type = 'num'
        else:
            if prev_type == 'num':
                filtered += x
                prev_type = 'op'
    if not raw[-1:].isdigit():
        filtered = filtered[:-1]
    return filtered


def calculate(expression):
    i = 1
    value = int(expression[0])
    try:
        while i < len(expression):
            if expression[i] == '+':
                value += int(expression[i + 1])
            elif expression[i] == '-':
                value -= int(expression[i + 1])
            elif expression[i] == '/':
                value /= int(expression[i + 1])
            elif expression[i] == '*':
                value *= int(expression[i + 1])
            i += 2
        return value
    except:
        return float('inf')


def fitness(goal, chromosome):
    expression = decode(chromosome)
    value = calculate(expression)

    try:
        return abs(1.0 / (goal - value))
    except OverflowError:
        return float('inf')
    except:
        raise WinnerException(f'Winner: {expression}, {value}')

def select(results):
    total = sum(list(map(lambda x: x[0], results)))
    pick = random.uniform(0, total)
    current = 0

    for r in results:
        current += r[0]
        if current >= pick:
            return r[1]

def crossover(rate, population, chromosomes):
    children = []
    while len(children) < population:

        first = select(chromosomes)
        second = select(chromosomes)

        if random.random() <= rate:
            split = random.randrange(0, len(first) -1)
            children.append(first[:split] + second[split:])
            children.append(second[:split] + first[split:])
        else:
            children.append(first)
            children.append(second)


    return children

def print_generation(goal, genes, generation):
    for c in generation:
        try:
            print(f'{decode(c).ljust(genes)}, {calculate(decode(c))}')
        except:
            print(f'{decode(c).ljust(genes)}, {calculate(decode(c))}')

def mutate(rate, chromosomes):
    def x (a):
        def y (b):
            if (random.random() <= rate):
                if (b == '0'):
                    return '1'
                else:
                    return '0'
            else:
                return b
        return ''.join(list(map(y,a)))
    return list(map(x, chromosomes))


def main(population, goal, crossover_rate, mutation_rate, genes):
    chromosomes = []

    for x in range(0, population):
        chromosome = ''
        for y in range(0, genes):
            chromosome += list(gene_pool.keys())[random.randrange(len(gene_pool) - 1)]
        chromosomes.append(chromosome)
    try:
        generation = 0
        while True:
            if generation % 1 == 0:
                print(generation)
                print_generation(goal, genes, chromosomes)

            results = list(map(lambda x: [fitness(goal, x), x], chromosomes))

            chromosomes = crossover(crossover_rate, population, results)

            chromosomes = mutate(mutation_rate, chromosomes)

            generation += 1
    except WinnerException as e:
        print(generation)
        print(e)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Evolve some equations.')
    parser.add_argument('population', type=int, help='population of each generation')
    parser.add_argument('goal', type=int, help='evolution goal value')
    parser.add_argument('crossover', type=float, help='rate of evolutionary crossover')
    parser.add_argument('mutation', type=float, help='rate of evolutionary mutation')
    parser.add_argument('genes', type=int, help='number of genes in each chromosome')

    args = parser.parse_args()

    main(args.population, args.goal, args.crossover, args.mutation, args.genes)


