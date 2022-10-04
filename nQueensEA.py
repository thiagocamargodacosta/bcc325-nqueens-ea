import numpy as np
import copy
import math
import statistics as st

def pop_init(k,n):
    return [np.random.permutation(n) for i in range(k)]

def mutation(sol):

    neighbor = copy.copy(sol)

    idx1 = np.random.randint(0,len(sol))
    idx2 = np.random.randint(0,len(sol))

    neighbor[idx1], neighbor[idx2] =  neighbor[idx2], neighbor[idx1] 

    return neighbor

def crossover(sol1,sol2):
    mask = np.random.randint(2, size=len(sol1))

    f1 = copy.copy(sol1)
    for i in range(len(sol1)):
        if mask[i] == 0:
            f1[i] = sol2[i]

    f2 = copy.copy(sol2)
    for i in range(len(sol2)):
        if mask[i] == 0:
            f2[i] = sol1[i]

    return f1,f2

#
#
#

def get_violations_count(sol):

    violations_count = 0

    for i in range(len(sol)):

        for j in range(len(sol)):

            # columns
            if (i != j) and (sol [i] == sol [j]):
                
                violations_count += 1

            # diagonals

            deltay = abs(sol[i] - sol[j])
            deltax = abs(i - j)
            same_diagonal = deltax == deltay

            if same_diagonal:
                
                violations_count += 1

    return violations_count

def nQueens_genetico(initial_pop, epochs=10):

    initial_solutions = initial_pop
    hall_of_fame      = list()
    violations_count  = dict()
    cream_of_the_crop = len(initial_solutions) // 2 + 1

    # create dictionary with solution index as key and violation count as value
    violations_count = evaluate(initial_solutions)

    # get metric for filtering hall of fame individuals
    values        = list(violations_count.values())
    mean_value    = math.floor(st.mean(values))
    
    # build hall of fame

    i = 0

    while len(hall_of_fame) != cream_of_the_crop:

        if violations_count[i] <= mean_value:

            hall_of_fame.append(list(initial_solutions[i]))

        i += 1
    
    # mutate and crossover across epochs

    epoch_counter = 0

    while epoch_counter != epochs:

        # least fit individual will mutate
        least_fit_individual = hall_of_fame[len(hall_of_fame) - 1]
        hall_of_fame[len(hall_of_fame) - 1] = mutation(least_fit_individual) 

        # others will crossover and their children will be appended on hall of fame

        for j in range(0, len(hall_of_fame) - 1, 2):

            child = crossover(hall_of_fame[j], hall_of_fame[j + 1])

            hall_of_fame.append(child)

        epoch_counter += 1

    return hall_of_fame

def evaluate(solutions):

    violations_count = dict()

    for index, solution in enumerate(solutions):

        violations_count[index] = get_violations_count(solution)

    return violations_count


def my_main(verbose=False):

    pop = pop_init(8, 8)

    if verbose:

        for p in pop:
            print(f'pop: {p}')
    
    hall_of_fame = nQueens_genetico(pop)

    if verbose:

        print(f'hall_of_fame: {hall_of_fame}')

if __name__ == '__main__':

    my_main(verbose=True)
