import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')

class CustomStatsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Your Game Stats Visualization")
        self.geometry("1000x700")

        self.df = pd.read_csv('database.csv')
        self.setup_widgets()

    def setup_widgets(self):
        ttk.Label(self, text="Select Graph", font=("Arial", 14, "bold")).pack(pady=10)

        self.combo = ttk.Combobox(self, state="readonly")
        self.combo['values'] = [
            'Player Attack Count Boxplot',
            'Zombies Killed Scatter Plot',
            'Zombie Type Counts Table',
            'Coins Collected Barplot',
            'Damage Taken Line Plot'
        ]
        self.combo.pack(pady=5)
        self.combo.bind('<<ComboboxSelected>>', self.update_plot)

        ttk.Button(self, text="Quit", command=self.destroy).pack(pady=5)

        self.fig = Figure(figsize=(9, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

    def update_plot(self, event):
        selection = self.combo.get()
        self.ax.clear()

        if selection == 'Player Attack Count Boxplot':
            data = self.df[['player_attack_count(10sec)']]
            sns.boxplot(y=data['player_attack_count(10sec)'], ax=self.ax)
            self.ax.set_yticks(range(0, 80, 20))
            self.ax.set_ylabel('total attack count')
            self.ax.set_title('player attack count every 10sec')

        elif selection == 'Zombies Killed Scatter Plot':
            data = self.df[['zombie_killed(10sec)']].head(51)
            self.ax.scatter(data.index, data['zombie_killed(10sec)'])
            self.ax.set_xticks(range(0, 51, 1))
            self.ax.set_yticks(range(0, 50, 10))
            self.ax.set_ylabel('eliminated amount')
            self.ax.set_title('total zombies killed every 10 sec')

        elif selection == 'Zombie Type Counts Table':
            self.ax.axis('off')
            counts = self.df['zombie_type(10sec)'].value_counts()
            table = self.ax.table(
                cellText=[[k, v] for k, v in counts.items()],
                colLabels=['Zombie Type', 'Count'],
                loc='center',
                cellLoc='center'
            )
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1.2, 1.2)
            self.ax.set_title("Zombie Type Counts (10 sec)", fontsize=14)

        elif selection == 'Coins Collected Barplot':
            data = self.df[['coin_collect(10sec)']].head(50)
            data.index = range(1, 50)
            sns.barplot(x=data.index, y='coin_collect(10sec)', data=data, ax=self.ax)
            self.ax.set_ylabel('total coin collected')
            self.ax.set_xlabel('Survival Time (10seconds)')
            self.ax.set_title('total coin collected within 10 sec')
            self.ax.tick_params(axis='x', rotation=45)

        elif selection == 'Damage Taken Line Plot':
            data = self.df[['damage_taken(10sec)']].head(51)
            self.ax.plot(data.index, data['damage_taken(10sec)'], marker='^', linestyle='-', color='b')
            self.ax.set_yticks(range(0, 200, 20))
            self.ax.set_ylabel('damage received')
            self.ax.set_xticks(range(0, 51, 1))
            self.ax.set_xlabel('time(10sec)')
            self.ax.set_title('total damage player taken every 10sec')
            self.ax.grid(axis='y', linestyle='--')

        self.canvas.draw()

def run_gui():
    app = CustomStatsApp()
    app.mainloop()

run_gui()
