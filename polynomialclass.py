# -*- coding: utf-8 -*-
"""
A very basic polynomial analyzer.  

to create a new polynomial instance, p, type 'p=Polynomial()'.  The program will automatically
store your variable choice at 'p.variable', unfortunately this program only supports
polynomials of a single variable.
Your polynomial will automatically be simplified, to view your simplified polynomial
type 'p.polynomial' or 'p.simplify()'  

this program can evaluate your polynomial, to do this use 'p.evaluate(a)' where 
'a' is the value you would like evaluated.  

The program can numerically solve for roots, use 'p.root()'.

The program can brute force optimize over an interval, use 'p.optimize()' 

This program can do basic calculus with your polynomials!
To take a derivative, type 'p.derivative()'.  After using the derivative method, the derivative is saved as
an instance of the class polynomial.  In particular, it is stored at p.prime.
One can take multiple derivatives by iterating this process, for example, the
second derivative can be found with the following syntax 'p.prime.derivative()'.

Similarly, the program can tell you the indefinite integral of your polynomial, use
'p.indefinite()'.  This will create an instance of the indefinite integral, to call
this instance use the syntax 'p.anti'.

The program can also solve definite integrals, use 'p.definite()'  
"""

class Polynomial(object):
    def __init__(self, polynomial=None,variable=None):
        if polynomial == None:
            self.polynomial=str(input("Input Polynomial:\n"))
        else:
            self.polynomial=polynomial

        if ' ' in self.polynomial:
            split = self.polynomial.split(' ')
            g = ''
            for item in split:
                g += item
            self.polynomial = g
        self.numbers = '0123456789'
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.variable = None
        if not variable:
            for x in self.polynomial:
                if x in letters:
                    self.variable = x
                    break
        else:
            self.variable=variable
        if not self.variable:
            self.variable='x'
        self.original = self.polynomial
        self.plist()
        self.polynomial = self.simplify()
        self.degree = 0
        num_terms = len(self.polynomial)
        for i in range(num_terms):
            if self.polynomial[i] == '^' and self.polynomial[i-1] == self.variable:
                to_check = self.polynomial[i+1]
                for k in range(i+2, num_terms):
                    if self.polynomial[k] in self.numbers:
                        to_check += self.polynomial[k]
                    else:
                        break
                if int(to_check) > self.degree:
                    self.degree = int(to_check)
        
    def fix_notation(self,f=None):
        if f == None:
            f = self.polynomial
        i = 0
        numbers = '.0123456789)'
        g = ''
        x = self.variable
        #print(f)
        while i < len(f):
            if i == 0 and f[i] == x:
                g += "1*"
            elif f[i] == x and f[i-1] in '-+([{)]}':
                g += '1*'
                
            if i == len(f)-1:
                if f[i] == x:
                    g += x+"^1"
                else:
                    g += f[i]
            else:
                if f[i] in numbers and f[i+1] not in '.0123456789-+*/^)]}':
                    g += f[i]+"*"
                elif f[i] == x and f[i+1] != '^':
                    g+=x+"^1"
                elif f[i] in ')}]' and f[i+1] not in '+-^*/':
                    g+=f[i]+'*'
                else:
                    g += f[i]
            if i < len(f)-1:
                if f[i] == x and f[i+1] in '({[':
                    g += "*"
            i+=1
        return g
    
    def plist(self,f=None):
        if f == None:
            f = self.fix_notation()
        flst = []
        term = ""
        i = 0
        while i < len(f):
            if f[i] in "0123456789."+self.variable:
                if i != len(f)-1:
                    term += f[i]
                else:
                    term += f[i]
                    flst.append(term)
            elif f[i] == '-':
                if i == 0:
                    term += '-'
                elif term == '':
                    term += '-'
                    flst.append('+')
                else:
                    flst.append(term)
                    flst.append('+')
                    term='-'
            elif f[i] in "+^*/":
                if term != "":
                    flst.append(term)
                    term = ''
                    flst.append(f[i])
                else:
                    flst.append(f[i])
            elif f[i] in '([{':
                if term != "":
                    flst.append(term)
                    term = ""
                j = i+1
                while f[j] not in ')]}':
                    term += f[j]
                    j += 1
                    i = j
                flst.append(self.plist(term))
                term = ''
            i += 1
        self.lst = flst
        return(flst)
    
    def combine_terms(self,l1):
        var1 = []
        const1 = []
        rv = []
        rc = []
        x = self.variable
        for i in range(len(l1)):
            if len(l1) == 1:
                const1.append(0)
                break
            if l1[i] == x:
                var1.append(i)
        c = 0
        c1 = 0
        if len(var1)>1:          
            for i in range(len(var1)):     
                if i in rv:
                    #print(rv)
                    c1 += 1
                    continue
                i1 = var1[i]-6*c1
                c = 0
                #print('\n','i=',i,'i1=',i1,'listv=',l1[i1+2], '\n')
                for j in range(i+1,len(var1)):
                    if j in rv:
                        c+=6
                        continue                                        
                    i2=var1[j]-c-6*c1
                    #print('g=',g,'i2=',i2)
                    #print('j=',j,'i2=',i2, 'listv=',l1[i2+2],'len(l1)=',len(l1))
                    if l1[i1+2]==l1[i2+2]:
                        l1[i1-2]=str(float(l1[i1-2])+float(l1[i2-2]))
                        del l1[i2-3:i2+3]
                        c+=6
                        rv.append(j)
        c = 0
        for i in range(len(l1)):
            if len(l1)==1:
                break
            if 0<i<len(l1)-1:
                if l1[i-1] in '+-' and l1[i+1] in '+-':
                    const1.append(i)
            elif i==0 and l1[i+1] in '+-':
                const1.append(i)
            elif i==len(l1)-1 and l1[i-1]  in '+-':
                const1.append(i)
        if len(const1)>1:
            for i in range(len(const1)):
                #print(l1,c)
                if i in rc:
                    continue
                for j in range(i+1,len(const1)):
                    i1=const1[i]
                    i2=const1[j]-c
                    l1[i1]=str(float(l1[i1])+float(l1[i2]))
                    del l1[i2-1:i2+1]
                    c+=2
                    rc.append(j)
        g=''
        for y in l1:
            g+=y
        #print(g)    
        return(l1)

    def list_prod(self,l1,l2):
        prod=[]
        var1=[]
        const1=[]
        var2=[]
        const2=[]
        x=self.variable
        for i in range(len(l1)):
            if len(l1)==1:
                const1.append(0)
                break
            if l1[i]==x:
                var1.append(i)
            if 0<i<len(l1)-1:
                if l1[i-1] in '+-' and l1[i+1] in '+-':
                    const1.append(i)
            elif i==0 and l1[i+1] in '+-':
                const1.append(i)
            elif i==len(l1)-1 and l1[i-1]  in '+-':
                const1.append(i)
        for i in range(len(l2)):
            if len(l2)==1:
                const2.append(0)
                break
            if l2[i]==x:
                var2.append(i)
            if 0<i<len(l2)-1:
                if l2[i-1] in '+-' and l2[i+1] in '+-':
                    const2.append(i)
            elif i==0 and l2[i+1] in '+-':
                const2.append(i)
            elif i==len(l2)-1 and l2[i-1] in '+-':
                const2.append(i)  
        #print(var1,const1,var2,const2)        
        if len(var1)!=0 and len(var2)!=0:
            for i in var1:
                for j in var2:
                    prod.append(str(float(l1[i-2])*float(l2[j-2])))
                    prod.append('*')
                    prod.append(x)
                    prod.append('^')
                    prod.append(str(int(l1[i+2])+int(l2[j+2])))
                    prod.append('+')
        if len(var1)!=0 and len(const2)!=0:
            for i in var1:
                for j in const2:
                    prod.append(str(float(l1[i-2])*float(l2[j])))
                    prod.append('*')
                    prod.append(x)
                    prod.append('^')
                    prod.append(l1[i+2])
                    prod.append('+')
        if len(var2)!=0 and len(const1)!=0:
            for i in var2:
                for j in const1:
                    prod.append(str(float(l2[i-2])*float(l1[j])))
                    prod.append('*')
                    prod.append(x)
                    prod.append('^')
                    prod.append(l2[i+2])
                    prod.append('+')
        if len(const1)!=0 and len(const2)!=0:
            for i in const1:
                for j in const2:
                    prod.append(str(float(l1[i])*float(l2[j])))
                    prod.append('+')
        if prod[-1]=='+':
            prod.pop(-1)
        prod=self.combine_terms(prod)
        return(prod) 
    
    def list_power(self,lst1,n):
        n=int(n)
        power = [x for x in lst1]
        for i in range(1,n):
            power = self.list_prod(power,lst1)
        g = ''
        for x in power:
            g += x
        #print(g)
        return(power)
    
    def distribute_c(self,l1,c):
        c=float(c)
        var1=[]
        const1=[]
        x=self.variable
        for i in range(len(l1)):
            if len(l1)==1:
                const1.append(0)
                break
            if l1[i]==x:
                var1.append(i)
            if 0<i<len(l1)-1:
                if l1[i-1] in '+-' and l1[i+1] in '+-':
                    const1.append(i)
            elif i==0 and l1[i+1] in '+-':
                const1.append(i)
            elif i==len(l1)-1 and l1[i-1]  in '+-':
                const1.append(i)
        for i in var1:
            l1[i-2]=str(float(l1[i-2])*c)
        for i in const1:
            l1[i]=str(float(l1[i])*c)
        return(l1)
    
    def distribute_x(self,l1,n):
        self.combine_terms(l1)
        n=int(n)
        var1=[]
        const1=[]
        x=self.variable
        for i in range(len(l1)):
            if len(l1)==1:
                const1.append(0)
                break
            if l1[i]==x:
                var1.append(i)
            if 0<i<len(l1)-1:
                if l1[i-1] in '+-' and l1[i+1] in '+-':
                    const1.append(i)
            elif i==0 and l1[i+1] in '+-':
                const1.append(i)
            elif i==len(l1)-1 and l1[i-1]  in '+-':
                const1.append(i)
        for i in var1:
            l1[i+2]=str(n+int(l1[i+2]))
        for i in const1:
            l1.insert(i+1,str(n))
            l1.insert(i+1,"^")
            l1.insert(i+1,x)
            l1.insert(i+1,"*")
        return(l1)

    def simplify(self):
        plst = self.plist()
        x = self.variable
        #do exponents
        i = 0
        #print(plst)
        while i < len(plst)-1:
            if type(plst[i])==list and plst[i+1]=='^':
                plst[i]=self.list_power(plst[i],plst[i+2])
                plst.pop(i+1)
                plst.pop(i+1)
            i+=1
        #do products
        i = 0
        while i<len(plst)-2:
            if type(plst[i])==list and type(plst[i+2])==list and plst[i+1]=='*':
                plst[i]=self.list_prod(plst[i],plst[i+2])
                plst.pop(i+1)
                plst.pop(i+1)
                i-=1
            i+=1
        #do x left
        i=5
        while i<len(plst):
            if type(plst[i])==list and plst[i-4]==x:
                plst[i-4]=self.distribute_x(plst[i],plst[i-2])
                plst.pop(i-3)
                plst.pop(i-3)
                plst.pop(i-3)
                plst.pop(i-3)
            i+=1
        #do x right
        i=0
        while i<len(plst)-6:
            if type(plst[i])==list and plst[i+4]==x:
                plst[i]=self.distribute_c(plst[i],plst[i+2])
                plst[i]=self.distribute_x(plst[i],plst[i+6])
                plst.pop(i+1)
                plst.pop(i+1)
                plst.pop(i+1)
                plst.pop(i+1)
                plst.pop(i+1)
                plst.pop(i+1)
            i+=1
        #print(plst)  
        #do constants on right
        i=0
        while i<len(plst)-1:
            #print('I got here',i)
            if i==len(plst)-2:
                if type(plst[i])==list:
                    plst[i]=self.distribute_c(plst[i],plst[i+1])
                    plst.pop(i+1)
            else:
                if type(plst[i])==list and plst[i+3] in '+-':
                    plst[i]=self.distribute_c(plst[i],plst[i+2])
                    plst.pop(i+1)
                    plst.pop(i+1)
            i+=1
        #do constants on left
        i=2
        while i<len(plst):
            #print('I am here',i)
            if i==2 and  type(plst[i])==list and plst[i-1]=='*':
                plst[i-2]=self.distribute_c(plst[i],plst[i-2])
                plst.pop(i-1)
                plst.pop(i-1)
                i-=2
            elif i>2 and type(plst[i])==list and plst[i-1]=='*' and plst[i-3] in '+-':
                plst[i-2]=self.distribute_c(plst[i],plst[i-2])
                plst.pop(i-1)
                plst.pop(i-1)
                i-=2
            i+=1

        l=[]
        i=0
        while i<len(plst):
           if type(plst[i])==list:
               l=[x for x in plst[i]]
               plst[i]=l[0]
               l=l[len(l):0:-1]
               for j in l:
                   plst.insert(i+1,j)
           i+=1
        self.combine_terms(plst)
        g=''
        for a in plst:
            g+=a
        return(g)
    
    
    def evaluate(self,num):
        value=0
        flst=self.plist()
        for i in range(len(flst)):
            if flst[i] == self.variable:
                flst[i]=num
        #print(flst)
        i=0
        while i<= len(flst)-1:
            if flst[i]=='^':
                value=float(flst[i-1])**float(flst[i+1])
                flst[i]=value
                flst.pop(i-1)
                flst.pop(i)
                i-=1
            #print(flst," in ^")
            i+=1
        i=0
        if flst[0]=='-':
            value=-1*float(flst[1])
            flst[0]=value
            flst.pop(1)
        #print(flst)
        i=0
        while i<= len(flst)-1:
            if flst[i]=='*':
                value=float(flst[i-1])*float(flst[i+1])
                flst[i]=value
                flst.pop(i-1)
                flst.pop(i) 
                i-=1
                #print(flst," in *")
            elif flst[i]=='/':
                value=float(flst[i-1])/float(flst[i+1])
                flst[i]=value
                flst.pop(i-1)
                flst.pop(i)
                i-=1
                #print(flst," in /")
            i+=1

        i=0
        while i<= len(flst)-1:
            #print(flst)
            if flst[i]=='+':
                value=float(flst[i-1])+float(flst[i+1])
                flst[i]=value
                flst.pop(i-1)
                flst.pop(i)
                i-=1
                #print(flst," in +")
            elif flst[i]=='-' and i!=0:
                value=float(flst[i-1])-float(flst[i+1])
                flst[i]=value
                flst.pop(i-1)
                flst.pop(i)
                i-=1
                #print(flst, " in -")
            i+=1
        i=0
        #print(1)
        return(flst[0])

    def derivative(self):
        f=""
        flst=self.plist()
        i=0
        if self.variable not in flst:
            flst=['0']
        
        while i < len(flst):
            if len(flst)==1:
                flst[0]='0'
                break
            if flst[i]=='^':
                if flst[i+1]!='1':
                    flst[i-3]=str(float(flst[i-3])*float(flst[i+1]))
                    flst[i+1]=str(int(flst[i+1])-1)
                else:
                    #flst[i-1]='1'
                    del flst[i-2:i+2]
                    i-=2
            elif i==0 and flst[1] in ['+','-']:
                flst[0]='0'
            elif i==len(flst)-1 and flst[-2] in ['+','-']:
                flst[-1]='0'
            elif flst[i-1] in ['+','-'] and flst[i+1] in ['+','-']:
                flst[i]='0'
            i+=1
        
        for a in flst:
            f+=a
        self.prime=Polynomial(f)
        return(f)

    def indefinite(self):
        f=""
        flst=self.plist()
        i=0
        if self.variable not in flst:
            flst=[str(self.evaluate(0))]   
        while i < len(flst):
            if len(flst)==1:
                if flst[0]=='0':
                    flst[0]='1'
                else:
                    flst.append(self.variable)
                break
            if flst[i]=='^':
                flst[i+1]=str(int(flst[i+1])+1)
                flst[i-3]=str(float(flst[i-3])/float(flst[i+1]))
            elif i==0 and flst[1] in ['+','-']:
                flst.insert(1,'x')
                i+=1
            elif i==len(flst)-1 and flst[-2] in ['+','-']:
                flst.append('x')
                i+=1
            elif flst[i-1] in ['+','-'] and flst[i+1] in ['+','-']:
                flst.insert(i+1,'x')
                i+=1
            i+=1
        for a in flst:
            f+=a
        self.anti=Polynomial(f)
        print(f)  
    def definite(self,a=None,b=None):
        if a==None:
            a=float(input('Enter a: \n'))
            b=float(input('Enter b: \n'))
        self.indefinite()
        return(self.anti.evaluate(b)-self.anti.evaluate(a))
    
    #make the better
    def optimize(self,a=None,b=None):
        if a==None:
            a=float(input("Input a: \n"))
            b=float(input("Input b: \n"))
        lst=[]
        n=100000
        deltaX=(b-a)/n
        for i in range(n+1):
            lst.append(self.evaluate(a+i*deltaX))
        maximum=max(lst)
        minimum=min(lst)
        print('max is approximately', maximum, '\n min is approximately', minimum)
    
    def roots(self,a=None):
        if a==None:
            a=float(input("Guess:\n"))
        self.derivative()
        self.prime.derivative()
        n=0
        while n<100000 and self.evaluate(a)>.000000000000000000000000000000000000001:
            f=float(self.evaluate(a))
            fprime=float(self.prime.evaluate(a))
            f2prime=float(self.prime.prime.evaluate(a))
            a=a-(2*f*fprime)/(2*fprime**2-f*f2prime)
            n+=1
        f=float(self.evaluate(a))
        a=round(a,7)
        return a
        # print('I did n=',n,' iterations','\n root, a, is approximately',a,'\n f(a) is approximately', f)


                
                


    