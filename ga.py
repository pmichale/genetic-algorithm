# ga search
from numpy.random import rand
from numpy.random import randint


# objective function
def onemax(x):
    return -sum(x)


# selection
def selection(pop, scores, k=3):
    # random selection
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        # check if better
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


# crossover
def crossover(p1, p2, r_cross):
    # children are carbon copies of parents (def)
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross:
        # select crossover point
        pt = randint(1, len(p1)-2)
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]


# mutation
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]


# gen alg
def gen_alg(objective, n_bits, n_iter, n_pop, r_cross, r_mut):
    # initial population
    pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
    # keep track of best solution
    best, best_eval = 0, objective(pop[0])
    for gen in range(n_iter):
        # evaluate all candidates in population
        scores = [objective(c) for c in pop]
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print("- %d, new best f(%s) = %.3f" % (gen, pop[i], scores[i]))
        # selection
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # new generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                mutation(c , r_mut)
                children.append(c)
        pop = children
    return [best, best_eval]

n_iter = 100
n_bits = 20
n_pop = 100
r_cross = 0.9
r_mut = 1.0/float(n_bits)
best, score = gen_alg(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)
print('done')
print("f(%s) = %f" % (best, score))
