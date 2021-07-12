from tkinter.constants import END
from tkinter import messagebox
import numpy as np 
import tkinter as tk
import os
import sys
import json
from numpy.random import randint

LARGE_FONT = ("Verdana", 12)
FG='blue'
FONT=('Arial',16,'bold')
BACKROUND = '#49A'
D = {}
D.update({'fg': FG})
D.update({'font': FONT})

        
def save_jason(data,path):
    
    with open(path, 'w') as f:
        json.dump(data, f)

    return

def load_jason(path):
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    return data

class GAME(tk.Tk):

    def __init__(self):
        
        super().__init__()
        self.adding()

        self.NAME = None
        self.LEVEL = None
        self.SCORE = 0

        self.container = tk.Frame(self)
        self.container.pack(side="top")

        # self.container.grid_rowconfigure(0, weight=1)
        # self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Reg_Page, Main_page, Score_page):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Reg_Page)

    def adding(self):

        self.option_add('*Font',FONT) 
        self.option_add('*Backround',BACKROUND)
        self.option_add('*Foreground',FG)
        self.option_add('*Frame.geometry','700x350') 
        self.option_add("*Button.relief","sunken")
        
        return

    def error(self,phrase):

        error_window = tk.Tk()
        error_frame = tk.Frame(master = error_window)        
        error_label = tk.Label(master = error_frame ,
                                    text= phrase                                 
                                    )
        error_frame.pack()
        error_label.pack()

        error_window.mainloop()
        return

    def show_frame(self, cont):
    
        frame = self.frames[cont]
        frame.tkraise()

class Reg_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.start_label = tk.Label(self, text="Regisration page ")
        self.start_label.grid(row=0)
         
        self.reg_name= tk.Label(self,text = 'name')
        self.reg_name_entry = tk.Entry(self)
        self.reg_name.grid(row= 1,column= 1)
        self.reg_name_entry.grid(row=1,column= 0)

        self.reg_level = tk.Label(self, text = 'pick level')
        self.level_vars = [ tk.IntVar(self) for var in range(4) ]
        self.reg_level_bars = [ tk.Checkbutton(self,text = str(i), variable= self.level_vars[i]) for i in range(4) ]
        
        self.reg_level.grid(row=1, column= 1)
        [self.reg_level_bars[i].grid(row= 2+i, column=2) for i in range(4) ]

        self.button = tk.Button(self, text="START",
                            command= lambda: self.check_reg(controller) )
        self.button.grid(row = 6)

        self.button2 = tk.Button(self, text="QUIT",
                            command= lambda: sys.exit())
        self.button2.grid(row = 7)
        
        return

    def check_reg(self,controller):
        name = self.reg_name_entry.get()
        level_vars = [ self.level_vars[i].get() for i in range(4) ] 
        
        #check name
        if any(name) == False:
            self.reg_name_entry.delete(0,END)
            controller.error('name not valid use letters')
        #check levels
        sum =0
        one_val = False
        i=0
        while i < len(level_vars):
            if level_vars[i] == 1:
                sum +=1
                _level = i
            i += 1
        if sum == 1:
            one_val = True
            
        if one_val != True:
            [ self.level_vars[i].set(0  ) for i in range(4) ] 
            controller.error('select one level')

        else:
            controller.LEVEL = _level
            controller.NAME = name
            controller.show_frame(Main_page)

        return 

