import nashpy
import numpy as np

A = np.array([[3,2], [4,0]])
B = np.array([[3,4], [2,0]])

game = nashpy.Game(A, B)

equilibria = game.support_enumeration()
for eq in equilibria:
    print(eq)