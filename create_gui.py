import numpy as np
import tkinter as tk
import config as c
import stochastic_bandit as sb


def button_function(label_list, bandit_instance, k):
    reward = bandit_instance.pull_arm(k)
    label_list[k]["text"] = "Average reward: "+ str(int(bandit_instance.mean_rewards[k]))+"€"


def create_gui():
    bandit_instance = sb.stochastic_bandit()
    window = tk.Tk()
    greeting = tk.Label(text="Hello, Player!")
    greeting.grid(row=0, column=1)
    label = tk.Label(text="Win the Jackpot!",
                    foreground="white",
                    background="black")
    label.grid(row=1, column=1)
    buttons = []
    labels = []


    for k in np.arange(c.NO_ARMS):
        buttons.append(tk.Button(text="Slot Machine "+str(k+1),
                                 width=25,
                                 height=5,
                                 bg='ForestGreen',
                                 fg="yellow",
                                 command=lambda k=k:button_function(labels, bandit_instance, k)))
        labels.append(tk.Label(text=" ",
                               width=25,
                               height=5,))
        labels[k].grid(row=k+2, column=2)
        buttons[k].grid(row=k+2, column=0)

    window.mainloop()