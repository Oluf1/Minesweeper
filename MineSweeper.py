import tkinter as Tk
from tkinter import ttk 
import random
import time 
class Minesweeper_main():
    def __init__(self):
        self.root = Tk.Tk()
        self.field_list = []
        self.combodiffs_list = ["Easy","Medium","Hard"]
        self.diffs_list = [(9,10),(16,40),(26,120)]
        self.revealed = []
        self.flagged = []
        self.buttons = {}
        self.mines = []
        
        self.root.geometry("300x250")
        
        self.diffs_box = ttk.Combobox(self.root,values=self.combodiffs_list)
        self.get_diffbtn = ttk.Button(self.root,command=self.pick_diff,text="Start")
            
        
        self.diffs_box.pack()
        self.get_diffbtn.pack()
        self.root.mainloop() 
    def generate_field(self,diff):
        
        n = diff[0]
        self.field_size = n
        self.field_list = [[0 for _ in range(n)] for _ in range(n)]

        for _ in range(diff[1]):
            while True:
                x, y = random.randint(0, n-1), random.randint(0, n-1)
                if self.field_list[x][y] == 0:  
                    self.field_list[x][y] = 20  

                    
                    richtungen = [(-1, -1), (-1, 0), (-1, 1),
                                ( 0, -1),          ( 0, 1),
                                ( 1, -1), ( 1, 0), ( 1, 1)]
                    for dx, dy in richtungen:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            if self.field_list[nx][ny] != 20:
                                self.field_list[nx][ny] += 1
                    break
        self.place_buttons(n,diff)

    def place_buttons(self,buttoncount_x,diff):
        b_size= 20
        self.root.geometry(f"{b_size*buttoncount_x+25}x{b_size*buttoncount_x+50}")
        self.root.title(f"difficulty:{self.combodiffs_list[self.diffs_list.index(diff)]}")
        self.diffs_box.pack_forget()
        self.get_diffbtn.pack_forget()
        for x in range(buttoncount_x):
            for y in range(buttoncount_x):
                new_button = Tk.Button(self.root,bg="gray")
                new_button.config(command= lambda ax=x,ay=y,btn=new_button:self.on_pressed(ax,ay,btn))
                self.buttons[(x,y)] = new_button
                new_button.place(x=b_size*x+2,
                                 y=b_size*y+2,
                                 height=b_size,width=b_size
                                 )
    def on_pressed(self,pos_x,pos_y,button):
        if (pos_x,pos_y) in self.flagged and self.field_list[pos_x][pos_y]==20:
            self.lost(pos_x,pos_y)
        elif (pos_x,pos_y) in self.flagged:
            
            if  self.field_list[pos_x][pos_y] ==0:
                self.on_revealed_zero(pos_x,pos_y,"on pressed",False)
            else: 
                self.revealed.append((pos_x,pos_y))
                self.on_revealed_exno(pos_x,pos_y)
            
        else:
            button.config(bg="red")
            self.flagged.append((pos_x,pos_y))
            
            
    def on_revealed_zero(self,pos_x,pos_y,dbs,num_pressed):
        #print(dbs)
        if(pos_x,pos_y) not in self.revealed and self.field_list[pos_x][pos_y] ==0 :
            self.buttons[(pos_x,pos_y)].place_forget()
            self.revealed.append((pos_x,pos_y))
            richtungen = [(-1, -1), (-1, 0), (-1, 1),
                        ( 0, -1),          ( 0, 1),
                        ( 1, -1), ( 1, 0), ( 1, 1)]
            for dx, dy in richtungen:
                nx, ny = pos_x + dx, pos_y + dy
                if 0 <= nx < self.field_size and 0 <= ny < self.field_size:
                    self.on_revealed_zero(nx,ny,"on_zero",False)
        elif (pos_x,pos_y) not in self.revealed and self.field_list[pos_x][pos_y] !=20 :
            self.on_revealed_exno(pos_x,pos_y)
            print("dbug 2")
        elif (pos_x,pos_y) not in self.flagged and (pos_x,pos_y)==20:
            self.lost(pos_x,pos_y)
        elif  (pos_x,pos_y) in self.revealed and num_pressed== True:
            richtungen = [(-1, -1), (-1, 0), (-1, 1),
                        ( 0, -1),          ( 0, 1),
                        ( 1, -1), ( 1, 0), ( 1, 1)]
            for dx, dy in richtungen:
                nx, ny = pos_x + dx, pos_y + dy
                if 0 <= nx < self.field_size and 0 <= ny < self.field_size:
                    if (nx,ny) not in self.revealed:
                        self.on_revealed_zero(nx,ny,"on_zero_2",False)
    
    def lost(self,pos_x,pos_y):
        print("womp womp wom")
    def win(self):
        print("you Won!")
    def on_revealed_exno(self,pos_x,pos_y):
        if (pos_x,pos_y) in self.flagged:
            self.flagged.remove((pos_x,pos_y))
        self.buttons[(pos_x,pos_y)].config(command=lambda x = pos_x, y=pos_y: self.on_revealed_zero(x,y,"on Exno",True),
        text=self.field_list[pos_x][pos_y],
        bg="white"   
        )
        self.revealed.append((pos_x,pos_y))
        
                    
                    
    def pick_diff(self):
        diff_temp = self.diffs_box.get()
        for i,e in enumerate(self.combodiffs_list):
            if e == diff_temp:
                diff_temp =self.diffs_list[i]
        if diff_temp in self.combodiffs_list:
            print("Error: Not a Difficulty")
        self.generate_field(diff_temp)
        
                           

if __name__ == "__main__":
    Minesweeper_main()
    