class Main_page(tk.Frame):

    def __init__(self, parent, controller):
        #init params
        self.math_sym = ['+','-','x','/']
        self.numbers = [ i+1 for i in range(20)]
        self.answer = -1
        self.num_Qs = 2
        self.num_correct = 0
        self.current_q = 0
        self.start_already = False
        self.checked = False

        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="GAME !!!")
        self.label.grid(row = 0)

        self.equation_label = tk.Label(self, text = 'solve equation')
        self.equation_var = tk.Entry(self)
        self.equation_label.grid(row=1,column=0)
        self.equation_var.grid(row=1,column=1)

        self.answer_label = tk.Label(self, text = 'answer')
        self.number_vars = [ tk.IntVar(self) for i in range (4) ] 
        self.string_vars = [ tk.StringVar(self) for i in range (4) ] 
        self.answers = [tk.Checkbutton(self,textvariable= self.string_vars[i], variable=self.number_vars[i]) for  i in range(4) ]
        self.answer_label.grid(row=2,column=0)
        [ self.answers[i].grid(row=2+i,column=1) for i in range(4) ]

        self.counter_label = tk.Label(self, text = 'counter')
        self.counter_var = tk.StringVar(self)
        self.counter_text = tk.Label(self, textvariable= self.counter_var)
        self.counter_label.grid(row = 2, column=3)
        self.counter_text.grid(row = 2, column=4)

        self.button1 = tk.Button(self, text="start",
                            command=lambda: self.start(controller.LEVEL))
        self.button1.grid(row=4)

        self.button2 = tk.Button(self, text="check answer",
                            command=lambda: self.check(controller))
        self.button2.grid(row=4, column = 3)

        self.comment_var = tk.StringVar(self)
        self.comment_text = tk.Label(self, textvariable= self.comment_var)
        self.comment_text.grid(row =8)
        
        self.button3 = tk.Button(self, text="next",
                            command=lambda: self.next(controller))
        self.button3.grid(row=9)

    def start(self,_level):
        #if already started
        if self.start_already :
            return
        #start game!
        _answer = self.initiate_game(_level)
        self.current_q = 1
        #game mode
        self.start_already = True
        
        return
    
    def check(self,controller):
        #if already checked answer for this q
        if self.checked:
            return
        #if correct 
        if self.check_answer(controller) :
            self.num_correct +=1
            controller.SCORE = self.num_correct
            self.comment_var.set('well done U R correct!!!')
            
            #refresh
            if any(self.counter_var.get()):
                self.counter_var.set('')
            #set
            self.counter_var.set(str(self.num_correct)+' / '+str(self.current_q))
            
            #check if finnished
            if self.current_q == self.num_Qs :
                self.checked = True
                self.current_q +=1 
                controller.error('finnished game!')
                
            #count checkings
            self.current_q +=1            
        #not correct :(
        else:   
            self.counter_var.set(str(self.num_correct)+' / '+str(self.current_q))
            self.current_q +=1 
            
            self.comment_var.set(' not so bad, but not so true...')
        
        self.checked = True

        return

    def next(self,controller):
        #if ive checked for the answer for this current q
        if not self.checked:
            return 
        #if havent started the game
        if not self.start_already:
            controller.error('press START to start the game!')
            return
        #refresh
        self.refresh_game() 

        #if still have more question
        if self.current_q <= self.num_Qs :
            self.initiate_game(controller.LEVEL)
        #move on
        else:
            #refresh whole class
            self.refresh_game() 
            self.counter_var.set('')
            self.answer = -1
            self.num_correct = 0
            self.current_q = 0
            self.start_already = False
            self.checked = False

            controller.frames[Score_page].update_dic(controller)
            controller.frames[Score_page].make_board(controller)
            controller.show_frame(Score_page)
            
        return
    
    def initiate_game(self,_level):
    
        # refresh
        self.refresh_game()
        # make equation function
        _equation, _answer = self.make_eq(_level)
        # equation
        self.equation_var.insert(0,_equation)
        
        #answers
        self.answer = np.random.randint(0,4)
        rand_answers = np.random.randint(np.round(_answer-int(_answer/2)),np.round(_answer+int(_answer/2)),4)
        self.string_vars[self.answer].set(str(_answer))
        #set answers in window
        for j in range(len(rand_answers)):
            if j != self.answer:
                self.string_vars[j].set(str(rand_answers[j]))

        return 

    def check_answer(self,controller):

        #check if one answer
        sum =0
        one_val = False
        i=0
        while i < len(self.number_vars):
            if self.number_vars[i].get() == 1:
                sum +=1
                _answer_guess = i
            i += 1

        if sum == 1:
            one_val = True
    
        if one_val != True:
            [ self.number_vars[i].set(0 ) for i in range(4) ] 
            controller.error('select one level')

        #check answer
        if one_val == True:
            if self.answer == _answer_guess :
                return True
            else:
                return False
   
        else:
            return

    def make_eq(self, _level):
        #random numbers
        #equation phrase = str , answer= ...answer for this eq

        if _level == 0 :
            num1 = np.random.randint(10,20)
            num2 = np.random.randint(1,11)

            wild_card = np.random.randint(0,1)
            symbol = self.math_sym[wild_card]
            equation_phrase = str(num1)+''+symbol+''+str(num2) +' = ?'
            answer = self.solve(num1,symbol,num2)
        
        if _level == 1 :
            num1 = np.random.randint(10,20)
            num2 = np.random.randint(1,11)

            wild_card = np.random.randint(0,2)
            symbol = self.math_sym[wild_card]
            equation_phrase = str(num1)+''+symbol+''+str(num2) +' = ?'
            answer = self.solve(num1,symbol,num2)
        
        if _level == 2 :
            num1 = np.random.randint(10,20)
            num2 = np.random.randint(1,11)

            wild_card = np.random.randint(0,3)
            symbol = self.math_sym[wild_card]
            equation_phrase = str(num1)+''+symbol+''+str(num2) +' = ?'
            answer = self.solve(num1,symbol,num2)
        
        if _level == 3 :
            num1 = np.random.randint(10,20)
            num2 = np.random.randint(1,11)

            wild_card = np.random.randint(0,4)
            symbol = self.math_sym[wild_card]
            equation_phrase = str(num1)+''+symbol+''+str(num2) +' = ?'
            answer = self.solve(num1,symbol,num2)
        
        return equation_phrase , answer

    def solve(self,_num1,_symbol,_num2):
        #make the equation and solve
        if _symbol == '+':
            _answer = _num1+_num2 
        elif _symbol == '-'  :
            _answer = _num1-_num2 
        elif _symbol == 'x':
            _answer = _num1*_num2
        elif _symbol == '/':
            _answer = _num1/_num2
        else:
            return
        return _answer

    def refresh_game(self):
        #refresh
        if any(self.equation_var.get()) ==True :
            self.equation_var.delete(0,END)

        for j in range(len(self.answers)):
            self.string_vars[j].set('')
        
        [ self.number_vars[j].set(0) for j in range(len(self.number_vars)) ]
        
        self.comment_var.set('')
        self.answer = -1
        self.checked = False

        return
     
