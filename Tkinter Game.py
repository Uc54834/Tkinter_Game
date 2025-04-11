import tkinter as tk
import random

class SimpleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Tkinter Game")
        
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()
        
        self.player = self.canvas.create_rectangle(180, 350, 220, 370, fill='blue')
        self.score = 0
        self.score_label = tk.Label(root, text=f"Score: {self.score}")
        self.score_label.pack()
        
        self.enemies = []
        self.create_enemy()
        
        # Bind keyboard events
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        
        self.game_loop()
    
    def move_left(self, event):
        self.canvas.move(self.player, -20, 0)
    
    def move_right(self, event):
        self.canvas.move(self.player, 20, 0)
    
    def create_enemy(self):
        x = random.randint(0, 350)
        enemy = self.canvas.create_oval(x, 0, x+50, 50, fill='red')
        self.enemies.append(enemy)
        self.root.after(1000, self.create_enemy)
    
    def game_loop(self):
        # Move enemies down
        for enemy in self.enemies[:]:
            self.canvas.move(enemy, 0, 10)
            pos = self.canvas.coords(enemy)
            
            # Check if enemy reached bottom
            if pos[3] >= 400:
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
            
            # Check for collision with player
            player_pos = self.canvas.coords(self.player)
            if self.check_collision(pos, player_pos):
                self.game_over()
                return
        
        self.root.after(50, self.game_loop)
    
    def check_collision(self, enemy_pos, player_pos):
        # Simple AABB collision detection
        return (enemy_pos[2] >= player_pos[0] and enemy_pos[0] <= player_pos[2] and
                enemy_pos[3] >= player_pos[1] and enemy_pos[1] <= player_pos[3])
    
    def game_over(self):
        self.canvas.create_text(200, 200, text="GAME OVER", font=('Arial', 30), fill='red')
        for enemy in self.enemies:
            self.canvas.delete(enemy)
        self.enemies.clear()

if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleGame(root)
    root.mainloop()