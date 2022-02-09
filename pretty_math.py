import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from polynomial_class_revisited import Polynomial
# idea taken from stackoverflow answer by ljetibo
# https://stackoverflow.com/questions/36636185/is-it-possible-for-python-to-display-latex-in-real-time-in-a-text-box


class Pretty_math(tk.Frame):
    def __init__(self, math_text, variable = 'x', poly_name = 'p',is_definite = False, is_eval=False, **kwargs):
        super().__init__(**kwargs)
        self.config(bg='white')
        if '=' in poly_name:
            self.math_text = poly_name + math_text
        else:
            self.math_text = f'{poly_name}({variable})=' + math_text
        label = tk.Label(self, font=('Computer Modern Roman', 12), bd = 0, relief = 'flat', bg = 'white')
        label.pack()
        num_terms = len(math_text.split(variable))
        # if is_definite:
        #     fig_size = (3,.55)
        # elif is_eval:
        #     fig_size = (2, .55)
        # else:
        #     fig_size = (1+num_terms//2,.5)
        fig_size = (5, .5)
        fig = matplotlib.figure.Figure(figsize=fig_size, dpi=100)
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
        # print(self.ax.get_ylim())
        self.ax.text(-0.1, 0.35, tmptext, fontsize=12, math_fontfamily='cm')
        self.canvas.draw()

if __name__ == '__main__':
    main = tk.Tk()
    main.configure(bg = 'white')
    derivative = Polynomial('-(x+1/2)(x-2)')
    poly_name = 'p'
    variable = 'x'
    n=1
    for _ in range(n):
        derivative.derivative()
        derivative = derivative.prime
    if n == 1:
        derivative_name = poly_name+'\''
    elif n == 2:
        derivative_name = poly_name+'\'\''
    else:
        derivative_name = poly_name+'^{'+f'({n})'+'}'

    derivative_pretty = Pretty_math(math_text=derivative.tex_string,
                                    variable=variable,
                                    poly_name=derivative_name,
                                    master=main)
    # p = Pretty_math(r'\dfrac{2}{3}\cdot x^{3}+\dfrac{2}{3}\cdot x^{3}+\dfrac{2}{3}\cdot x^{3}+\dfrac{2}{3}\cdot x^{3}',
    #                 variable = 'x',
    #                 poly_name = 'p',
    #                 master = main)
    derivative_pretty.pack(expand = True, fill = 'both')
    main.mainloop()
