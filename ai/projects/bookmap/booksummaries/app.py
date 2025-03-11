import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from atlas import Atlas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import joblib

class BookSimilarityApp:
    def __init__(self, root, model_path="book_similarity_model"):
        self.root = root
        self.root.title("Book Similarity Visualizer")
        
        # Load the trained model
        self.model = self.load_model(model_path)
        if not self.model:
            messagebox.showerror("Error", "Failed to load the model.")
            self.root.destroy()
            return
        
        # GUI Components
        self.setup_gui()
        
    def load_model(self, model_path):
        try:
            return Atlas.load(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def setup_gui(self):
        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_button = ttk.Button(search_frame, text="Search", command=self.on_search)
        self.search_button.pack(side=tk.LEFT)
        
        # Graph Frame
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize graph
        self.G = nx.Graph()
        self.pos = {}
        self.current_center = None
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def on_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a book title.")
            return
        
        # Search for matching titles
        matches = self.model.search_titles(query)
        if not matches:
            messagebox.showinfo("No Results", f"No books found matching '{query}'.")
            return
        
        # If multiple matches, let the user choose one
        if len(matches) > 1:
            selected_title = self.show_selection_dialog(matches)
            if not selected_title:
                return
        else:
            selected_title = matches[0]
        
        # Update the graph with the selected book as the center
        self.update_graph(selected_title)
    
    def show_selection_dialog(self, matches):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select a Book")
        
        selected_title = tk.StringVar()
        
        ttk.Label(dialog, text="Multiple matches found. Please select one:").pack(pady=10)
        
        for title in matches:
            ttk.Radiobutton(dialog, text=title, variable=selected_title, value=title).pack(anchor=tk.W)
        
        ttk.Button(dialog, text="OK", command=dialog.destroy).pack(pady=10)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return selected_title.get()
    
    def update_graph(self, center_title):
        # Clear the graph
        self.G.clear()
        self.ax.clear()
        
        # Add the center node
        self.G.add_node(center_title)
        
        # Get similar books
        similars = self.model.similars(center_title, n=10)
        for title, score in similars:
            self.G.add_node(title)
            self.G.add_edge(center_title, title, weight=score)
        
        # Use circular layout for positioning
        self.pos = nx.circular_layout(self.G)
        
        # Draw the graph
        nx.draw(self.G, self.pos, with_labels=True, node_size=800, node_color="skyblue", font_size=8, font_weight="bold", ax=self.ax, edge_color="gray")
        self.ax.set_title(f"Books Similar to '{center_title}'")
        self.canvas.draw()
        
        # Bind click event to nodes
        self.canvas.mpl_connect("button_press_event", self.on_node_click)
    
    def on_node_click(self, event):
        if not event.inaxes:
            return
        
        # Find the clicked node
        for node, (x, y) in self.pos.items():
            if (event.xdata - x) ** 2 + (event.ydata - y) ** 2 < 0.1:  # Simple distance check
                self.update_graph(node)
                break


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = BookSimilarityApp(root, model_path="book_similarity_model")
    root.mainloop()
