import numpy as np
import tkinter as tk
import config as c
import create_gui as cg
from  matplotlib.colors import LinearSegmentedColormap
cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256) 


def main():

    cg.create_gui()




if __name__ == '__main__':
    main()