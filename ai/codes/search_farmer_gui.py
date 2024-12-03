import tkinter as tk
from tkinter import messagebox
from enum import IntEnum
from collections import deque

class Move(IntEnum):
    F = 0  # farmer
    W = 1  # wolf
    G = 2  # goat
    C = 3  # cabbage

class Solution:
    def is_fail(self, state):
        if (state[Move.W] == state[Move.G] and state[Move.F] != state[Move.W]): return True
        if (state[Move.C] == state[Move.G] and state[Move.F] != state[Move.C]): return True
        return False

    def successors(self, state): 
        possible_actions = [[Move.F]]
        for i in range(Move.W, Move.C + 1):
            if state[Move.F] == state[i]:
                possible_actions.append([Move.F, Move(i)])
        return possible_actions

    def execute_action(self, state, action):
        state = list(state)
        for move in action:
            state[move] = 'e' if state[move] == 'w' else 'w' 
        return tuple(state)

    def search(self, initial_state, final_state):
        self.parents = {initial_state: None}
        visited = set()
        queue = deque([initial_state])
        while queue:
            current = queue.popleft()
            if current == final_state:
                path = []
                state = current
                while self.parents[state] is not None:
                    path.append(state)
                    state = self.parents[state]
                path.append(state)
                return path[::-1]
            visited.add(current)
            for action in self.successors(current):
                next_state = self.execute_action(current, action)
                if next_state not in visited and not self.is_fail(next_state):
                    self.parents[next_state] = current
                    queue.append(next_state)
        return None

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("River Crossing Puzzle")
        
        self.colors = {
            'water': '#4A90E2',
            'bank': '#8BC34A',
            'sky': '#E3F2FD',
            'boat': '#795548',
            'farmer': '#FFA000',
            'wolf': '#607D8B',
            'goat': '#9E9E9E',
            'cabbage': '#43A047'
        }
        
        self.root.configure(bg=self.colors['sky'])
        self.canvas = tk.Canvas(self.root, width=800, height=500, 
                              bg=self.colors['sky'], highlightthickness=0)
        self.canvas.pack(pady=20)

        self.button_frame = tk.Frame(self.root, bg=self.colors['sky'])
        self.button_frame.pack(pady=10)
        
        self.prev_button = tk.Button(self.button_frame, text="← Previous",
                                   command=self.prev_step, font=("Arial", 12),
                                   bg='white', relief=tk.RAISED)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = tk.Button(self.button_frame, text="Next →",
                                   command=self.next_step, font=("Arial", 12),
                                   bg='white', relief=tk.RAISED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        solution = Solution()
        self.path = solution.search(('w', 'w', 'w', 'w'), ('e', 'e', 'e', 'e'))
        if not self.path:
            messagebox.showerror("Error", "No solution found!")
            return
            
        self.state_index = 0
        self.animation_id = None
        self.boat_position = 0
        self.current_state = self.path[0]
        self.next_state = self.path[1] if len(self.path) > 1 else None
        self.draw_scene()

    def draw_scene(self):
        self.canvas.delete("all")
        
        # Background
        self.canvas.create_rectangle(0, 0, 800, 500, fill=self.colors['water'])
        self.canvas.create_rectangle(0, 0, 200, 500, fill=self.colors['bank'])
        self.canvas.create_rectangle(600, 0, 800, 500, fill=self.colors['bank'])
        
        boat_x = 200 + (400 * self.boat_position)
        
        # Draw boat
        y = 250
        points = [boat_x - 40, y, boat_x + 40, y, boat_x + 30, y + 30, boat_x - 30, y + 30]
        self.canvas.create_polygon(points, fill=self.colors['boat'], smooth=True)

        # Draw characters
        chars = [
            ("Farmer", self.colors['farmer']),
            ("Wolf", self.colors['wolf']),
            ("Goat", self.colors['goat']),
            ("Cabbage", self.colors['cabbage'])
        ]
        
        for i, (name, color) in enumerate(chars):
            # Determine if character is moving with boat
            is_moving = False
            if self.next_state:
                if self.current_state[i] != self.next_state[i]:
                    is_moving = True

            if is_moving:
                x = boat_x + (-20 if self.current_state[i] == 'w' else 20)
            else:
                x = 100 if self.current_state[i] == 'w' else 700
            
            y = 200 + i * 50
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
            self.canvas.create_text(x, y, text=name, font=("Arial", 10, "bold"), fill="white")

        # Update buttons
        self.prev_button.config(state=tk.NORMAL if self.state_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.state_index < len(self.path) - 1 else tk.DISABLED)

    def animate_boat(self, target_position):
        if abs(self.boat_position - target_position) < 0.05:
            self.boat_position = target_position
            self.draw_scene()
            self.animation_id = None

            # Update current and next states after boat reaches the target position
            if target_position == 1:
                self.current_state = self.path[self.state_index]
                self.next_state = self.path[self.state_index + 1] if self.state_index < len(self.path) - 1 else None

            return

        self.boat_position += 0.05 if target_position > self.boat_position else -0.05
        chars = [
            ("Farmer", self.colors['farmer']),
            ("Wolf", self.colors['wolf']),
            ("Goat", self.colors['goat']),
            ("Cabbage", self.colors['cabbage'])
        ]
        # Update character positions based on boat movement
        for i, (name, color) in enumerate(chars):
            if self.current_state[i] != self.next_state[i]:  # Character is moving with the boat
                x = self.boat_position * 400 + (-20 if self.current_state[i] == 'w' else 20)
            else:
                x = 100 if self.current_state[i] == 'w' else 700

            y = 200 + i * 50
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
            self.canvas.create_text(x, y, text=name, font=("Arial", 10, "bold"), fill="white")

        self.draw_scene()
        self.animation_id = self.root.after(50, lambda: self.animate_boat(target_position))

    def next_step(self):
        if self.state_index < len(self.path) - 1 and not self.animation_id:
            self.state_index += 1
            self.animate_boat(1 if self.path[self.state_index][Move.F] == 'e' else 0)

    def prev_step(self):
        if self.state_index > 0 and not self.animation_id:
            self.state_index -= 1
            self.animate_boat(1 if self.path[self.state_index][Move.F] == 'e' else 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
