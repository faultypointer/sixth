import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import pickle
import numpy as np

class ModernWidget(ttk.Frame):
    def __init__(self, parent, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(padding="10")
        self.configure(relief="ridge", borderwidth=1)
        
        # Header
        header = ttk.Label(self, text=text, style="Header.TLabel")
        header.pack(fill="x", pady=(0, 10))

class KidneyDiseasePredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("Kidney Disease Risk Assessment Tool")
        self.root.geometry("900x800")
        self.root.configure(bg='#f0f2f5')
        
        # Configure styles
        self.setup_styles()
        
        # Create main container
        main_container = ttk.Frame(root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ttk.Label(
            header_frame, 
            text="Kidney Disease Risk Assessment", 
            style="Title.TLabel"
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Enter patient information below for analysis",
            style="Subtitle.TLabel"
        )
        subtitle.pack()
        
        # Create scrollable frame
        canvas = tk.Canvas(main_container, bg='#f0f2f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, padding="10")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=850)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar components
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Dictionary to store input variables
        self.inputs = {}
        
        # Group fields by category
        self.field_groups = {
            'Demographics': {
                'age': {'type': 'float', 'label': 'Age (years)'},
                'bp': {'type': 'float', 'label': 'Blood Pressure (mm/Hg)'}
            },
            'Urinalysis': {
                'sg': {'type': 'combo', 'label': 'Specific Gravity', 'values': [1.005, 1.010, 1.015, 1.020, 1.025]},
                'al': {'type': 'combo', 'label': 'Albumin', 'values': [0, 1, 2, 3, 4, 5]},
                'su': {'type': 'combo', 'label': 'Sugar', 'values': [0, 1, 2, 3, 4, 5]},
                'rbc': {'type': 'combo', 'label': 'Red Blood Cells', 'values': ['normal', 'abnormal']},
                'pc': {'type': 'combo', 'label': 'Pus Cell', 'values': ['normal', 'abnormal']},
                'pcc': {'type': 'combo', 'label': 'Pus Cell Clumps', 'values': ['present', 'notpresent']},
                'ba': {'type': 'combo', 'label': 'Bacteria', 'values': ['present', 'notpresent']}
            },
            'Blood Tests': {
                'bgr': {'type': 'float', 'label': 'Blood Glucose Random (mgs/dl)'},
                'bu': {'type': 'float', 'label': 'Blood Urea (mgs/dl)'},
                'sc': {'type': 'float', 'label': 'Serum Creatinine (mgs/dl)'},
                'sod': {'type': 'float', 'label': 'Sodium (mEq/L)'},
                'pot': {'type': 'float', 'label': 'Potassium (mEq/L)'},
                'hemo': {'type': 'float', 'label': 'Hemoglobin (gms)'},
                'pcv': {'type': 'float', 'label': 'Packed Cell Volume'},
                'wbcc': {'type': 'float', 'label': 'White Blood Cell Count (cells/cumm)'},
                'rbcc': {'type': 'float', 'label': 'Red Blood Cell Count (millions/cmm)'}
            },
            'Medical History': {
                'htn': {'type': 'combo', 'label': 'Hypertension', 'values': ['no', 'yes']},
                'dm': {'type': 'combo', 'label': 'Diabetes Mellitus', 'values': ['no', 'yes']},
                'cad': {'type': 'combo', 'label': 'Coronary Artery Disease', 'values': ['no', 'yes']},
                'appet': {'type': 'combo', 'label': 'Appetite', 'values': ['good', 'poor']},
                'pe': {'type': 'combo', 'label': 'Pedal Edema', 'values': ['no', 'yes']},
                'ane': {'type': 'combo', 'label': 'Anemia', 'values': ['no', 'yes']}
            }
        }
        
        # Create input fields by group
        self.create_grouped_inputs()
        
        # Create predict button with modern styling
        button_frame = ttk.Frame(main_container, padding="20")
        button_frame.pack(fill="x", pady=20)
        
        predict_btn = ttk.Button(
            button_frame,
            text="Generate Prediction",
            command=self.predict,
            style="Accent.TButton"
        )
        predict_btn.pack(pady=10)
        
        try:
            with open('model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "Model file (model.pkl) not found!")
            self.model = None

    def setup_styles(self):
        style = ttk.Style()
        
        default_font = font.nametofont("TkDefaultFont")
        
        # Configure colors
        style.configure(".", font=(default_font.actual("family"), 10))
        style.configure("Title.TLabel", font=(default_font.actual("family"), 24, "bold"), foreground="#1a237e")
        style.configure("Subtitle.TLabel", font=(default_font.actual("family"), 12), foreground="#424242")
        style.configure("Header.TLabel", font=(default_font.actual("family"), 14, "bold"), foreground="#1a237e")
        style.configure("Section.TFrame", background="#ffffff")
        
        # Button styling
        style.configure("Accent.TButton",
                        font=(default_font.actual("family"), 12),
                        padding=10)
        
        # Entry styling
        style.configure("TEntry", padding=5)
        style.configure("TCombobox", padding=5)

    def create_grouped_inputs(self):
        row = 0
        for group_name, fields in self.field_groups.items():
            # Create group frame
            group_frame = ModernWidget(self.scrollable_frame, group_name)
            group_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 20), padx=5)
            
            # Create fields within group
            for idx, (field, properties) in enumerate(fields.items()):
                container = ttk.Frame(group_frame)
                container.pack(fill="x", pady=2)
                
                # Create label
                label = ttk.Label(container, text=properties['label'])
                label.pack(side="left", padx=(0, 10))
                
                # Create input field based on type
                if properties['type'] == 'float':
                    self.inputs[field] = ttk.Entry(container, width=20)
                elif properties['type'] == 'combo':
                    self.inputs[field] = ttk.Combobox(
                        container,
                        values=properties['values'],
                        state='readonly',
                        width=17
                    )
                    self.inputs[field].set(properties['values'][0])
                
                self.inputs[field].pack(side="right", padx=5)
            
            row += 1

    def preprocess_input(self):
        # Collect all fields in correct order
        all_fields = []
        for group in self.field_groups.values():
            all_fields.extend(group.items())
            
        values = []
        for field, properties in all_fields:
            try:
                if properties['type'] == 'float':
                    value = float(self.inputs[field].get())
                else:
                    value = self.inputs[field].get()
                    # Convert categorical variables to numeric
                    if value in ['normal', 'notpresent', 'no', 'poor']:
                        value = 0
                    elif value in ['abnormal', 'present', 'yes', 'good']:
                        value = 1
                values.append(value)
            except ValueError:
                messagebox.showerror("Error", f"Invalid input for {properties['label']}")
                return None
        return np.array(values).reshape(1, -1)

    def predict(self):
        if self.model is None:
            messagebox.showerror("Error", "Model not loaded!")
            return
        
        input_data = self.preprocess_input()
        if input_data is None:
            return
        
        try:
            prediction = self.model.predict(input_data)
            result = "Chronic Kidney Disease" if prediction[0] == 1 else "No Chronic Kidney Disease detected"
            
            # Create a custom dialog for results
            result_dialog = tk.Toplevel(self.root)
            result_dialog.title("Prediction Results")
            result_dialog.geometry("400x200")
            result_dialog.configure(bg='#f0f2f5')
            
            # Add some padding
            frame = ttk.Frame(result_dialog, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            # Result header
            ttk.Label(
                frame,
                text="Analysis Results",
                style="Title.TLabel"
            ).pack(pady=(0, 20))
            
            # Result text
            ttk.Label(
                frame,
                text=result,
                style="Subtitle.TLabel"
            ).pack(pady=10)
            
            # Close button
            ttk.Button(
                frame,
                text="Close",
                command=result_dialog.destroy,
                style="Accent.TButton"
            ).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Prediction error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KidneyDiseasePredictor(root)
    root.mainloop()
