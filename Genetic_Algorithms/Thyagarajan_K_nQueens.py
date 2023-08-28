import random

def initial_population(population_size, n):
    return [random.sample(range(n), n) for _ in range(population_size)]


def fitness(board):
    attacks = 0
    n = len(board)
    freq_row = [0] * n
    freq_diag1 = [0] * (2 * n)
    freq_diag2 = [0] * (2 * n)

    for i in range(n):
        freq_row[board[i]] += 1
        freq_diag1[i + board[i]] += 1
        freq_diag2[n - board[i] + i] += 1

    for i in range(2*n):
        if i < n:
            attacks += freq_row[i] * (freq_row[i] - 1) / 2
        attacks += freq_diag1[i] * (freq_diag1[i] - 1) / 2
        attacks += freq_diag2[i] * (freq_diag2[i] - 1) / 2

    return attacks




def crossover(parent1, parent2):
    n = len(parent1)
    # child = [-1] * n
    # if random.random() < 0.2:
    #     return random_child(n)
    # for i in range(n):
    #     if parent1[i] == parent2[i]:
    #         child[i] = parent1[i]
    # for i in range(n):
    #     if child[i] == -1:
    #         child[i] = random.choice([parent1[i], parent2[i]])
    # return child
    index = random.randint(0, n - 1)
    child1 = parent1[:index] + parent2[index:]
    child2 = parent2[:index] + parent1[index:]
    return child1, child2


def random_child(n):
    return random.sample(range(n), n)


def mutate(child):
    n = len(child)
    index = random.randint(0, n - 1)
    value = random.randint(0, n - 1)
    child[index] = value
    return child


def radiation(population):
    size = len(population)
    n = len(population[0])
    for i in range(size):
        for _ in range(random.randint(n//10, n//5)):
            population[i] = mutate(population[i])
    return population


def best_solution(population):
    return min(population, key=fitness)


def genetic_algorithm(population_size, n, max_generations):
    population = initial_population(population_size, n)
    gen = 0
    child_count = population_size
    best_so_far = n*(n-1)/2
    same_val = 0
    center_variation = population_size // 20
    for _ in range(max_generations):
        for x in range(child_count):
            center = random.randint(0, len(population) - 1 - center_variation)
            parent1 = population[center]
            parent2 = population[random.randint(center-center_variation, center+center_variation)]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            population.append(child1)
            child2 = mutate(child2)
            population.append(child2)
        population.sort(key=fitness)
        population = population[:population_size]
        gen += 1
        print(f"Generation: {gen}, Best Fitness: {fitness(population[0])}")
        if fitness(population[0]) <= 0:
            break
        if fitness(population[0]) == best_so_far:
            same_val += 1
            if same_val >= 6000*(2.718**(-0.00896*population_size)) + 50:
                print("Radiation")
                population = radiation(population)
                same_val = 0
                population.sort(key=fitness)
                best_so_far = fitness(population[0])
        else:
            best_so_far = fitness(population[0])
            same_val = 0
    return best_solution(population)


def display(solution):
    '''Board is stored as a list with indices 0-len representing the row that each queen is in per column.'''
    result = ""
    dots = "." * len(solution)
    for i in range(len(solution)):
        result += dots[:solution[i]] + "Q" + dots[solution[i] + 1:] + "\n"
    return result

def main():
    num_queens = int(input("Enter the number of queens: "))
    population_size = 80
    solution = genetic_algorithm(population_size, num_queens, 10**6)
    print(display(solution))

if __name__ == "__main__":
    main()