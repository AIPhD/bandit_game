import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
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
    label_list[k]["text"] = str(int(human_agent.mean_rewards[k]))+"€"
    if int(human_agent.arms_pulled_counter[k]) == 1:
        pulled_counted_list[k]["text"] = str(int(human_agent.arms_pulled_counter[k]))
    else:
        pulled_counted_list[k]["text"] = str(int(human_agent.arms_pulled_counter[k]))
    ucb_pot["value"] = ucb_agent.total_reward/2000
    ts_pot["value"] = ts_agent.total_reward/2000
    human_pot["value"] = human_agent.total_reward/2000

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
    
    if ucb_pot["value"] >= 100 or ts_pot["value"] >= 100 or human_pot["value"] >= 100:
        master = Tk()
        master.geometry("200x200")
        #newwindow=Toplevel(master)
        if human_pot["value"] < 100:
            winner_label = tk.Label(master, text="You Lose!", width=13)
            playersad = Image.open(r"images/playersad.jpg")
            playersad = playersad.resize((64,49), Image.ANTIALIAS)
            playersadtk = ImageTk.PhotoImage(playersad)
            #winner_image = tk.Label(newwindow, image=playersadtk)
        elif human_pot["value"] >= 100 and (ucb_pot["value"] >= 100 or ts_pot["value"] >= 100):
            winner_label = tk.Label(master, text="Draw!", width=13)
        elif human_pot["value"] >= 100 and ucb_pot["value"] < 100 or ts_pot["value"] < 100:
            winner_label = tk.Label(master, text="You Win!", width=13)
            playerhappy = Image.open(r"images/playerhappy.gif")
            playerhappy = playerhappy.resize((64,49), Image.ANTIALIAS)
            playerhappytk = ImageTk.PhotoImage(playerhappy)
            #winner_image = tk.Label(newwindow, image=playerhappytk)
        winner_label.grid(row=0, column=0)
        # winner_image.grid(row=1, column=0)
        


def create_gui():
    """Create graphical user interface, inwhich a human can interact with a bandit environment."""
    bandit_instance = sb.StochasticBandit()
    human_agent = sb.InteractingAgent(bandit_instance)
    ucb_agent = sb.InteractingAgent(bandit_instance)
    ts_agent = sb.InteractingAgent(bandit_instance)
    window = tk.Tk()

    ucbhappy = Image.open(r"images/ucbhappy.png")
    ucbhappy = ucbhappy.resize((64,49), Image.ANTIALIAS)
    ucbsad = Image.open(r"images/ucbsad.png")
    ucbsad = ucbsad.resize((64,49), Image.ANTIALIAS)
    ucbhappytk = ImageTk.PhotoImage(ucbhappy)
    ucbsadtk = ImageTk.PhotoImage(ucbsad)
    ucbimage_label = tk.Label(image=ucbhappytk)
    ucbimage_label.grid(row=1, column=4)

    playerhappy = Image.open(r"images/playerhappy.gif")
    playerhappy = playerhappy.resize((64,49), Image.ANTIALIAS)
    playersad = Image.open(r"images/playersad.jpg")
    playersad = playersad.resize((64,49), Image.ANTIALIAS)
    playerhappytk = ImageTk.PhotoImage(playerhappy)
    playersadtk = ImageTk.PhotoImage(playersad)
    playerimage_label = tk.Label(image=playerhappytk)
    playerimage_label.grid(row=1, column=3)


    tshappy = Image.open(r"images/tshappy.png")
    tshappy = tshappy.resize((64,49), Image.ANTIALIAS)
    tssad = Image.open(r"images/tssad.png")
    tssad = tssad.resize((64,49), Image.ANTIALIAS)
    tshappytk = ImageTk.PhotoImage(tshappy)
    tssadtk = ImageTk.PhotoImage(tssad)
    tsimage_label = tk.Label(image=tshappytk)
    tsimage_label.grid(row=1, column=5)

    window['bg'] = "white"
    greeting = tk.Label(text="Hello, Player!",
                        width=13)
    greeting.grid(row=0, column=1)
    label = tk.Label(text="Win the Jackpot!",
                    foreground="white",
                    background="black",
                    width=13,
                    height=3)
    action_label = tk.Label(text="Actions",
                    foreground="white",
                    background="black",
                    width=13,
                    height=3)
    counter_label = tk.Label(text="Times selected",
                    foreground="white",
                    background="black",
                    width=13,
                    height=3)
    reward_label = tk.Label(text="Average Reward",
                    foreground="white",
                    background="black",
                    width=13,
                    height=3)
    action_label.grid(row=2, column=0)
    counter_label.grid(row=2, column=1)
    reward_label.grid(row=2, column=2)
    label.grid(row=1, column=1)
    ucb_pot = ttk.Progressbar(window,
                              orient="vertical",
                              mode='determinate',
                              length=35*c.NO_ARMS)
    ts_pot = ttk.Progressbar(window,
                             orient="vertical",
                             mode='determinate',
                             length=35*c.NO_ARMS)
    ucb_pot.grid(row=3, column=4, rowspan=c.NO_ARMS, ipadx=20, padx=3)#, pady=50)
    ts_pot.grid(row=3, column=5, rowspan=c.NO_ARMS, ipadx=20, padx=3)
    human_pot = ttk.Progressbar(window,
                                orient="vertical",
                                mode="determinate",
                                length=35*c.NO_ARMS)
    human_pot.grid(row=3, column=3, rowspan=c.NO_ARMS, ipadx=20, padx=3)#, pady=50)
    buttons = []
    labels = []
    pulled_counter = []


    for k in np.arange(c.NO_ARMS):
        buttons.append(tk.Button(text="Slot Machine "+str(k+1),
                                 width=13,
                                 height=2,
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
                               width=13,
                               height=2,))
        pulled_counter.append(tk.Label(text="Never selected",
                                       width=13,
                                       height=2))
        labels[k].grid(row=k+3, column=2)
        pulled_counter[k].grid(row=k+3, column=1)
        buttons[k].grid(row=k+3, column=0)

    window.mainloop()
