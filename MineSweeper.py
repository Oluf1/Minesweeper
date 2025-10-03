import tkinter as Tk
from tkinter import ttk 
import random
import time
class Minesweeper_main():
    def __init__(self):
        self.root = Tk.Tk()
        self.field_list = []
        self.combodiffs_list = ["Easy","Medium","Hard"]
        self.diffs_list = [(9,10),(16,40),(26,100)]
        self.revealed = set()
        self.flagged = set()
        self.buttons = {}
        self.mines = set()
        self.image_mine = Tk.PhotoImage(file="Minesweeper/MineSweeper_Flagge.png")
        self.richtungen=  [(-1, -1), (-1, 0), (-1, 1),
                    ( 0, -1),          ( 0, 1),
                        ( 1, -1), ( 1, 0), ( 1, 1)]
        
        self.root.geometry("300x250")
        
        self.diffs_box = ttk.Combobox(self.root,values=self.combodiffs_list)
        self.get_diffbtn = ttk.Button(self.root,command=self.pick_diff,text="Start")
            
        
        self.diffs_box.pack()
        self.get_diffbtn.pack()
    def generate_field(self,diff):
        
        n = diff[0]
        self.field_size = n
        self.field_list = [[0 for _ in range(n)] for _ in range(n)]

        for _ in range(diff[1]):
            while True:
                x, y = random.randint(0, n-1), random.randint(0, n-1)
                if self.field_list[x][y] != -1:  
                    self.field_list[x][y] = -1  
                    self.mines.add((x,y))
                    
                    
                    for dx, dy in self.richtungen:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            if self.field_list[nx][ny] != -1:
                                self.field_list[nx][ny] += 1
                    break
        self.place_buttons(n,diff)

    def place_buttons(self,buttoncount_x,diff):
        b_size= 25
        self.root.geometry(f"{b_size*buttoncount_x}x{b_size*buttoncount_x+50}")
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
        if (pos_x,pos_y) in self.flagged and self.field_list[pos_x][pos_y]==-1:
            self.lost(pos_x,pos_y)
        elif (pos_x,pos_y) in self.flagged:
            
            if  self.field_list[pos_x][pos_y] ==0:
                self.on_revealed_zero(pos_x,pos_y)
            else: 
                self.revealed.add((pos_x,pos_y))
                self.on_revealed_exno(pos_x,pos_y)
            
        else:
            button.config(bg="red")
            print(self.field_list[pos_x][pos_y])
            self.flagged.add((pos_x,pos_y))
            print(sorted(self.flagged))
            if self.flagged==self.mines:
                self.win()
            
    def on_revealed_pressed(self,pos_x,pos_y):
        self.buttons[(pos_x,pos_y)].config(state="disabled")
        
        for dx, dy in self.richtungen:
            nx, ny = pos_x + dx, pos_y + dy
            if 0 <= nx < self.field_size and 0 <= ny < self.field_size:
                if (nx,ny) not in self.revealed:
                    self.on_revealed_zero(nx,ny)
    def on_revealed_zero(self,pos_x,pos_y):
        #print(dbs)
        print("tst1")
        if self.flagged==self.mines:
            self.win()
        if(pos_x,pos_y) not in self.revealed and self.field_list[pos_x][pos_y] ==0 :
            
            self.flagged.discard((pos_x,pos_y))
            self.buttons[(pos_x,pos_y)].config(state="disabled",bg="white",
                                               borderwidth=0,       
                                                highlightthickness=0)
            self.revealed.add((pos_x,pos_y))
            for dx, dy in self.richtungen:
                nx, ny = pos_x + dx, pos_y + dy
                if 0 <= nx < self.field_size and 0 <= ny < self.field_size:
                    self.on_revealed_zero(nx,ny)
        elif (pos_x,pos_y) not in self.revealed and  (pos_x,pos_y) not in self.mines:
            self.on_revealed_exno(pos_x,pos_y)
        elif (pos_x,pos_y) in self.mines and (pos_x,pos_y) not in self.flagged:
            self.lost(pos_x,pos_y)
        

    def on_revealed_exno(self,pos_x,pos_y):
        
        self.flagged.discard((pos_x,pos_y))
        if self.flagged==self.mines:
            self.win()
        self.buttons[(pos_x,pos_y)].config(
        command=lambda x = pos_x, y=pos_y: self.on_revealed_pressed(x,y),
        text=self.field_list[pos_x][pos_y],
        bg="white",image=None   
        )
        self.revealed.add((pos_x,pos_y))


    def lost(self, pos_x, pos_y):
    # Alle Buttons zuerst deaktivieren
        for button in self.buttons.values():
            button.config(state="disabled")

        # Buttons als Liste speichern
        buttons = list(self.buttons.values())

        def delete_next():
            if buttons:
                btn = buttons.pop(0)   
                btn.destroy()
                if buttons:
                    btn = buttons.pop(0)
                    btn.destroy()          
                self.root.after(2, delete_next)  
            else:
                
                verloren = ttk.Label(self.root, text="Du hast verloren")
                verloren.pack()

        delete_next()
    def win(self):
        print("you Won!")
        for button in self.buttons.values():
            button.config(state="disabled")

        # Buttons als Liste speichern
        buttons = list(self.buttons.values())

        def delete_nexts():
            if buttons:
                btn = buttons.pop(0)   
                btn.destroy()
                if buttons:
                    btn = buttons.pop(0)
                    btn.destroy()          
                self.root.after(2, delete_nexts)  
            else:
                
                gewonnen= ttk.Label(self.root, text="Du hast gewonnen")
                gewonnen.pack()

        delete_nexts()
        
    
        
                    
                    
    def pick_diff(self):
        difficulty_temporary = self.diffs_box.get()
        for i,e in enumerate(self.combodiffs_list):
            if e == difficulty_temporary:
                difficulty_temporary =self.diffs_list[i]
        if difficulty_temporary in self.combodiffs_list:
            print("Error: Not a Difficulty")
        self.generate_field(difficulty_temporary)
        
                           

if __name__ == "__main__":
    game = Minesweeper_main()
    game.root.mainloop()
