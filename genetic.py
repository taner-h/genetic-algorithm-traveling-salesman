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


def isAllCitiesVisited(state):
    transposed = np.transpose(state)
    for city in transposed:
        if sum(city) == 0: return False 
    return True 

def calculateF1Bonus(state):
    if isAllCitiesVisited(state): return 100
    return 0

def calculateF2Bonus(state):
    transposed = np.transpose(state)
    revenue = np.transpose(calculateRevenueMatrix(state))
    bonuses = []
    for index, city in enumerate(transposed):
        cityRevenue = sum(revenue[index])
        difference = (max(city) - min(city))
        bonusPercentage = max(20 - difference, 0)
        bonus = bonusPercentage * cityRevenue / 100
        bonuses.append(bonus)
    return bonuses, sum(bonuses)

def calculateF3Bonus(state):
    transposed = np.transpose(state)
    fbase = calculateTotalRevenue(state)
    itemsSoldPerCity = [sum(city) for city in transposed]
    difference = max(itemsSoldPerCity) - min(itemsSoldPerCity)
    bonusPercentage = max(20 - difference, 0)
    bonus = bonusPercentage * fbase / 100 

def generatePriceMatrix():
    return np.array([
        [1,4,6,4,4],
        [3,8,2,5,15],
        [3,12,3,5,5],
        [2,6,10,2,4],
        [10,5,12,6,3],
    ])

def calculateRevenueMatrix(state):
    return state * priceMatrix

def calculateTotalRevenue(state):
    return sum(calculateRevenueMatrix(state).flatten())

N = 8 # population size
population = [generateRandomIndividual() for _ in range(N)]
priceMatrix = generatePriceMatrix()
# printPopulation(population)
print(population[0])
# print(calculateRevenueMatrix(population[0]))
# print(calculateF1Bonus(population[0]))
# print(calculateF2Bonus(population[0]))

calculateF3Bonus(population[0])

# x = generateRandomIndividual()
# print(x)
# print(np.transpose(x))
# printIndividualState(x)
