import random
import numpy as np

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

        state = np.array([x1, x2, x3, x4, x5])
        # Make sure that exactly 150 items is sold (Hard Constraint #2)
        if is150ItemsSold(state):  
            return state

def printIndividualState(state):
    print('\tx1\tx2\tx3\tx4\tx5')
    print('A\t'+'\t'.join(str(num) for num in state[0]))
    print('B\t'+'\t'.join(str(num) for num in state[1]))
    print('C\t'+'\t'.join(str(num) for num in state[2]))
    print('D\t'+'\t'.join(str(num) for num in state[3]))
    print('E\t'+'\t'.join(str(num) for num in state[4]))

def printPopulation(population):
    for individual in population:
        printIndividualState(individual)
        print()

def is150ItemsSold(state):
    return sum(state.flatten()) == 150 




N = 8 # population size
population = [generateRandomIndividual() for _ in range(N)]
printPopulation(population)


# x = generateRandomIndividual()
# print(x)
# print(np.transpose(x))
# printIndividualState(x)
