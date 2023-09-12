import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
import config as c
import stochastic_bandit as sb


def button_function(label_list,
                    pulled_counted_list,
                    ucb_pot,
                    ts_pot,
                    human_pot,
                    human_agent,
                    ucb_agent,
                    ts_agent,
                    player_image_label,
                    ucb_image_label,
                    ts_image_label,
                    player_images,
                    ucb_images,
                    ts_images,
                    k):
    """Define what happens when a human player presses a Button."""
    human_agent.select_action(k)
    ucb_agent.ucb_policy()
    ts_agent.ts_policy()
    label_list[k]["text"] = "Average reward: "+ str(int(human_agent.mean_rewards[k]))+"€"
    if int(human_agent.arms_pulled_counter[k]) == 1:
        pulled_counted_list[k]["text"] = "Selected " + str(int(human_agent.arms_pulled_counter[k])) + " time"
    else:
        pulled_counted_list[k]["text"] = "Selected " + str(int(human_agent.arms_pulled_counter[k])) + " times"
    ucb_pot["value"] = ucb_agent.total_reward/5000
    ts_pot["value"] = ts_agent.total_reward/5000
    human_pot["value"] = human_agent.total_reward/5000

    if ucb_agent.total_reward > human_agent.total_reward and ucb_agent.total_reward > ts_agent.total_reward:
        ucb_image_label.configure(image=ucb_images[0])
        ts_image_label.configure(image=ts_images[1])
        player_image_label.configure(image=player_images[1])
    else:
        ucb_image_label.configure(image=ucb_images[1])

        if ts_agent.total_reward > human_agent.total_reward:
            ts_image_label.configure(image=ts_images[0])
            player_image_label.configure(image=player_images[1])
        else:
            ts_image_label.configure(image=ts_images[1])
            player_image_label.configure(image=player_images[0])


def create_gui():
    """Create graphical user interface, inwhich a human can interact with a bandit environment."""
    bandit_instance = sb.StochasticBandit()
    human_agent = sb.InteractingAgent(bandit_instance)
    ucb_agent = sb.InteractingAgent(bandit_instance)
    ts_agent = sb.InteractingAgent(bandit_instance)
    window = tk.Tk()

    ucbhappy = Image.open(r"images/ucbhappy.png")
    ucbhappy = ucbhappy.resize((128,97), Image.ANTIALIAS)
    ucbsad = Image.open(r"images/ucbsad.png")
    ucbsad = ucbsad.resize((128,97), Image.ANTIALIAS)
    ucbhappytk = ImageTk.PhotoImage(ucbhappy)
    ucbsadtk = ImageTk.PhotoImage(ucbsad)
    ucbimage_label = tk.Label(image=ucbhappytk)
    ucbimage_label.grid(row=1, column=4)

    playerhappy = Image.open(r"images/playerhappy.gif")
    playerhappy = playerhappy.resize((128,97), Image.ANTIALIAS)
    playersad = Image.open(r"images/playersad.jpg")
    playersad = playersad.resize((128,97), Image.ANTIALIAS)
    playerhappytk = ImageTk.PhotoImage(playerhappy)
    playersadtk = ImageTk.PhotoImage(playersad)
    playerimage_label = tk.Label(image=playerhappytk)
    playerimage_label.grid(row=1, column=3)


    tshappy = Image.open(r"images/tshappy.png")
    tshappy = tshappy.resize((128,97), Image.ANTIALIAS)
    tssad = Image.open(r"images/tssad.png")
    tssad = tssad.resize((128,97), Image.ANTIALIAS)
    tshappytk = ImageTk.PhotoImage(tshappy)
    tssadtk = ImageTk.PhotoImage(tssad)
    tsimage_label = tk.Label(image=tshappytk)
    tsimage_label.grid(row=1, column=5)

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
    ucb_pot = ttk.Progressbar(window,
                              orient="vertical",
                              mode='determinate',
                              length=80*c.NO_ARMS)
    ts_pot = ttk.Progressbar(window,
                             orient="vertical",
                             mode='determinate',
                             length=80*c.NO_ARMS)
    ucb_pot.grid(row=2, column=4, rowspan=c.NO_ARMS, ipadx=30, padx=3)#, pady=50)
    ts_pot.grid(row=2, column=5, rowspan=c.NO_ARMS, ipadx=30, padx=3)
    human_pot = ttk.Progressbar(window,
                                orient="vertical",
                                mode="determinate",
                                length=80*c.NO_ARMS)
    human_pot.grid(row=2, column=3, rowspan=c.NO_ARMS, ipadx=30, padx=3)#, pady=50)
    buttons = []
    labels = []
    pulled_counter = []


    for k in np.arange(c.NO_ARMS):
        buttons.append(tk.Button(text="Slot Machine "+str(k+1),
                                 width=25,
                                 height=5,
                                 bg='ForestGreen',
                                 fg="yellow",
                                 command=lambda k=k:button_function(labels,
                                                                    pulled_counter,
                                                                    ucb_pot,
                                                                    ts_pot,
                                                                    human_pot,
                                                                    human_agent,
                                                                    ucb_agent,
                                                                    ts_agent,
                                                                    playerimage_label,
                                                                    ucbimage_label,
                                                                    tsimage_label,
                                                                    [playerhappytk,playersadtk],
                                                                    [ucbhappytk,ucbsadtk],
                                                                    [tshappytk,tssadtk],
                                                                    k)))
        labels.append(tk.Label(text=" ",
                               width=25,
                               height=5,))
        pulled_counter.append(tk.Label(text="Never selected",
                                       width=25,
                                       height=5))
        labels[k].grid(row=k+2, column=2)
        pulled_counter[k].grid(row=k+2, column=1)
        buttons[k].grid(row=k+2, column=0)

    window.mainloop()
