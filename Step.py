import os
from model.State import State
from solver.CSP import Backtracking
from solver.HillClimping import HC
from solver.KBeam import Beam
from utils.IO import IO
from solver.GeneticAlgorithm import GA

Dimension = 8  # For N-Queen problem here N=8
result = IO('test/Sample_Input.txt')
board = result.readFile()
initialSate = State(board)

# ga = GA(500,Dimension,3) #parameters: population size , Dimension of board, crossover (Hint:random start)
# ga.start()
# ga.report()

# using initial State, Dimension of board,to restart algorithm till solve set True
hc = HC(initialSate, Dimension, False)
hc.start()
board, finalBoard = hc.report()
result.writeFile(finalBoard)

# csp = Backtracking(Dimension)#parameters: Dimension of board (Hint:random start)
# csp.start()
# csp.report()

# k = Beam(8,Dimension) #parameters: value of K, Dimension of board (Hint:random start)
# k.start()
# k.report()
