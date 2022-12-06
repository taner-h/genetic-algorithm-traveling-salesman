import random
import numpy as np

class Individual:
    def __init__(self, state):
        self.state = state
        self.transposed = np.transpose(self.state)
        self.revenueMatrix = self.calculateRevenueMatrix()
        self.revenueMatrixTransposed = np.transpose(self.revenueMatrix)
        self.fbase = self.calculateTotalRevenue()
        self.f1 = self.calculateF1Bonus()
        self.f2 = self.calculateF2Bonus()
        self.f3 = self.calculateF3Bonus()
        self.f = self.fbase + self.f1 + self.f2 + self.f3

    def calculateRevenueMatrix(self):
        return self.state * priceMatrix

    def calculateTotalRevenue(self):
        return sum(self.revenueMatrix.flatten())

    def printState(self):
        print('\tx1\tx2\tx3\tx4\tx5')
        print('A\t'+'\t'.join(str(num) for num in self.state[0]))
        print('B\t'+'\t'.join(str(num) for num in self.state[1]))
        print('C\t'+'\t'.join(str(num) for num in self.state[2]))
        print('D\t'+'\t'.join(str(num) for num in self.state[3]))
        print('E\t'+'\t'.join(str(num) for num in self.state[4]))
        print()


    def calculateF1Bonus(self):
        if self.isAllCitiesVisited(): return 100
        return 0

    def calculateF2Bonus(self):
        bonuses = []
        for index, city in enumerate(self.transposed):
            cityRevenue = sum(self.revenueMatrixTransposed[index])
            difference = (max(city) - min(city))
            bonusPercentage = max(20 - difference, 0)
            bonus = bonusPercentage * cityRevenue / 100
            bonuses.append(bonus)
        return sum(bonuses)

    def calculateF3Bonus(self):
        itemsSoldPerCity = [sum(city) for city in self.transposed]
        difference = max(itemsSoldPerCity) - min(itemsSoldPerCity)
        bonusPercentage = max(20 - difference, 0)
        bonus = bonusPercentage * self.fbase / 100 
        return bonus

    def isAllCitiesVisited(self):
        for city in self.transposed:
            if sum(city) == 0: return False 
        return True 

    def printAllProperties(self):
        print('Individual State:')
        self.printState()
        print('Matrix:\n', self.state)
        print('\nTransposed Matrix:\n', self.transposed)
        print('\nRevenue Matrix:\n', self.revenueMatrix)
        print('\nfbase:', self.fbase)
        print('f1:', self.f1)
        print('f2:', self.f2)
        print('f3:', self.f3)
        print('f:', self.f)
        print()

    def printProperties(self):
        print('Individual State:')
        self.printState()
        print('fbase:', self.fbase)
        print('f1:', self.f1)
        print('f2:', self.f2)
        print('f3:', self.f3)
        print('f:', self.f)
        print() 

def printPopulationState(population):
    for individual in population:
        individual.printState()

def printPopulationFitness(population):
    for index, individual in enumerate(population):
        print(f'Individual {index + 1}:  {individual.f}')
    
def printPopulationProperties(population):
    for individual in population:
        individual.printProperties()

def generatePriceMatrix():
    return np.array([
        [1,4,6,4,4],
        [3,8,2,5,15],
        [3,12,3,5,5],
        [2,6,10,2,4],
        [10,5,12,6,3],
    ])

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

def is150ItemsSold(state):
    return sum(state.flatten()) == 150 

def initializePopulation():
    states = [generateRandomIndividual() for _ in range(N)]
    return [Individual(state) for state in states]

def selection(population):
    fitness = [individual.f for individual in population]
    return random.choices(population, fitness, k=N)

def crossover(population):
    newPopulation = []
    for index in range(N//2):
        # generate the number of cities to interchange/crossover
        count = random.randint(1, 4) 
        print(f'count: {count}')
        # choose the cities that will be exchanged randomly
        cities = random.sample(range(5), count)
        print(f'cities: {cities}')
        print('before:')

        population[index * 2].printState()
        population[index * 2 + 1].printState()


        temp1 = np.copy(population[index * 2].transposed)
        temp2 = np.copy(population[index * 2 + 1].transposed)

        for city in cities:
            temp1[city], temp2[city] = temp2[city].copy(), temp1[city].copy()

        newPopulation.append(Individual(np.transpose(temp1)))
        newPopulation.append(Individual(np.transpose(temp2)))
        print('after:')
        newPopulation[index * 2].printState()
        newPopulation[index * 2 + 1].printState()

        # print(np.transpose(temp1))
        # print(np.transpose(temp2))
    return newPopulation


INITIAL_SIZE = 32 # Initial population size
N = 4 # Initial population size
LIMIT = 50
highestFitness = 0
# bestIndividual = 
iterationsSinceBest = 0
priceMatrix = generatePriceMatrix()


population = initializePopulation()
printPopulationState(population)
printPopulationFitness(population)

selection = selection(population)
population = crossover(population)
printPopulationState(population)
printPopulationFitness(population)

# population = initializePopulation(N)
# printPopulationState(population)



