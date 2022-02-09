from tkinter import *
from tkinter import ttk
from tkinter import font
from polynomial_class_revisited import Polynomial, DivisionFormatError, VariableFormatError, ExponentFormatError
from pretty_math import Pretty_math

class Polynomial_gui(Tk):
    def __init__(self):
        super().__init__()
        self.title('Polynomial Calculator')
        self.geometry("900x500")
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family='Courier 10 Pitch',
                                   size=12)

        self.enter_poly_left = Frame(self, bd=2, relief='solid')
        self.enter_poly_left.grid(row = 1, column = 1, sticky = 'NSEW')

        self.enter_poly_right = Frame(self, bg = 'white', bd=2, relief='solid')
        self.enter_poly_right.grid(row = 1, column = 2, sticky = 'NSEW')
        
        self.eval_left = Frame(self, bd=2, relief='solid')
        self.eval_left.grid(row = 2, column = 1, sticky = 'NSEW')

        self.eval_right = Frame(self, bg = 'white', bd=2, relief='solid')
        self.eval_right.grid(row = 2, column = 2, sticky = 'NSEW')

        self.derivative_left = Frame(self, bd=2, relief='solid')
        self.derivative_left.grid(row = 3, column = 1, sticky = 'NSEW')

        self.derivative_right = Frame(self, bg = 'white', bd=2, relief='solid')
        self.derivative_right.grid(row = 3, column = 2, sticky = 'NSEW')

        self.indefinite_left = Frame(self, bd=2, relief='solid')
        self.indefinite_left.grid(row = 4, column = 1, sticky = 'NSEW')

        self.indefinite_right = Frame(self, bg = 'white', bd=2, relief='solid')
        self.indefinite_right.grid(row = 4, column = 2, sticky = 'NSEW')

        self.definite_left = Frame(self, bd=2, relief='solid')
        self.definite_left.grid(row = 5, column = 1, sticky = 'NSEW')

        self.definite_right = Frame(self, bg = 'white', bd=2, relief='solid')
        self.definite_right.grid(row = 5, column = 2, sticky = 'NSEW')
        
        self.roots_left = Frame(self, bd=2, relief='solid')
        self.roots_left.grid(row = 6, column = 1, sticky = 'NSEW')

        self.roots_right = Frame(self, bg = 'white', bd=2, relief='solid')
        self.roots_right.grid(row = 6, column = 2, sticky = 'NSEW')
        
        
        # self.graph_left = Frame(self, bd=2, relief='solid')
        # self.graph_left.grid(row = 7, column = 1, sticky = 'NSEW')
        #
        # self.graph_right = Frame(self, bd=2, relief='solid')
        # self.graph_right.grid(row = 7, column = 2, sticky = 'NSEW')


        self.poly_name = 'p'
        self.poly_string_var = StringVar(self)
        self.poly_string_var.set('(x^2-2)(x+5)(x-1)')
        self.make_enter_polynomial_frame()
        self.make_simplify_frame()


        self.eval_at_value = DoubleVar(self)
        self.eval_at_value.set(0)
        self.make_enter_evaluate_frame()
        self.make_evaluate_result_frame()

        self.nth_derivative = IntVar(self)
        self.nth_derivative.set(1)
        self.make_derivative_select_frame()
        self.make_pretty_derivative_frame(n = 1)

        self.make_indefinite_frame()

        self.a = DoubleVar(self)
        self.a.set(0)
        self.b = DoubleVar(self)
        self.b.set(6)
        self.make_select_definite_bounds_frame()
        self.make_definite_frame()

        self.root_guess = DoubleVar(self)
        self.root_guess.set(1.4)
        self.max_find_root_iterations = DoubleVar(self)
        self.max_find_root_iterations.set(10000)
        self.find_roots_tolerance = DoubleVar(self)
        self.find_roots_tolerance.set(1e-39)

        self.make_guess_roots_frame()
        self.make_get_roots_frame()

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 3)
        self.columnconfigure(2, weight = 3)
        self.columnconfigure(3, weight = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(2, weight = 2)
        self.rowconfigure(3, weight = 2)
        self.rowconfigure(4, weight = 2)
        self.rowconfigure(5, weight = 2)
        self.rowconfigure(6, weight = 2)
        self.rowconfigure(7, weight = 1)

    def remake_all_frames(self):
        try:
            for widget in self.winfo_children():
                if type(widget) not in [StringVar, IntVar, DoubleVar]:
                    widget.destroy()

            self.enter_poly_left = Frame(self, bd=2, relief='solid')
            self.enter_poly_left.grid(row=1, column=1, sticky='NSEW')
            self.enter_poly_right = Frame(self, bg='white', bd=2, relief='solid')
            self.enter_poly_right.grid(row=1, column=2, sticky='NSEW')
            self.eval_left = Frame(self, bd=2, relief='solid')
            self.eval_left.grid(row=2, column=1, sticky='NSEW')
            self.eval_right = Frame(self, bg='white', bd=2, relief='solid')
            self.eval_right.grid(row=2, column=2, sticky='NSEW')
            self.derivative_left = Frame(self, bd=2, relief='solid')
            self.derivative_left.grid(row=3, column=1, sticky='NSEW')
            self.derivative_right = Frame(self, bg='white', bd=2, relief='solid')
            self.derivative_right.grid(row=3, column=2, sticky='NSEW')
            self.indefinite_left = Frame(self, bd=2, relief='solid')
            self.indefinite_left.grid(row=4, column=1, sticky='NSEW')
            self.indefinite_right = Frame(self, bg='white', bd=2, relief='solid')
            self.indefinite_right.grid(row=4, column=2, sticky='NSEW')
            self.definite_left = Frame(self, bd=2, relief='solid')
            self.definite_left.grid(row=5, column=1, sticky='NSEW')
            self.definite_right = Frame(self, bg='white', bd=2, relief='solid')
            self.definite_right.grid(row=5, column=2, sticky='NSEW')
            self.roots_left = Frame(self, bd=2, relief='solid')
            self.roots_left.grid(row=6, column=1, sticky='NSEW')
            self.roots_right = Frame(self, bg='white', bd=2, relief='solid')
            self.roots_right.grid(row=6, column=2, sticky='NSEW')
            # self.graph_left = Frame(self, bd=2, relief='solid')
            # self.graph_left.grid(row=7, column=1, sticky='NSEW')
            # self.graph_right = Frame(self, bd=2, relief='solid')
            # self.graph_right.grid(row=7, column=2, sticky='NSEW')

            self.make_enter_polynomial_frame()
            self.make_simplify_frame()
            self.make_enter_evaluate_frame()
            self.make_evaluate_result_frame()
            self.make_derivative_select_frame()
            self.make_pretty_derivative_frame()
            self.make_indefinite_frame()
            self.make_select_definite_bounds_frame()
            self.make_definite_frame()

            self.make_guess_roots_frame()
            self.make_get_roots_frame()

            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=3)
            self.columnconfigure(2, weight=3)
            self.columnconfigure(3, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=2)
            self.rowconfigure(2, weight=2)
            self.rowconfigure(3, weight=2)
            self.rowconfigure(4, weight=2)
            self.rowconfigure(5, weight=2)
            self.rowconfigure(6, weight=2)
            self.rowconfigure(7, weight=1)
        except VariableFormatError:
            self.poly_string_var.set('0')
            self.remake_all_frames()
        except DivisionFormatError:
            self.poly_string_var.set('0')
            self.remake_all_frames()
        except ExponentFormatError:
            self.poly_string_var.set('0')
            self.remake_all_frames()
        except TypeError:
            self.poly_string_var.set('0')
            self.remake_all_frames()

    def error_popup(self,error):
        error_pop_up = Tk()
        error_pop_up.title('Too many Variables')

    def make_enter_polynomial_frame(self):
        enter_frame = Frame(self.enter_poly_left)
        enter_frame.pack(fill = 'both', expand = True)

        enter_frame_left_space = Label(enter_frame, text='')
        enter_frame_right_space = Label(enter_frame, text='')
        enter_frame_center_space = Label(enter_frame, text='')

        enter_label = Label(enter_frame, text='Enter a polynomial below, then press set:')
        enter_label.pack(fill='both', expand = True)

        self.poly = Polynomial(self.poly_string_var.get())
        self.degree = self.poly.degree
        self.variable = self.poly.variable

        p_label = Label(enter_frame,text=f'p({self.poly.variable})=')
        poly_entry = Entry(enter_frame,
                           justify='left',
                           textvariable=self.poly_string_var,
                           font =('Courier 10 Pitch',12))

        set_poly_button = Button(enter_frame, text='Set', command=lambda: self.button_press('set polynomial'))
        enter_frame_left_space.pack(side='left')
        enter_frame_right_space.pack(side='right')
        p_label.pack(side='left')
        poly_entry.pack(side='left', fill='x', expand=True)
        enter_frame_center_space.pack(side='left')
        set_poly_button.pack(side='right', fill='x')

    def make_enter_evaluate_frame(self):
        enter_eval_frame = Frame(self.eval_left)
        enter_eval_frame.pack(fill = 'both', expand = True)

        enter_eval_label = Label(enter_eval_frame, text = 'Enter value to evaluate at:')
        value_entry = Entry(enter_eval_frame, textvariable=self.eval_at_value, width =6)
        evaluate_button = Button(enter_eval_frame,
                                 text = 'Evaluate!',
                                 command=lambda: self.button_press('evaluate'))

        enter_eval_label.grid(row = 0, column = 1, sticky = 'NSEW')
        value_entry.grid(row = 0, column = 2, sticky = 'EW')
        evaluate_button.grid(row = 0, column = 3)

        enter_eval_frame.rowconfigure(0, weight=1)
        enter_eval_frame.columnconfigure(0, weight=1)
        enter_eval_frame.columnconfigure(1, weight=1)
        enter_eval_frame.columnconfigure(2, weight=2)
        enter_eval_frame.columnconfigure(3, weight=1)
        enter_eval_frame.columnconfigure(4, weight=1)


    def make_derivative_select_frame(self):
        derivative_select_frame = Frame(self.derivative_left)
        derivative_select_frame.pack(fill = 'both', expand = True)
        derivative_select_label = Label(derivative_select_frame, text='Select a derivative:')


        derivative_list = []
        for k in range(1,self.degree+1):
            derivative_list.append(self.make_nth_string(k))
        self.derivative_dropdown = ttk.Combobox(derivative_select_frame,
                                           values=derivative_list,
                                           width=2,
                                           font=('Courier 10 Pitch',12))
        nth = self.make_nth_string(self.nth_derivative.get())
        self.derivative_dropdown.set(nth)
        derivative_show_button = Button(derivative_select_frame,
                                        text='Show!',
                                        width=2,
                                        command=lambda: self.button_press('take derivative'))

        derivative_select_label.grid(row=0, column=0, sticky='EW')
        self.derivative_dropdown.grid(row=0, column=2, sticky='EW')
        derivative_show_button.grid(row=0, column=4, sticky='EW')

        derivative_select_frame.rowconfigure(0, weight=1)
        derivative_select_frame.columnconfigure(0, weight=1)
        derivative_select_frame.columnconfigure(1, weight=1)
        derivative_select_frame.columnconfigure(2, weight=1)
        derivative_select_frame.columnconfigure(3, weight=1)
        derivative_select_frame.columnconfigure(4, weight=1)
        derivative_select_frame.columnconfigure(5, weight=1)
        derivative_select_frame.columnconfigure(6, weight=1)

    def make_select_definite_bounds_frame(self):
        select_bounds_frame = Frame(self.definite_left)
        select_bounds_frame.pack(expand=True, fill='both')

        message = Label(select_bounds_frame, text = 'Enter integral bounds: ')
        a_label = Label(select_bounds_frame, text = 'a=')
        a_entry = Entry(select_bounds_frame, textvariable=self.a, width = 4)
        b_label = Label(select_bounds_frame, text = 'b=')
        b_entry = Entry(select_bounds_frame, textvariable=self.b, width = 4)
        set_bounds = Button(select_bounds_frame, text = 'Set!', command=lambda: self.button_press('set bounds'))

        message.grid(row=0, column=1)
        a_label.grid(row=0, column=2, sticky= 'E')
        a_entry.grid(row=0, column=3, sticky='EW' )
        b_label.grid(row=0, column=4, sticky='E' )
        b_entry.grid(row=0, column=5, sticky='EW' )
        set_bounds.grid(row=0, column=6)

        select_bounds_frame.rowconfigure(0, weight=1)
        select_bounds_frame.columnconfigure(0, weight=1)
        select_bounds_frame.columnconfigure(1, weight=2)
        select_bounds_frame.columnconfigure(2, weight=2)
        select_bounds_frame.columnconfigure(3, weight=2)
        select_bounds_frame.columnconfigure(4, weight=2)
        select_bounds_frame.columnconfigure(5, weight=2)
        select_bounds_frame.columnconfigure(6, weight=1)
        select_bounds_frame.columnconfigure(7, weight=1)

    def make_guess_roots_frame(self):
        guess_label = Label(self.roots_left, text='Guess root location, a=')
        guess_label.grid(row = 1, column=1, sticky = 'E')
        guess_entry = Entry(self.roots_left, textvariable=self.root_guess)
        guess_entry.grid(row = 1, column=2, sticky = 'EW')

        max_iterations_label = Label(self.roots_left, text='Max number of iterations:')
        max_iterations_label.grid(row = 2, column=1, sticky = 'E')
        max_iterations_entry = Entry(self.roots_left, textvariable=self.max_find_root_iterations)
        max_iterations_entry.grid(row = 2, column=2, sticky = 'EW')

        tolerance_label = Label(self.roots_left, text='Tolerance:')
        tolerance_label.grid(row = 3, column=1, sticky = 'E')
        tolerance_entry = Entry(self.roots_left, textvariable=self.find_roots_tolerance)
        tolerance_entry.grid(row = 3, column=2, sticky = 'EW')

        find_roots_button = Button(self.roots_left, text = 'Find root!', command=lambda: self.button_press('find root'))
        find_roots_button.grid(row = 4, column=1, columnspan=2, sticky = 'EW')

        self.roots_left.rowconfigure(0,weight=1)
        self.roots_left.rowconfigure(1, weight=2)
        self.roots_left.rowconfigure(2, weight=2)
        self.roots_left.rowconfigure(3, weight=2)
        self.roots_left.rowconfigure(4, weight=2)
        self.roots_left.rowconfigure(5, weight=1)

        self.roots_left.columnconfigure(0, weight=1)
        self.roots_left.columnconfigure(1, weight=2)
        self.roots_left.columnconfigure(2, weight=2)
        self.roots_left.columnconfigure(3, weight=1)


    def make_simplify_frame(self):
        simplified_frame = Frame(self.enter_poly_right, bg = 'white')
        simplified_frame.pack(fill='both', expand=True)
        simplified_pretty = Pretty_math(math_text = self.poly.tex_string,
                                        variable = self.variable,
                                        poly_name = self.poly_name,
                                        master = simplified_frame)
        simplified_pretty.pack(side = 'left', fill='x', expand=True)


    def make_evaluate_result_frame(self):
        value = self.poly.evaluate(float(self.eval_at_value.get()))
        eval_name = r'p'+f'({self.eval_at_value.get()})='
        evaluated_pretty = Pretty_math(math_text=str(value),
                                        variable=self.variable,
                                        poly_name=eval_name,
                                        is_definite=True,
                                        master=self.eval_right)
        evaluated_pretty.pack(side = 'left', fill='x', expand=True)

    def make_nth_string(self, n):
        if n == 1:
            nth = '1st'
        elif n == 2:
            nth = '2nd'
        elif n == 3:
            nth = '3rd'
        else:
            nth = f'{n}th'
        return nth

    def make_pretty_derivative_frame(self, n = None):
        if n == None:
            n = int(self.nth_derivative.get())
        derivative = self.poly
        for _ in range(n):
            derivative.derivative()
            derivative = derivative.prime
        if n == 1:
            derivative_name = self.poly_name+'\''
        elif n == 2:
            derivative_name = self.poly_name+'\'\''
        else:
            derivative_name = self.poly_name+'^{'+f'({n})'+'}'
        derivative_pretty = Pretty_math(math_text=derivative.tex_string,
                                        variable=self.variable,
                                        poly_name=derivative_name,
                                        master=self.derivative_right)
        derivative_pretty.pack(side = 'left', expand=True, fill='x')

    def make_indefinite_frame(self):
        indefinite_label = Label(self.indefinite_left, text = 'The indefinite integral is').pack(fill='both',
                                                                                                 expand=True)

        self.poly.indefinite()
        anti_name = r'\int \,\, p'+f'({self.variable})d{self.variable}='
        integral_label = Pretty_math(math_text = self.poly.anti.tex_string + '+C',
                                        variable = self.variable,
                                        poly_name = anti_name,
                                        master = self.indefinite_right)
        integral_label.pack(side = 'left', fill='x', expand=True)

    def make_definite_frame(self):
        aval = self.a.get()
        if aval - aval//1 == 0:
            aval = int(aval)
        bval = self.b.get()
        if bval - bval//1 == 0:
            bval = int(bval)

        definite_name = r'\int'+'^{'+str(bval)+'}_{'+str(aval)+r'} p'+f'({self.variable})d{self.variable}='
        definite_value =  self.poly.definite(a=aval,b=bval)
        definite_label = Pretty_math(math_text = str(definite_value),
                                     variable = self.variable,
                                     poly_name = definite_name,
                                     is_definite = True,
                                     master = self.definite_right)
        definite_label.pack(side = 'left', fill='x', expand=True)

    def make_get_roots_frame(self):
        a = self.root_guess.get()
        max_its = int(self.max_find_root_iterations.get())
        tolerance = self.find_roots_tolerance.get()
        root_value,p_value = self.poly.roots(a=a,
                                             max_iterations=max_its,
                                             accepted_tolerance=tolerance)
        roots_label = Label(self.roots_right,
                            text=f' Root near a={root_value}, p(a)={p_value}\n These values may be approximate!\n Rounded to 12 decimal places',
                            bg='white')
        roots_label.grid(row=1, column=1, sticky = 'NSEW')
        self.roots_right.rowconfigure(0, weight=1)
        self.roots_right.rowconfigure(1, weight=1)
        self.roots_right.rowconfigure(2, weight=1)

        self.roots_right.columnconfigure(0, weight=1)
        self.roots_right.columnconfigure(1, weight=2)
        self.roots_right.columnconfigure(2, weight=2)
        self.roots_right.columnconfigure(3, weight=5)


    def button_press(self, which_button):
        if which_button == 'set polynomial':
            self.remake_all_frames()
        elif which_button == 'evaluate':
            self.eval_right.destroy()
            self.eval_right = Frame(self, bg='white', bd=2, relief='solid')
            self.eval_right.grid(row=2, column=2, sticky='NSEW')
            self.make_evaluate_result_frame()
        elif which_button == 'take derivative':
            nth = self.derivative_dropdown.get()
            self.nth_derivative.set(int(nth[:-2]))
            self.derivative_right.destroy()
            self.derivative_right = Frame(self, bg='white', bd=2, relief='solid')
            self.derivative_right.grid(row=3, column=2, sticky='NSEW')
            self.make_pretty_derivative_frame()
        elif which_button == 'set bounds':
            self.definite_right.destroy()
            self.definite_right = Frame(self, bg='white', bd=2, relief='solid')
            self.definite_right.grid(row=5, column=2, sticky='NSEW')
            self.make_definite_frame()
        elif which_button == 'find root':
            self.roots_right.destroy()
            self.roots_right = Frame(self, bg='white', bd=2, relief='solid')
            self.roots_right.grid(row=6, column=2, sticky='NSEW')
            self.make_get_roots_frame()

    def make_graph_frame(self):
        graph = Canvas(self.graph_right)
        graph.pack(fill = 'both', expand = True)


if __name__ == '__main__':
    p = Polynomial_gui()
    p.mainloop()
