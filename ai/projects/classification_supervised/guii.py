import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import numpy as np
from ttkthemes import ThemedTk

class ModernTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip, text=self.text, justify='left',
                         background="#2E2E2E", foreground="white",
                         relief='solid', borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class KidneyDiseasePredictorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kidney Disease Predictor")
        self.root.geometry("1000x800")
        
        # Set theme
        self.root.set_theme("arc")  # Modern, clean theme
        
        # Configure colors
        self.colors = {
            'primary': '#2196F3',    # Blue
            'success': '#4CAF50',    # Green
            'warning': '#FFC107',    # Yellow
            'danger': '#F44336',     # Red
            'bg': '#F5F5F5',         # Light gray
            'text': '#212121'        # Dark gray
        }
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.main_container = ttk.Frame(root, padding="20")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Add header
        self.create_header()
        
        # Add tab control
        self.create_tabs()
        
        # Initialize encoding dictionaries (same as before)
        self.encoding_dict = {
            'sg': {'1.005': 0, '1.010': 1, '1.015': 2, '1.020': 3, '1.025': 4, '?': 5},
            'al': {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '?': 5},
            'su': {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '?': 6},
            'rbc': {'?': 0, 'abnormal': 1, 'normal': 2},
            'pc': {'?': 0, 'abnormal': 1, 'normal': 2},
            'pcc': {'?': 0, 'notpresent': 1, 'present': 2},
            'ba': {'?': 0, 'notpresent': 1, 'present': 2},
            'htn': {'?': 0, 'no': 1, 'yes': 2},
            'dm': {'?': 0, 'no': 1, 'yes': 2},
            'cad': {'?': 0, 'no': 1, 'yes': 2},
            'appet': {'?': 0, 'good': 1, 'poor': 2},
            'pe': {'?': 0, 'no': 1, 'yes': 2},
            'ane': {'?': 0, 'no': 1, 'yes': 2}
        }
        
        # Create form fields
        self.create_form_fields()
        
        # Load the model
        try:
            with open('model.pkl', 'rb') as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Model file (model.pkl) not found!")
            self.model = None

    def configure_styles(self):
        style = ttk.Style()
        
        # Configure frame styles
        style.configure('Header.TFrame', background=self.colors['bg'])
        style.configure('Content.TFrame', background=self.colors['bg'])
        
        # Configure label styles
        style.configure('Header.TLabel',
                       font=('Helvetica', 24, 'bold'),
                       foreground=self.colors['primary'])
        style.configure('SubHeader.TLabel',
                       font=('Helvetica', 12),
                       foreground=self.colors['text'])
        style.configure('Field.TLabel',
                       font=('Helvetica', 10),
                       padding=5)
        
        # Configure button styles
        style.configure('Predict.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=10)
        
        # Configure entry styles
        style.configure('Field.TEntry',
                       padding=5)

    def create_header(self):
        header_frame = ttk.Frame(self.main_container, style='Header.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        logo_label = ttk.Label(header_frame, text="🏥", font=('Helvetica', 32))
        logo_label.grid(row=0, column=0, padx=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Kidney Disease Predictor",
                               style='Header.TLabel')
        title_label.grid(row=0, column=1)
        
        subtitle_label = ttk.Label(header_frame,
                                 text="Enter patient information to predict kidney disease risk",
                                 style='SubHeader.TLabel')
        subtitle_label.grid(row=1, column=1)

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.main_container)
        self.tab_control.grid(row=1, column=0, sticky="nsew")
        
        # Patient Information Tab
        self.patient_tab = ttk.Frame(self.tab_control, padding=20)
        self.tab_control.add(self.patient_tab, text="Patient Information")
        
        # Help Tab
        help_tab = ttk.Frame(self.tab_control, padding=20)
        self.tab_control.add(help_tab, text="Help")
        
        # Add help content
        help_text = """
        This application predicts the likelihood of chronic kidney disease based on patient data.
        
        Instructions:
        1. Fill in all the required fields in the Patient Information tab
        2. Click the Predict button to see the results
        3. Consult with a healthcare professional for proper diagnosis
        
        Note: This tool is for screening purposes only and should not replace professional medical advice.
        """
        help_label = ttk.Label(help_tab, text=help_text, wraplength=600)
        help_label.pack(pady=20)

    def create_form_fields(self):
        # Create a canvas with scrollbar
        canvas = tk.Canvas(self.patient_tab)
        scrollbar = ttk.Scrollbar(self.patient_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Group fields
        field_groups = {
            'Basic Information': ['age', 'bp'],
            'Urine Analysis': ['sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba'],
            'Blood Tests': ['bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wbcc', 'rbcc'],
            'Medical History': ['htn', 'dm', 'cad', 'appet', 'pe', 'ane']
        }

        # Create fields by group
        self.entries = {}
        row = 0
        
        for group_name, fields in field_groups.items():
            # Add group header
            group_label = ttk.Label(scrollable_frame, text=group_name,
                                  font=('Helvetica', 12, 'bold'))
            group_label.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="w")
            row += 1
            
            # Add fields
            for field in fields:
                # Field label
                label = ttk.Label(scrollable_frame, text=self.fields[field]['label'],
                                style='Field.TLabel')
                label.grid(row=row, column=0, sticky="w", padx=5, pady=2)
                
                # Field input
                if self.fields[field]['type'] == 'float':
                    entry = ttk.Entry(scrollable_frame, style='Field.TEntry')
                else:
                    entry = ttk.Combobox(scrollable_frame, values=self.fields[field]['values'],
                                       state='readonly')
                    entry.set(self.fields[field]['values'][0])
                
                entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                self.entries[field] = entry
                
                # Add tooltip with normal ranges or descriptions
                tooltip_text = self.get_tooltip_text(field)
                ModernTooltip(entry, tooltip_text)
                
                row += 1

        # Add predict button
        predict_button = ttk.Button(scrollable_frame, text="Predict",
                                  style='Predict.TButton',
                                  command=self.predict)
        predict_button.grid(row=row, column=0, columnspan=2, pady=20)

        # Configure grid
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.patient_tab.grid_columnconfigure(0, weight=1)
        self.patient_tab.grid_rowconfigure(0, weight=1)

    def get_tooltip_text(self, field):
        # Define normal ranges and descriptions for fields
        tooltips = {
            'age': "Patient's age in years",
            'bp': "Normal range: 90/60 - 120/80 mmHg",
            'bgr': "Normal fasting range: 70-100 mg/dL",
            'bu': "Normal range: 7-20 mg/dL",
            'sc': "Normal range: 0.7-1.3 mg/dL",
            'sod': "Normal range: 135-145 mEq/L",
            'pot': "Normal range: 3.5-5.0 mEq/L",
            'hemo': "Normal range: 13.5-17.5 g/dL (men), 12.0-15.5 g/dL (women)",
            'pcv': "Normal range: 40-50% (men), 36-44% (women)",
            'wbcc': "Normal range: 4,500-11,000 cells/μL",
            'rbcc': "Normal range: 4.5-5.9 million cells/μL (men), 4.1-5.1 million cells/μL (women)",
        }
        return tooltips.get(field, "Click to select a value")

    def validate_inputs(self):
        for field, entry in self.entries.items():
            if self.fields[field]['type'] == 'float':
                try:
                    value = float(entry.get())
                    if value < 0:
                        messagebox.showerror("Error", f"{self.fields[field]['label']} cannot be negative!")
                        return False
                except ValueError:
                    messagebox.showerror("Error", f"Please enter a valid number for {self.fields[field]['label']}")
                    return False
        return True

    def predict(self):
        if not self.model:
            messagebox.showerror("Error", "Model not loaded!")
            return
            
        if not self.validate_inputs():
            return
            
        # Get values and convert to appropriate format
        input_data = []
        categorical_fields = list(self.encoding_dict.keys())
        
        for field, entry in self.entries.items():
            value = entry.get()
            if field in categorical_fields:
                # Convert categorical value to number using encoding dictionary
                encoded_value = self.encoding_dict[field][value]
                input_data.append(encoded_value)
            else:
                # Convert numeric value to float
                input_data.append(float(value))
        
        try:
            # Make prediction
            input_array = np.array(input_data).reshape(1, -1)
            prediction = self.model.predict(input_array)
            
            if prediction[0] == 0:
                result = "Based on the provided information, chronic kidney disease is indicated.\n\nPlease consult with a healthcare professional for proper diagnosis and treatment."
                messagebox.showwarning("Prediction Result", result)
            else:
                result = "Based on the provided information, chronic kidney disease is not indicated.\n\nHowever, always consult with a healthcare professional for proper medical advice."
                messagebox.showinfo("Prediction Result", result)
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during prediction: {str(e)}")

def main():
    root = ThemedTk(theme="arc")
    app = KidneyDiseasePredictorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
