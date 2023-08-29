import tkinter as tk
import numpy as np
import config as c
import stochastic_bandit as sb


def button_function(label_list, ai_label, human_label, human_agent, ai_agent, k):
    """Define what happens when a human player presses a Button."""
    human_agent.select_action(k)
    ai_agent.ucb_policy()
    label_list[k]["text"] = "Average reward: "+ str(int(human_agent.mean_rewards[k]))+"€"
    ai_label["text"] = "AI Profit: " + str(int(ai_agent.total_reward)) + "€"
    human_label["text"] = "Your Profit: " + str(int(human_agent.total_reward)) + "€"


def create_gui():
    """Create graphical user interface, inwhich a human can interact with a bandit environment."""
    bandit_instance = sb.StochasticBandit()
    human_agent = sb.InteractingAgent(bandit_instance)
    ai_agent = sb.InteractingAgent(bandit_instance)
    window = tk.Tk()
    window['bg'] = "white"
    greeting = tk.Label(text="Hello, Player!",
                        width=25)
    greeting.grid(row=0, column=1)
    label = tk.Label(text="Win the Jackpot!",
                    foreground="white",
                    background="black",
                    width=25,
                    height=5)
    label.grid(row=1, column=1)
    ai_pot = tk.Label(text="AI Profit:",
                      foreground="black",
                      background="white",
                      width=25,
                      height=5)
    ai_pot.grid(row=6, column=4)
    human_pot = tk.Label(text="Your Profit:",
                         foreground="black",
                         background="white",
                         width=25,
                         height=5)
    human_pot.grid(row=6, column=5)
    buttons = []
    labels = []


    for k in np.arange(c.NO_ARMS):
        buttons.append(tk.Button(text="Slot Machine "+str(k+1),
                                 width=25,
                                 height=5,
                                 bg='ForestGreen',
                                 fg="yellow",
                                 command=lambda k=k:button_function(labels,
                                                                    ai_pot,
                                                                    human_pot,
                                                                    human_agent,
                                                                    ai_agent,
                                                                    k)))
        labels.append(tk.Label(text=" ",
                               width=25,
                               height=5,))
        labels[k].grid(row=k+2, column=2)
        buttons[k].grid(row=k+2, column=0)

    window.mainloop()
