import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import numpy as np

class KidneyDiseasePredictorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronic Kidney Disease Predictor")
        self.root.geometry("800x900")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', padding=5, font=('Arial', 10))
        style.configure('TButton', padding=5, font=('Arial', 10, 'bold'))
        style.configure('TEntry', padding=5)
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Chronic Kidney Disease Predictor", style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Define encoding dictionaries based on ordinal.categories_
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
        self.create_form_fields(main_frame)
        
        # Create predict button
        predict_button = ttk.Button(main_frame, text="Predict", command=self.predict)
        predict_button.grid(row=len(self.entries)+1, column=0, columnspan=2, pady=20)
        
        # Load the model
        try:
            with open('model.pkl', 'rb') as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Model file (model.pkl) not found!")
            self.model = None

    def create_form_fields(self, parent):
        # Define all fields with their types and options
        self.fields = {
            'age': {'type': 'float', 'label': 'Age (years)'},
            'bp': {'type': 'float', 'label': 'Blood Pressure (mm/Hg)'},
            'sg': {'type': 'combo', 'label': 'Specific Gravity', 
                   'values': ['1.005', '1.010', '1.015', '1.020', '1.025']},
            'al': {'type': 'combo', 'label': 'Albumin', 
                   'values': ['0', '1', '2', '3', '4']},
            'su': {'type': 'combo', 'label': 'Sugar', 
                   'values': ['0', '1', '2', '3', '4', '5']},
            'rbc': {'type': 'combo', 'label': 'Red Blood Cells', 
                    'values': ['normal', 'abnormal']},
            'pc': {'type': 'combo', 'label': 'Pus Cell', 
                   'values': ['normal', 'abnormal']},
            'pcc': {'type': 'combo', 'label': 'Pus Cell Clumps', 
                    'values': ['notpresent', 'present']},
            'ba': {'type': 'combo', 'label': 'Bacteria', 
                   'values': ['notpresent', 'present']},
            'bgr': {'type': 'float', 'label': 'Blood Glucose Random (mgs/dl)'},
            'bu': {'type': 'float', 'label': 'Blood Urea (mgs/dl)'},
            'sc': {'type': 'float', 'label': 'Serum Creatinine (mgs/dl)'},
            'sod': {'type': 'float', 'label': 'Sodium (mEq/L)'},
            'pot': {'type': 'float', 'label': 'Potassium (mEq/L)'},
            'hemo': {'type': 'float', 'label': 'Hemoglobin (gms)'},
            'pcv': {'type': 'float', 'label': 'Packed Cell Volume'},
            'wbcc': {'type': 'float', 'label': 'White Blood Cell Count (cells/cumm)'},
            'rbcc': {'type': 'float', 'label': 'Red Blood Cell Count (millions/cmm)'},
            'htn': {'type': 'combo', 'label': 'Hypertension', 
                    'values': ['no', 'yes']},
            'dm': {'type': 'combo', 'label': 'Diabetes Mellitus', 
                   'values': ['no', 'yes']},
            'cad': {'type': 'combo', 'label': 'Coronary Artery Disease', 
                    'values': ['no', 'yes']},
            'appet': {'type': 'combo', 'label': 'Appetite', 
                      'values': ['good', 'poor']},
            'pe': {'type': 'combo', 'label': 'Pedal Edema', 
                   'values': ['no', 'yes']},
            'ane': {'type': 'combo', 'label': 'Anemia', 
                    'values': ['no', 'yes']}
        }
        
        # Create and store entry widgets
        self.entries = {}
        for i, (field, props) in enumerate(self.fields.items()):
            row = i + 1
            label = ttk.Label(parent, text=props['label'])
            label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            
            if props['type'] == 'float':
                entry = ttk.Entry(parent)
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
            else:  # combo box
                entry = ttk.Combobox(parent, values=props['values'], state='readonly')
                entry.set(props['values'][0])  # set default value
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
            
            self.entries[field] = entry

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
    root = tk.Tk()
    app = KidneyDiseasePredictorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
