import random

def generateSoldItemCount(count):
    while True:
        items = [random.random() for _ in range(5)]
        total = sum(items)
         # round() method ensures that elements are natural number (Hard Constraint #1)
        items = [round(count * item / total) for item in items]
        # Make sure sold item amounts is equal to the stock (Hard Constraint #3)
        if sum(items) == count:
            return items

def generateRandomIndividual():
    while True:
        x1 = generateSoldItemCount(30)
        x2 = generateSoldItemCount(40)
        x3 = generateSoldItemCount(20)
        x4 = generateSoldItemCount(40)
        x5 = generateSoldItemCount(20)

        state = x1 + x2 + x3 + x4 + x5

        # Make sure that exactly 150 items is sold (Hard Constraint #2)
        if is150ItemsSold(state):  
            return state

def printIndividualState(state):
    print('\tx1\tx2\tx3\tx4\tx5')
    print('A\t', end='')
    print('\t'.join(str(num) for num in state[:5]))
    print('B\t', end='')
    print('\t'.join(str(num) for num in state[5:10]))
    print('C\t', end='')
    print('\t'.join(str(num) for num in state[10:15]))
    print('D\t', end='')
    print('\t'.join(str(num) for num in state[15:20]))
    print('E\t', end='')
    print('\t'.join(str(num) for num in state[20:]))


def printPopulation(population):
    for individual in population:
        print(individual)
        printIndividualState(individual)
        print()

def is150ItemsSold(state):
    return sum(state) == 150 

def getX1(state):
    return [state[0], state[5], state[10], state[15], state[20]] 

# def isAllCitiesVisited(state):


N = 8 # population size
population = [generateRandomIndividual() for _ in range(N)]
printPopulation(population)

print(getX1(population[7]))


