import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# idea taken from stackoverflow answer by ljetibo
# https://stackoverflow.com/questions/36636185/is-it-possible-for-python-to-display-latex-in-real-time-in-a-text-box


class pretty_math(tk.Frame):
    def __init__(self, math_text, *args):
        super().__init__(*args)
        self.math_text = math_text
        label = tk.Label(self, font=('Computer Modern Roman', 12))
        label.pack()
        fig = matplotlib.figure.Figure(figsize=(4, 2), dpi=100)
        self.ax = fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(fig, master=label)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.canvas._tkcanvas.pack(side="top", fill="both", expand=True)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.graph()

    def graph(self, event=None):
        tmptext = "$"+self.math_text+"$"

        self.ax.clear()
        # for item in self.ax.__dir__():
        #     print(item)
        print(self.ax.get_ylim())
        self.ax.text(0.0, 0.5, tmptext, fontsize=12, math_fontfamily='cm')
        self.canvas.draw()

if __name__ == '__main__':
    main = tk.Tk()
    p = pretty_math('p(x)=x^3 +3x^2 +1', main)
    p.pack()
    main.mainloop()
