from copy import deepcopy
from random import shuffle
from random import randint as rand
from time import time

from termcolor import colored

from model.State import State


class GA:
    def __init__(self,population, dimension, crossover):
        self.generationNumber = 1
        self.pSize=population
        self.d=dimension
        self.co=crossover
        self.environment=list()
        self.solved=False
        self.solution=None
        self.un=list()
        self.minCosts = list()
        self.runningTime=0
        self.expandedNodes=population

    def start(self):
        start = time()
        self.initializeEnvironmnt()
        self.checkGoal()
        while not self.solved:
            self.generationNumber+=1
            chroms=self.crossOver()
            self.updateEnvironment()
            self.checkGoal()
        end=time()
        self.runningTime=end-start
        if len(self.un)!=0:
            self.expandedNodes = len(self.un)





    def initializeEnvironmnt(self):
        for i in range(self.pSize):
            chrom = list(range(self.d))
            shuffle(chrom)
            while chrom in self.environment:
                shuffle(chrom)
            self.environment.append(chrom)

    def checkGoal(self):
        for chrom in self.environment:
            state=State(chrom)
            #print(chrom,">>",state.cost,">>",len(self.un),">>",self.generationNumber)
            if(state.cost==0):
                self.solved = True
                self.solution=chrom

    def crossOver(self):
        for i in range(0,len(self.environment)-1,2):
            chrom1 = self.environment[i][:]
            chrom2 = self.environment[i+1][:]
            chromo1=chrom1[0:self.co]+chrom2[self.co:]
            chromo2=chrom2[0:self.co]+chrom1[self.co:]
            self.mutant(chromo1)
            self.mutant(chromo2)

    def mutant(self, param):
        choice = rand(0,3)
        if choice ==0:
            self.mutantZero(param)
        elif choice ==1:
            self.mutantOne(param)
        elif choice ==2:
            self.mutantTwo(param)
        # elif choice ==3:
        #     self.mutantThree(param)

    def updateEnvironment(self):
        for chrom in self.environment:
            if chrom not in self.un:
                self.un.append(chrom)
        self.minCosts=list()
        costs = list()
        newEnvironment = list()
        for chrom in self.environment:
            state=State(chrom)
            costs.append(state.cost)
        if min(costs) == 0:
            self.solution = costs.index(min(costs))
            self.goal = self.environment[self.solution]
            return self.environment
        while len(newEnvironment) < self.d:
            minCost = min(costs)
            minIndex = costs.index(minCost)
            self.minCosts.append(costs[minIndex])
            newEnvironment.append(self.environment[minIndex])
            costs.remove(minCost)
            self.environment.remove(self.environment[minIndex])
        self.environment=newEnvironment
        print(self.minCosts,">>",len(self.un))

    def report(self):
        print("Running Time : ",self.runningTime,"s")
        print("Number of generations : ",self.generationNumber)
        print("Number of Expanded Nodes : ",self.expandedNodes)
        print("The Solution >> ",self.solution)
        print("The Final State\n")
        self.constructBoard()
        print("= = = = = = = = = = = = = = = = = = = =")

    def constructBoard(self):
        for i in range(0,len(self.solution)):
            temp = ['#'] * self.d
            index = self.solution.index(i)
            temp[index]='Q'
            for j in range(len(temp)):
                if temp[j] == 'Q':
                    print(colored(temp[j], self.getColor(j,self.solution)), end=" ")
                else:
                    print(temp[j], end=" ")
            print()

    def mutantZero(self, param):
        bound = self.d // 2
        leftIndex = rand(0, bound)
        RightIndex = rand(bound + 1, self.d - 1)
        newGen = []
        for dna in param:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.d):
            if i not in newGen:
                newGen.append(i)
        gen = newGen
        gen[leftIndex] = gen[RightIndex]
        gen[RightIndex] = gen[leftIndex]
        self.environment.append(gen)

    def mutantOne(self, param):
        newGen = []
        for dna in param:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.d):
            if i not in newGen:
                newGen.append(i)
        gen = newGen
        for i in range(0,len(gen),2):
            temp=deepcopy(gen[i])
            gen[i]=gen[i+1]
            gen[i+1]=temp
        self.environment.append(gen)
    def mutantTwo(self, param):
        bound = self.d // 2
        leftIndex = rand(0, bound)
        RightIndex = rand(bound + 1, self.d - 1)
        newGen = []
        for dna in param:
            newGen.append(dna)
        gen = newGen
        gen[leftIndex] = gen[RightIndex]
        gen[RightIndex] = gen[leftIndex]
        self.environment.append(gen)

    def mutantThree(self, param):
        newGen = []
        for dna in param:
            newGen.append(dna)
        gen = newGen
        while gen not in self.environment:
            print(gen,len(self.environment))
            shuffle(gen)
        self.environment.append(gen)

    def getColor(self, j, board):
        for col in range(len(board)):
            if col != j:
                if self.isThreaten(board[j], j, board[col], col):
                    return "red"

        return "green"

    def isThreaten(self, i, param, j, param1):
        if i == j:
            return True
        if param == param1:
            return True
        if abs(i - j) == abs(param1 - param):
            return True
        return False





