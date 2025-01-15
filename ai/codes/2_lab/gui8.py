import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from queue import PriorityQueue
import time

class EightPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        
        # Initialize states
        self.goalState = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]).reshape(3, 3)
        self.currentState = None
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create puzzle grid
        self.cells = []
        self.create_puzzle_grid()
        
        # Create buttons
        self.create_buttons()
        
        # Create solution display
        self.solution_text = tk.Text(self.main_frame, height=10, width=40)
        self.solution_text.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Initialize puzzle
        self.randomize_puzzle()

    def create_puzzle_grid(self):
        puzzle_frame = ttk.Frame(self.main_frame)
        puzzle_frame.grid(row=0, column=0, columnspan=3, pady=10)
        
        for i in range(3):
            for j in range(3):
                cell = ttk.Label(
                    puzzle_frame,
                    width=4,
                    padding=10,
                    relief="solid",
                    anchor="center",
                    style="Puzzle.TLabel"
                )
                cell.grid(row=i, column=j, padx=2, pady=2)
                self.cells.append(cell)
        
        # Create custom style for puzzle cells
        style = ttk.Style()
        style.configure("Puzzle.TLabel", font=('Helvetica', 20, 'bold'))

    def create_buttons(self):
        ttk.Button(
            self.main_frame,
            text="Randomize",
            command=self.randomize_puzzle
        ).grid(row=1, column=0, pady=10, padx=5)
        
        ttk.Button(
            self.main_frame,
            text="Solve",
            command=self.solve_puzzle
        ).grid(row=1, column=1, pady=10, padx=5)
        
        ttk.Button(
            self.main_frame,
            text="Clear",
            command=self.clear_solution
        ).grid(row=1, column=2, pady=10, padx=5)

    def update_display(self, state):
        for i in range(9):
            value = state.flatten()[i]
            self.cells[i].configure(text=str(value) if value != 0 else " ")

    def randomize_puzzle(self):
        self.currentState = np.random.permutation(9).reshape(3, 3)
        self.update_display(self.currentState)
        self.clear_solution()

    def clear_solution(self):
        self.solution_text.delete(1.0, tk.END)

    def solve_puzzle(self):
        if not self.is_solvable(self.currentState):
            messagebox.showwarning("Warning", "This puzzle configuration is not solvable!")
            return

        self.solution_text.delete(1.0, tk.END)
        self.solution_text.insert(tk.END, "Solving...\n")
        self.root.update()
        
        start_time = time.time()
        goalFound, prev, cost = self.astar(self.currentState, self.goalState)
        end_time = time.time()
        
        if goalFound:
            path = []
            current = tuple(self.goalState.flatten())
            while current != " ":
                path.append(np.array(current).reshape(3, 3))
                current = prev[current]
            path.reverse()
            
            self.solution_text.delete(1.0, tk.END)
            self.solution_text.insert(tk.END, f"Solution found!\nMoves required: {cost}\n")
            self.solution_text.insert(tk.END, f"Time taken: {end_time - start_time:.2f} seconds\n\n")
            
            # Animate solution
            self.animate_solution(path)
        else:
            self.solution_text.delete(1.0, tk.END)
            self.solution_text.insert(tk.END, "No solution found!")

    def animate_solution(self, path):
        def show_next_state(states, index):
            if index < len(states):
                self.update_display(states[index])
                self.root.after(500, show_next_state, states, index + 1)
        
        show_next_state(path, 0)

    def is_solvable(self, state):
        # Count inversions
        flat = state.flatten()
        inv_count = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                    inv_count += 1
        return inv_count % 2 == 0

    # Your existing functions
    def make_move(self, state, move):
        i, j = move[0], move[1]
        match move[2]:
            case "up":
                state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
            case "down":
                state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
            case "left":
                state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
            case "right":
                state[i][j], state[i][j+1] = state[i][j+1], state[i][j]

    def successors(self, state):
        successors = []
        indexes = np.where(state==0)
        i, j = indexes[0][0], indexes[1][0]
        if (i > 0):
            up_succ = state.copy()
            self.make_move(up_succ, (i, j, "up"))
            successors.append(up_succ)
        if (i < 2):
            down_succ = state.copy()
            self.make_move(down_succ, (i, j, "down"))
            successors.append(down_succ)
        if (j > 0):
            left_succ = state.copy()
            self.make_move(left_succ, (i, j, "left"))
            successors.append(left_succ)
        if (j < 2):
            right_succ = state.copy()
            self.make_move(right_succ, (i, j, "right"))
            successors.append(right_succ)
        return successors

    def h1_score(self, state, goalState):
        return np.sum(state != goalState)

    def h_score(self, state, goalState):
        return self.h1_score(state, goalState)

    def astar(self, initialState, goalState):
        PQ = PriorityQueue()
        prev = dict()
        visited = set()
        PQ.put((0 + self.h_score(initialState, goalState), (tuple(initialState.flatten()), 0)))
        prev[tuple(initialState.flatten())] = " "
        
        while not PQ.empty():
            outStateFScore, (outStateTuple, outStateGScore) = PQ.get()
            outState = np.array(outStateTuple).reshape(initialState.shape)
            visited.add(outStateTuple)
            
            if np.array_equal(outState, goalState):
                return True, prev, outStateGScore
                
            for chimeki in self.successors(outState):
                chimekiTuple = tuple(chimeki.flatten())
                if chimekiTuple not in visited:
                    chimekiGScore = outStateGScore + 1
                    chimekiFScore = self.h_score(chimeki, goalState) + chimekiGScore
                    PQ.put((chimekiFScore, (chimekiTuple, chimekiGScore)))
                    prev[chimekiTuple] = outStateTuple
                    
        return False, prev, float('inf')

def main():
    root = tk.Tk()
    app = EightPuzzleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