class Score_page(tk.Frame):

    def __init__(self, parent, controller):
        
        self.dic_open = False
        
        tk.Frame.__init__(self, parent)
        self.score_label = tk.Label(self, text="SCORE BOARD!!!")
        self.score_label.grid(row =0)
        self.score_level_var = tk.StringVar(self)
        self.score_level = tk.Label(self, textvariable=self.score_level_var)
        self.score_level.grid(row =1)

        #dictionary of score_board
        score_folder = [ x for x in os.listdir(os.getcwd()) if x == 'game_board' ] 
        
        if score_folder != []:
            self.score_dic =load_jason('game_board')
        else:
            self.score_dic = self.make_dict()
        
        # code for creating table
        self.e = [ tk.Entry(self) for i in range (10)] 
        m=0
        for i in range(5):
            for j in range(2):
                    self.e[m].grid(row=i+1, column=j)
                    m +=1

        #buttons             
        button1 = tk.Button(self, text="Back to start",
                        command=lambda: controller.show_frame(Reg_Page))
        button1.grid(row=6)

        button2 = tk.Button(self, text= "QUIT",
                        command= self.finnish_game )
        button2.grid(row = 7)

        return

    def make_dict(self):
        
        my_dic = dict()
        
        for j in range(4):
            level_dic = dict()
            for i in range(5):
                level_dic.update({str(i) : ('name',0)})

            my_dic.update({str(j) : level_dic}) 

        return my_dic

    def update_dic(self,_controller):

        if _controller.LEVEL == None :
            return
                    
        level_dic = self.score_dic[str(_controller.LEVEL)]
        names = [ level_dic[str(i)][0] == 'name' for i in range(5) ] 
        # if dict empty
        if all(names):
            level_dic['0'] = (_controller.NAME,_controller.SCORE)
        #if not empty
        else:
            i=0
            done = False
            len_dic = len(level_dic.keys())
            while i <len_dic and not done :
                if level_dic[str(i)][1] <= _controller.SCORE:
                    current_score = level_dic[str(i)]
                    level_dic[str(i)] = (_controller.NAME,_controller.SCORE)
                    
                    j =  i+1
                    while j < len_dic:
                        next_score = level_dic[str(j)]
                        level_dic.update({str(j) : current_score})
                        current_score = next_score
                        j +=1
                        done = True
                else:
                    i +=1

        self.score_dic.update({str(_controller.LEVEL) : level_dic})
            
        if self.score_level_var.get() != '':
            self.score_level_var.set('')

        self.score_level_var.set('level: '+str(_controller.LEVEL))       
        
        return
    
    def make_board(self,_controller):
        
        if _controller.LEVEL == None:
            return
        before = [ x.get() for x in self.e ]
        before = [x == '' for x in before ]

        if not all(before):
            m=0
            for i in range(5):
                for j in range(2):
                    self.e[m].delete(0,END) 
                    m += 1

        level_scores = self.score_dic[str(_controller.LEVEL)]
        m=0
        for i in range(5):
            for j in range(2):
                self.e[m].insert(0,str(level_scores[str(i)][j]) )
                m += 1
        
        return
    
    def finnish_game(self):

        save_jason(self.score_dic,'game_board')
        sys.exit()
        return 

app = GAME()
app.mainloop()