
class DivisionFormatError(Exception):
    pass

class VariableFormatError(Exception):
    pass

class ExponentFormatError(Exception):
    pass

class Polynomial(object):
    def __init__(self, polynomial=None, variable=None):
        if polynomial == None:
            self.polynomial = str(input("Input Polynomial:\n"))
        else:
            self.polynomial = polynomial

        if ' ' in self.polynomial:
            split = self.polynomial.split(' ')
            g = ''
            for item in split:
                g += item
            self.polynomial = g
        self.round_to = 5
        self.numbers = '0123456789'
        self.common_fractions = {.0:'1'}
        dens = [k for k in range(2,101)]
        dens.reverse()
        for den in dens:
            for num in range(1,den):
                self.common_fractions[round(num/den, 12)] = [num, den]
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        all_math = './[]()*+-'
        self.variable = None
        var_list = []
        if not variable:
            for x in self.polynomial:
                if x in letters:
                    self.variable = x
                    if x not in var_list:
                        var_list.append(x)
                        if len(var_list) >= 2:
                            raise VariableFormatError
        else:
            self.variable = variable
        if not self.variable:
            self.variable = 'x'
        self.original = self.polynomial
        self.make_term_list()
        self.simplify_dct_list()
        self.polynomial = self.make_print_string()
        self.make_tex_string()
        self.degree = max(self.poly_dct.keys())


    def fix_notation(self, f=None):
        """
        Takes in a polynomial as a string, and changes the notation of the polynomial so that every exponent is
        contained in curly brackets {}, every variable term has an exponent, and so there is a *
        wherever a product occurs. Also turns subtraction into addition times a negative.
        Returns the polynomial with new notation.
        :param f: string, uses class instance as the default
        :return: string

        Example: f=2(x+3)(x^2-5)->2*(x^{1}+3)*(x^{2}-1*5)
        """
        if f == None:
            f = self.polynomial
        numbers_plus = '.0123456789)'
        g = ''
        x = self.variable
        close_exponent = False
        i = 0
        while i < len(f):
            if f[i] == '-':
                g += '-1*'
            else:
                if i == len(f) - 1:
                    if f[i] == x:
                        g += x + "^{1}"
                    else:
                        g += f[i]
                else:
                    if f[i] in numbers_plus and f[i+1] not in '.0123456789-+*/^)]':
                        g += f[i] + "*"
                    elif f[i] == x and f[i+1] != '^':
                        g += x + "^{1}"
                    elif f[i] in ')}]' and f[i+1] not in '+-^*/':
                        g += f[i] + '*'
                    elif f[i] == '^':
                        g += '^{'
                        i+=1
                        while f[i] in self.numbers:
                            g += f[i]
                            i += 1
                            if i == len(f):
                                break
                        i -= 1
                        g += '}'
                    else:
                        g += f[i]
                if i < len(f) - 1:
                    if f[i] == x and f[i+1] in '({[':
                        g += "*"
            i += 1
        return g


    def make_term_list(self, f=None):
        """
        Turns a polynomial as a string into a list of strings and lists. Anything contained in parentheses becomes a
        list. Exponent carrots and their value become a single term without curly brackets.
        Ex:
        2*x^{10}+6*x^{12}+-1*3^{2} -> ['2','*','x','^10','+','6','*','x','^12','+','-1','*','3','^2']
        2*(x^{1}+3)*(x^{2}+5) -> ['2','*',['x','^1','+','3'],'*',['x','^2','+','5']]
        :param f: a string, defaults to class instance polynomial string
        :return: a list
        """
        if f == None:
            f = self.fix_notation()
            save_result = True
        else:
            save_result = False
        term_list = []
        term = ""
        i = 0
        while i < len(f):
            if f[i] in "0123456789." + self.variable:
                if i != len(f) - 1:
                    term += f[i]
                else:
                    term += f[i]
                    term_list.append(term)
            elif f[i] == '-':
                if i == 0:
                    term += '-'
                elif term == '':
                    term += '-'
                    term_list.append('+')
                else:
                    term_list.append(term)
                    term_list.append('+')
                    term = '-'
            elif f[i] in "+^*/":
                if term != "":
                    term_list.append(term)
                    term = ''
                    term_list.append(f[i])
                else:
                    term_list.append(f[i])
            elif f[i] in '(':
                if term != "":
                    term_list.append(term)
                    term = ""
                j = i + 1
                while f[j] not in ')':
                    term += f[j]
                    j += 1
                    i = j
                term_list.append(self.make_term_list(term))
                term = ''
            elif f[i] in '[':
                if term != "":
                    term_list.append(term)
                    term = ""
                j = i + 1
                while f[j] not in ']':
                    term += f[j]
                    j += 1
                    i = j
                term_list.append(self.make_term_list(term))
                term = ''
            elif f[i] in '{':
                if term != "":
                    term_list.append(term)
                term = '{'
                j = i + 1
                while f[j] not in '}':
                    term += f[j]
                    j += 1
                    i = j
                term += '}'
                if term == '{}':
                    raise ExponentFormatError
                term_list.append(term)
                term = ''
            i += 1
        if save_result:
            self.term_list = term_list
            self.list_term_to_dct()
        return term_list

    def list_term_to_dct(self,term_list = None):
        """
        Turns the string terms of a term_list into a dictionary.  The keys of the dictionary are the degree of the term,
        the value of the dictionary is the coefficient value. Except for constant terms, every coefficient is treated as
        one during this process, and if there is a coefficient two dictionaries are made. Later, a dictionary will
        represent an entire polynomial.
        Examples (The first arrow is make_term_list, the second is this method, list_term_to_dct.)
          '5' -> ['5'] -> [{0: 5}]
          'x^{2}' -> ['x','^2'] -> [{2: 1}]
          '5*x^{2}' -> ['5','*','x','^2'] -> [{0:5},'*',{2:1}]
          '(5*x^{2})^{3}+2^{6}' -> [['5','*','x','^2'],'^3','+','2','^6'] -> [[{0:5},'*',{2:1}],'^3','+',{0: 2},'^6']
        :param term_list: list
        :return: list
        """
        dct_list = []
        save_result = False
        if term_list == None:
            term_list = self.term_list
            save_result = True
        for i,item in enumerate(term_list):
            if type(item) == list:
                dct_list.append(self.list_term_to_dct(item))
            elif item in '*+-/':
                dct_list.append(item)
            elif item == self.variable:
                power = term_list[i+2][1:-1]
                dct_list.append({int(power):1.0})
            elif item == '^' and term_list[i-1] != self.variable:
                dct_list.append('^'+term_list[i+1][1:-1])
            else:
                try:
                    dct_list.append({0:float(item)})
                except ValueError:
                    continue
        if save_result:
            self.dct_list = dct_list
        return dct_list

    def dct_mult(self, dct1, dct2):
        """
        Multiplies term dictionaries.
        Examples: the first bit is the product being preformed. The second is what the method sees and outputs.
          2*x^3 = 2x^3 : {0:2}*{3:1} -> {3:2}
          3*(2x^3+1) = 6x^3+3 : {0:3}*{3:2, 0:1} -> {3:6, 0:3}
          3x*(2x^3+1) = 6x^4+3x : {1:3}*{3:2, 0:1} -> {4:6, 1:3}
          (x^2+3)(1-2x) = -2x^3+x^2-6x+3  : {2:1, 0:3}*{1:-2, 0:1} -> {3:-2, 2:1, 1:-6, 0: 3}
        :param dct1: dictionary
        :param dct2: dictionary
        :return: dictionary
        """
        new_dct = {}
        for key1 in dct1:
            for key2 in dct2:
                if key1+key2 not in new_dct.keys():
                    if dct1[key1]*dct2[key2] != 0:
                        new_dct[key1+key2] = dct1[key1]*dct2[key2]
                else:
                    new_dct[key1+key2] += dct1[key1]*dct2[key2]
                    if new_dct[key1+key2] == 0:
                        new_dct.pop(key1+key2)
        return new_dct

    def dct_divide(self, dct1, dct2):
        """
        Divides Term dictionaries. Currently, In practice, the term being denominator (dct2) should ONLY be a constant!
        That said, this operation will divide a polynomial by a monomial.
        :param dct1: dictionary
        :param dct2: dictionary
        :return: dictionary
        """
        if len(dct2)>1:
            raise DivisionFormatError
        new_dct = {}
        for key1 in dct1:
            for key2 in dct2:
                if key2 != 0:
                    raise DivisionFormatError
                if key1-key2 not in new_dct.keys():
                    new_dct[key1-key2] = dct1[key1]/dct2[key2]
                else:
                    new_dct[key1-key2] += dct1[key1]/dct2[key2]
        return new_dct

    def dct_sum(self, dct1, dct2):
        """
        Adds term dictionaries.
        Examples: the first bit is the product being preformed. The second is what the method sees and outputs.
          2+x^3 = 2+x^3 : {0:2}+{3:1} -> {3:1,0:2}
          3+(2x^3+1) = 2x^3+4 : {0:3}+{3:2, 0:1} -> {3:2, 0:4}
          (3x+5)+(2x^3+1) = 2x^3+3x+6 : {1:3, 0:5}+{3:2, 0:1} -> {3:2, 1:3, 0:6}
        :param dct1: dictionary
        :param dct2: dictionary
        :return: dictionary
        """
        for key in dct2:
            if key in dct1.keys():
                dct1[key] += dct2[key]
                if dct1[key] == 0:
                    dct1.pop(key)
            else:
                dct1[key] = dct2[key]
                if dct1[key] == 0:
                    dct1.pop(key)
        return dct1

    def dct_diff(self, dct1, dct2):
        """
        Subtracts term dictionaries.
        Examples: the first bit is the product being preformed. The second is what the method sees and outputs.
          2-x^3 = 2-x^3 : {0:2}-{3:1} -> {3:-1,0:2}
          (2x^3+1)-3 = 2x^3-2 : {3:2, 0:1}-{0:3} -> {3:2, 0:-2}
          (3x+5)-(2x^3+1) = -2x^3+3x+4 : {1:3, 0:5}-{3:2, 0:1} -> {3:-2, 1:3, 0:4}
        :param dct1: dictionary
        :param dct2: dictionary
        :return: dictionary
        """
        for key in dct2:
            if key in dct1.keys():
                dct1[key] -= dct2[key]
            else:
                dct1[key] = -1*dct2[key]
            if dct1[key] == 0:
                dct1.pop(key)
        return dct1

    def dct_power(self, dct, power):
        """
        Raises a term dictionary to a positive integer power by repeatedly preforming dct_mult.
        Examples: the first bit is the operation being preformed. The second is what the method sees and outputs.
          (3x^2)^4 = 81x^8 : {2:3}^4 -> {8:81}
          (x+1)^2 = x^2+2x+1 : {1:1,0:1} -> {2:1, 1:2, 0:1}
          (x^2+2x+1)^2 = x^4+4x^3+5x^2+4x+1 : {2:1, 1:2, 0:1} -> {4:1, 3:4, 2:5, 1:4, 0:1}
        :param dct1: dictionary
        :param dct2: dictionary
        :return: dictionary
        """
        if power == 1:
            return dct
        dct_p = {key:dct[key] for key in dct}
        for i in range(1,power):
            dct_p = self.dct_mult(dct_p, dct)
        return dct_p

    def simplify_dct_list(self, dct_list=None):
        """
        Simplifies the output of list_term_to_dct using the various dct_{operation}.
        Outputs a single dictionary that represents the entire polynomial in expanded form.
        :param dct_list: list, defaults to the output of list_term_to_dct
        :return: dictionary
        """
        if dct_list == None:
            save_dct = True
            dct_list = self.dct_list
        else:
            save_dct = False
        new_dct_list = []
        for item in dct_list:
            if type(item) == list:
                new_dct_list.append(self.simplify_dct_list(item))
            else:
                new_dct_list.append(item)
        dct_list = new_dct_list
        new_dct_list = []
        for i,item in enumerate(dct_list):
            if i+1<len(dct_list):
                if '^' in dct_list[i+1]:
                    new_dct = self.dct_power(item,int(dct_list[i+1][1:]))
                    new_dct_list.append(new_dct)
                elif '^' in item:
                    continue
                else:
                    new_dct_list.append(item)
            else:
                if '^' in item:
                    continue
                else:
                    new_dct_list.append(item)
        dct_list = new_dct_list
        while '*' in dct_list:
            for i,item in enumerate(dct_list):
                if item == '*':
                    new_dct = self.dct_mult(dct_list[i-1],dct_list[i+1])
                    dct_list[i-1] = new_dct
                    dct_list.pop(i)
                    dct_list.pop(i)
                    break
        while '/' in dct_list:
            for i,item in enumerate(dct_list):
                if item == '/':
                    new_dct = self.dct_divide(dct_list[i-1],dct_list[i+1])
                    dct_list[i-1] = new_dct
                    dct_list.pop(i)
                    dct_list.pop(i)
                    break
        while '+' in dct_list:
            for i,item in enumerate(dct_list):
                if item == '+':
                    new_dct = self.dct_sum(dct_list[i-1],dct_list[i+1])
                    dct_list[i-1] = new_dct
                    dct_list.pop(i)
                    dct_list.pop(i)
                    break
        while '-' in dct_list:
            for i,item in enumerate(dct_list):
                if item == '-':
                    new_dct = self.dct_diff(dct_list[i-1],dct_list[i+1])
                    dct_list[i-1] = new_dct
                    dct_list.pop(i)
                    dct_list.pop(i)
                    break
        if dct_list[0] == {}:
            dct_list[0] = {0:0}
        if save_dct:
            self.poly_dct = dct_list[0]
        return dct_list[0]

    def make_tex_string(self, poly_dct = None):
        """
        Turns the polynomial dictionary representation into a string which will be nicely formatted via Tex.

        Note that fractions are rounded at the 12th decimal place.  This may cause issues for huge exponents or
        very precise coefficients.

        :param poly_dct: a dictionary, defaults to the output of simplify_dct_list.
        :return: a string
        """
        if poly_dct == None:
            poly_dct = self.poly_dct
            to_save = True
        else:
            to_save = False
        if poly_dct == {}:
            return '0'
        powers = list(poly_dct.keys())
        powers.sort()
        powers.reverse()
        string = ''
        x = self.variable
        for i, power in enumerate(powers):
            if i == 0:
                if poly_dct[power] < 0:
                    string += '-'
            value_str = str(float(abs(poly_dct[power])))
            value_split = value_str.split('.')
            value_int = int(value_split[0])
            value_decimal = round(float('0.'+value_split[1]),12)
            if value_decimal == 0.0:
                coef = str(value_int)
            elif value_decimal in self.common_fractions:
                value_frac_lst = self.common_fractions[value_decimal]
                numerator = value_frac_lst[0]
                denominator = value_frac_lst[1]
                coef = r'\dfrac{'+f'{value_int*denominator+numerator}'+r'}{'+f'{denominator}'+r'}'
            elif len(str(value_decimal)) < 12:
                numerator = int(value_split[1])
                denominator = 10**(len(str(value_decimal))-2)
                coef = r'\dfrac{'+f'{value_int*denominator+numerator}'+r'}{'+f'{denominator}'+r'}'
            else:
                value_decimal_round = round(value_decimal, self.round_to)
                coef = str(value_int+value_decimal_round)
            if coef == '1':
                if power > 1:
                    string += x+'^{'+str(power)+'}'
                elif power == 1:
                    string += x
                elif power == 0:
                    string += coef
            else:
                if power > 1:
                    string += coef+r'\cdot '+x+'^{'+str(power)+'}'
                elif power == 1:
                    string += coef+r'\cdot '+x
                elif power == 0:
                    string += coef
            if i < len(powers)-1:
                if poly_dct[powers[i+1]] > 0:
                    string += '+'
                else:
                    string += '-'
        if to_save:
            self.tex_string = string
        return string



    def make_print_string(self,poly_dct = None):
        """
        Turns the polynomial dictionary representation into a string which will be nicely formatted for printing to
        an ipython console or to the terminal.  This will also be used in the indefinite and derivative class methods
        to make those class instances.

        Note that fractions are rounded at the 12th decimal place.  This may cause issues for huge exponents or
        very precise coefficients.

        :param poly_dct: a dictionary, defaults to the output of simplify_dct_list
        :return: a string
        """
        if poly_dct == None:
            poly_dct = self.poly_dct
            to_save = True
        else:
            to_save = False
        if poly_dct == {}:
            return '0'
        powers = list(poly_dct.keys())
        powers.sort()
        powers.reverse()
        string = ''
        x = self.variable
        for i,power in enumerate(powers):
            if i == 0:
                if poly_dct[power]<0:
                    string += '-'
            value_str = str(float(abs(poly_dct[power])))
            value_split = value_str.split('.')

            value_int = int(value_split[0])
            value_decimal = round(float('0.'+value_split[1]),12)
            if value_decimal == 0.0:
                coef = str(value_int)
            elif value_decimal in self.common_fractions:
                value_frac_lst = self.common_fractions[value_decimal]
                numerator = value_frac_lst[0]
                denominator = value_frac_lst[1]
                coef = f'({value_int*denominator+numerator}/{denominator})'

            elif len(str(value_decimal)) < 12:
                numerator = int(str(value_decimal)[2:])
                denominator = 10**(len(str(value_decimal))-2)
                coef = f'({value_int*denominator+numerator}/{denominator})'

            else:
                value_decimal_round = round(value_decimal, self.round_to)
                coef = str(value_int+value_decimal_round)

            if coef == '1':
                if power > 1:
                    string += x+'^'+str(power)
                elif power == 1:
                    string += x
                elif power == 0:
                    string += coef
            else:
                if power > 1:
                    string += coef+x+'^'+str(power)
                elif power == 1:
                    string += coef+x
                elif power == 0:
                    string += coef
            if i < len(powers)-1:
                if poly_dct[powers[i+1]]>0:
                    string += '+'
                else:
                    string += '-'
        if to_save:
            self.print_string = string
        return string

    def evaluate(self, num):
        """
        Evaluates the polynomial as a given number num.
        :param num: float
        :return: float
        """
        if type(num) not in [float,int]:
            raise ValueError

        value = 0
        for key in self.poly_dct:
            value += self.poly_dct[key] * (num ** key)
        return value

    def derivative(self):
        """
        Returns a string of the derivative and stores the derivative as a class instance at self.prime
        :return: string
        """
        derivative_dct = {key-1:key*self.poly_dct[key] for key in self.poly_dct if key!=0}
        f_prime = self.make_print_string(derivative_dct)
        self.prime = Polynomial(f_prime)
        return f_prime

    def indefinite(self):
        """
        Returns a string of the indefinite integral and stores the integral as a class instance at self.anti
        :return: string
        """
        if self.poly_dct == {0:0} or self.poly_dct == {0:0.0}:
            indefinite_dct = {0:0}
        else:
            indefinite_dct = {key+1:self.poly_dct[key]/(key+1) for key in self.poly_dct}
        F = self.make_print_string(indefinite_dct)
        self.anti = Polynomial(F)
        return F


    def definite(self, a=None, b=None):
        """
        Computes the definite integral of the polynomial from a to b using the indefinite integral class instance at
        self.anti.  Rounds the results at the 12th decimal place
        :param a: float
        :param b: float
        :return: float
        """

        if type(a) not in [float,int]:
            raise ValueError
        if type(b) not in [float,int]:
            raise ValueError

        if a == None:
            a = float(input('Enter a: \n'))
            b = float(input('Enter b: \n'))
        self.indefinite()
        return round(self.anti.evaluate(b) - self.anti.evaluate(a),12)

    # make this better
    # def optimize(self, a=None, b=None):
    #     # find roots
    #     try:
    #         p_prime = self.prime
    #     except AttributeError:
    #         self.derivative()
    #         p_prime = self.prime
    #     if a//1 == a:
    #         a_ceil = int(a)
    #     else:
    #         a_ceil = int(1+a//1)
    #     b_floor = int(b//1)
    #     num_its = 2*(b_floor-a_ceil)+1
    #     to_find_roots = [a]+[a_ceil+k/2 for k in range(num_its)]+[b]
    #     roots = [p_prime.roots(a=x_val)[0] for x_val in to_find_roots]
    #     roots = list(set(roots))
    #     to_evaluate = [a]+[root for root in roots if a < root < b]+[b]
    #     print(to_evaluate)
    #     points = [(x_val,self.evaluate(x_val)) for x_val in to_evaluate]
    #     max_guess = points[0]
    #     min_guess = points[0]
    #     for point in points:
    #         if point[1] > max_guess[1]:
    #             max_guess = point
    #         if point[1] < min_guess[1]:
    #             min_guess = point
    #     return max_guess, min_guess


    def roots(self,
              a=None,
              max_iterations=10000,
              accepted_tolerance=1e-20):
        """
        Computes (approximations) of roots using Halley's method. a is a guess of the roots value, max_iterations is
        the maximum number of iterations the algorithm will preform, and accepted_tolerance is how close p(a) must be
        to zero for the algorithm to accept a as a root.
        The algorithm will terminate under either of the following conditions:
            1.) the number of iterations > max iterations,
            2.) |p(a)|< accepted_tolerance
        :param a: float
        :param max_iterations: int
        :param accepted_tolerance: float
        :return: float, float
        """
        if type(a) not in [float,int]:
            raise ValueError
        if type(max_iterations) is not int:
            raise ValueError
        if type(accepted_tolerance) not in [float,int]:
            raise ValueError

        if a == None:
            a = float(input("Guess:\n"))
        self.derivative()
        self.prime.derivative()
        n = 0
        while n < max_iterations and abs(self.evaluate(a)) > accepted_tolerance:
            f = float(self.evaluate(a))
            fprime = float(self.prime.evaluate(a))
            f2prime = float(self.prime.prime.evaluate(a))
            a = a - (2*f*fprime)/(2*fprime**2 - f*f2prime)
            n += 1
        f = round(float(self.evaluate(a)),12)
        a = round(a, 12)
        return a,f
        # print('I did n=', n, ' iterations', '\n root, a, is approximately', a, '\n f(a) is approximately', f)



if __name__ == '__main__':
    # poly = Polynomial('-(x+1/2)(x-2)')
    # print(poly.polynomial)
    # poly.derivative()
    # poly.roots(10)
    import matplotlib.pyplot as plt
    import numpy as np
    poly = Polynomial('1-+2')
    print(poly.polynomial)

    print('indefinite')

    print(poly.indefinite())
    # print(poly.anti.optimize(a=-2, b=200))
    # for
    # poly = Polynomial('x^2+2x+1')
    # poly = Polynomial('x^100 + 2^3 +2/3+2*3')
    # poly = Polynomial('(x+1)(x+1)')
    # poly = Polynomial('x(x^10+6x+7)')
    # poly = Polynomial('-(x+1)(x+2)(2x+3)')
    # poly = Polynomial('x^2+x^3')




