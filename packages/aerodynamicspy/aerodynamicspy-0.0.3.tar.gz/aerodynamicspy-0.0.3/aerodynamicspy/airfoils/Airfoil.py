import matplotlib.pyplot as plt
import pandas as pd

class Airfoil:

    def __init__(self, Name, x, z):
        self.Name = Name

        Coords = pd.DataFrame
        Coords.x = x
        Coords.z = z
        self.Coords = Coords

    def plot(self):

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(self.Coords.x,self.Coords.z, marker = "o")
        ax.set_aspect('equal')

        ax.set_title(self.Name)
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Z (m)")
        ax.grid()
        plt.show()

