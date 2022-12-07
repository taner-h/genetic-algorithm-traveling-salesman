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
        print('\tx1\tx2\tx3\tx4\tx5\tTotal')
        print('A\t'+'\t'.join(str(num) for num in self.state[0])+'\t'+str(sum(self.state[0])))
        print('B\t'+'\t'.join(str(num) for num in self.state[1])+'\t'+str(sum(self.state[1])))
        print('C\t'+'\t'.join(str(num) for num in self.state[2])+'\t'+str(sum(self.state[2])))
        print('D\t'+'\t'.join(str(num) for num in self.state[3])+'\t'+str(sum(self.state[3])))
        print('E\t'+'\t'.join(str(num) for num in self.state[4])+'\t'+str(sum(self.state[4])))
        print()


    def calculateF1Bonus(self):
        if self.isAllCitiesVisited(): return 100
        return 0

    def calculatePropertiesFromState(self):
        self.transposed = np.transpose(self.state)
        self.revenueMatrix = self.calculateRevenueMatrix()
        self.revenueMatrixTransposed = np.transpose(self.revenueMatrix)
        self.fbase = self.calculateTotalRevenue()
        self.f1 = self.calculateF1Bonus()
        self.f2 = self.calculateF2Bonus()
        self.f3 = self.calculateF3Bonus()
        self.f = self.fbase + self.f1 + self.f2 + self.f3

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

    def mutate(self):
        temp = np.copy(self.state)
        city = random.choice(range(5))
        items = random.sample(range(5), 2)

        # If the element is to be decreased, make sure that it doesn't go below zerp
        decreaseLimit = self.state[city][items[0]] 
        # If the element is to be increased, make sure that the other element to be decreased doesn't go below zerp
        increaseLimit = self.state[city][items[1]]
        operation = random.choice(['INCREASE', 'DECREASE'])
        if operation == 'INCREASE':
            if not increaseLimit == 0:
                magnitude = random.randint(1, increaseLimit)
                temp[city][items[0]] += magnitude
                temp[city][items[1]] -= magnitude
                self.state = temp
                self.calculatePropertiesFromState()
        else:
            if not decreaseLimit == 0:
                magnitude = random.randint(1, decreaseLimit)
                temp[city][items[0]] -= magnitude
                temp[city][items[1]] += magnitude
                self.state = temp
                self.calculatePropertiesFromState()

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
    print()
    
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
    states = [generateRandomIndividual() for _ in range(INITIAL_SIZE)]
    return [Individual(state) for state in states]

def selection(population):
    fitness = [individual.f for individual in population]
    return random.choices(population, fitness, k=N)

def crossover(population):
    # printPopulationState(population)
    newPopulation = []
    for index in range(N//2):
        # generate the number of item types to interchange/crossover
        count = random.randint(1, 4) 
        # choose the item types that will be exchanged randomly
        itemTypes = random.sample(range(5), count)
   
        temp1 = np.copy(population[index * 2].state)
        temp2 = np.copy(population[index * 2 + 1].state)

        for type in itemTypes:
            temp1[type], temp2[type] = temp2[type].copy(), temp1[type].copy()

        newPopulation.append(Individual(temp1))
        newPopulation.append(Individual(temp2))
    # print('AFTER')
    # printPopulationState(newPopulation)

    return newPopulation

def willMutate():
    return random.choices([True, False], [0.01, 0.98], k=1)

def mutation(population):
    for individual in population:
        if willMutate():
            individual.mutate()

def getBestIndividual(population):
    ordered = sorted(population, key=lambda individual: individual.f, reverse=True)
    global bestF, iterationsSinceBest, bestIndividual, iterationCount
    if ordered[0].f > bestF: 
        bestF = ordered[0].f
        bestIndividual = ordered[0]
        iterationsSinceBest = 0
    else:
        iterationsSinceBest += 1
    iterationCount += 1
    print(f'Best: {bestF}')
    print(f'Best of current iteration: {ordered[0].f}')
    print(f'Iterations: {iterationCount}')
    print(f'Iterations since best f-score: {iterationsSinceBest}')
    print()


def getNBestIndividual(population):
    newPopulation = sorted(population, key=lambda individual: individual.f, reverse=True)
    return newPopulation[:N] 
         
INITIAL_SIZE = 128 # Initial population size
N = 128 # Initial population size
LIMIT = 250
bestF = 0
bestIndividual = None 
iterationsSinceBest = 0
iterationCount = 0
priceMatrix = generatePriceMatrix()

population = getNBestIndividual(initializePopulation())

while iterationsSinceBest < LIMIT:
    selected = selection(population)
    population = crossover(selected)
    getBestIndividual(population)
    mutation(population)
bestIndividual.printProperties()



