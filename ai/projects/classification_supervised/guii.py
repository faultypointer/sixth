import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import numpy as np

class Card(ttk.Frame):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(style='Card.TFrame', padding=(15, 10))
        
        # Card header
        header = ttk.Label(
            self,
            text=title,
            style='CardTitle.TLabel'
        )
        header.pack(anchor='w', pady=(0, 10))
        
        # Content frame
        self.content = ttk.Frame(self, style='CardContent.TFrame')
        self.content.pack(fill='x', expand=True)

class ModernEntry(ttk.Frame):
    def __init__(self, parent, label, input_type='entry', values=None, **kwargs):
        super().__init__(parent, style='Modern.TFrame', padding=(0, 5))
        
        # Label
        self.label = ttk.Label(
            self,
            text=label,
            style='FieldLabel.TLabel'
        )
        self.label.pack(anchor='w')
        
        # Input field
        if input_type == 'entry':
            self.input = ttk.Entry(
                self,
                style='Modern.TEntry',
                width=20
            )
        else:  # combobox
            self.input = ttk.Combobox(
                self,
                values=values,
                style='Modern.TCombobox',
                state='readonly',
                width=17
            )
            self.input.set(values[0])
            
        self.input.pack(anchor='w', pady=(2, 0))

class KidneyDiseasePredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("Kidney Disease Prediction Tool")
        self.root.configure(bg='#f8fafc')
        self.root.geometry("1000x800")
        
        # Configure styles
        self.setup_styles()
        
        # Main container
        main_container = ttk.Frame(root, style='Main.TFrame', padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_container)
        
        # Create scrollable content area
        self.create_scrollable_content(main_container)
        
        # Create content
        self.create_content()
        
        # Load model
        try:
            with open('model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            self.show_error("Model file (model.pkl) not found!")
            self.model = None

    def setup_styles(self):
        self.style = ttk.Style()
        
        # Color palette
        colors = {
            'bg': '#f8fafc',
            'card': '#ffffff',
            'primary': '#2563eb',
            'text': '#1e293b',
            'text_light': '#64748b',
            'border': '#e2e8f0'
        }
        
        # Configure base styles
        self.style.configure('Main.TFrame', background=colors['bg'])
        self.style.configure('Card.TFrame',
                           background=colors['card'],
                           borderwidth=1,
                           relief='solid')
        
        # Labels
        self.style.configure('Header.TLabel',
                           font=('Segoe UI', 24, 'bold'),
                           foreground=colors['primary'],
                           background=colors['bg'])
        
        self.style.configure('Subheader.TLabel',
                           font=('Segoe UI', 12),
                           foreground=colors['text_light'],
                           background=colors['bg'])
        
        self.style.configure('CardTitle.TLabel',
                           font=('Segoe UI', 14, 'bold'),
                           foreground=colors['text'],
                           background=colors['card'])
        
        self.style.configure('FieldLabel.TLabel',
                           font=('Segoe UI', 10),
                           foreground=colors['text_light'],
                           background=colors['card'])
        
        # Entry and Combobox
        self.style.configure('Modern.TEntry',
                           fieldbackground='#f1f5f9',
                           borderwidth=0,
                           padding=5)
        
        self.style.configure('Modern.TCombobox',
                           fieldbackground='#f1f5f9',
                           borderwidth=0,
                           padding=5)
        
        # Button
        self.style.configure('Primary.TButton',
                           font=('Segoe UI', 11),
                           padding=10)

    def create_header(self, parent):
        header = ttk.Frame(parent, style='Main.TFrame')
        header.pack(fill='x', pady=(0, 20))
        
        title = ttk.Label(
            header,
            text="Kidney Disease Risk Assessment",
            style='Header.TLabel'
        )
        title.pack(anchor='w')
        
        subtitle = ttk.Label(
            header,
            text="Enter patient information in the fields below for analysis",
            style='Subheader.TLabel'
        )
        subtitle.pack(anchor='w')

    def create_scrollable_content(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(container, bg='#f8fafc', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure canvas
        self.scrollable_frame = ttk.Frame(self.canvas, style='Main.TFrame')
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=940)
        
        # Update scroll region when frame size changes
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_content(self):
        # Patient Information
        patient_container = ttk.Frame(self.scrollable_frame, style='Main.TFrame')
        patient_container.pack(fill='x', padx=5, pady=5)
        
        patient_card = Card(patient_container, "Patient Information")
        patient_card.pack(fill='x', side=tk.LEFT, expand=True, padx=5)
        
        urinalysis_card = Card(patient_container, "Urinalysis Results")
        urinalysis_card.pack(fill='x', side=tk.LEFT, expand=True, padx=5)
        
        self.inputs = {}
        
        # Patient Information Fields
        self.inputs['age'] = ModernEntry(patient_card.content, "Age (years)", 'entry')
        self.inputs['age'].pack(fill='x', pady=2)
        self.inputs['bp'] = ModernEntry(patient_card.content, "Blood Pressure (mm/Hg)", 'entry')
        self.inputs['bp'].pack(fill='x', pady=2)
        
        # Urinalysis Fields
        self.inputs['sg'] = ModernEntry(urinalysis_card.content, "Specific Gravity",
                                      'combo', [1.005, 1.010, 1.015, 1.020, 1.025])
        self.inputs['sg'].pack(fill='x', pady=2)
        self.inputs['al'] = ModernEntry(urinalysis_card.content, "Albumin",
                                      'combo', [0, 1, 2, 3, 4, 5])
        self.inputs['al'].pack(fill='x', pady=2)
        
        # Blood Tests
        blood_card = Card(self.scrollable_frame, "Blood Test Results")
        blood_card.pack(fill='x', padx=10, pady=5)
        
        blood_content = ttk.Frame(blood_card.content, style='CardContent.TFrame')
        blood_content.pack(fill='x')
        
        left_blood = ttk.Frame(blood_content, style='CardContent.TFrame')
        left_blood.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        right_blood = ttk.Frame(blood_content, style='CardContent.TFrame')
        right_blood.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        blood_tests_left = [
            ('bgr', 'Blood Glucose (mgs/dl)', 'entry'),
            ('bu', 'Blood Urea (mgs/dl)', 'entry'),
            ('sc', 'Serum Creatinine (mgs/dl)', 'entry'),
            ('sod', 'Sodium (mEq/L)', 'entry'),
            ('pot', 'Potassium (mEq/L)', 'entry')
        ]
        
        blood_tests_right = [
            ('hemo', 'Hemoglobin (gms)', 'entry'),
            ('pcv', 'Packed Cell Volume', 'entry'),
            ('wbcc', 'White Blood Cell Count', 'entry'),
            ('rbcc', 'Red Blood Cell Count', 'entry')
        ]
        
        for key, label, input_type in blood_tests_left:
            self.inputs[key] = ModernEntry(left_blood, label, input_type)
            self.inputs[key].pack(fill='x', pady=2)
            
        for key, label, input_type in blood_tests_right:
            self.inputs[key] = ModernEntry(right_blood, label, input_type)
            self.inputs[key].pack(fill='x', pady=2)
        
        # Medical History
        history_card = Card(self.scrollable_frame, "Medical History")
        history_card.pack(fill='x', padx=10, pady=5)
        
        history_content = ttk.Frame(history_card.content, style='CardContent.TFrame')
        history_content.pack(fill='x')
        
        left_history = ttk.Frame(history_content, style='CardContent.TFrame')
        left_history.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        right_history = ttk.Frame(history_content, style='CardContent.TFrame')
        right_history.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        medical_history_left = [
            ('htn', 'Hypertension', ['no', 'yes']),
            ('dm', 'Diabetes Mellitus', ['no', 'yes']),
            ('cad', 'Coronary Artery Disease', ['no', 'yes'])
        ]
        
        medical_history_right = [
            ('appet', 'Appetite', ['good', 'poor']),
            ('pe', 'Pedal Edema', ['no', 'yes']),
            ('ane', 'Anemia', ['no', 'yes'])
        ]
        
        for key, label, values in medical_history_left:
            self.inputs[key] = ModernEntry(left_history, label, 'combo', values)
            self.inputs[key].pack(fill='x', pady=2)
            
        for key, label, values in medical_history_right:
            self.inputs[key] = ModernEntry(right_history, label, 'combo', values)
            self.inputs[key].pack(fill='x', pady=2)
        
        # Predict Button
        button_frame = ttk.Frame(self.scrollable_frame, style='Main.TFrame')
        button_frame.pack(pady=20)
        
        predict_btn = ttk.Button(
            button_frame,
            text="Generate Prediction",
            style='Primary.TButton',
            command=self.predict
        )
        predict_btn.pack()

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def predict(self):
        if self.model is None:
            self.show_error("Model not loaded!")
            return
        
        try:
            # Collect and preprocess input values
            input_values = []
            for key, field in self.inputs.items():
                value = field.input.get()
                try:
                    if isinstance(field.input, ttk.Entry):
                        value = float(value)
                    else:  # Combobox
                        value = 1 if value in ['yes', 'present', 'abnormal', 'good'] else 0
                    input_values.append(value)
                except ValueError:
                    self.show_error(f"Invalid input for {field.label['text']}")
                    return
            
            # Make prediction
            input_data = np.array(input_values).reshape(1, -1)
            prediction = self.model.predict(input_data)
            
            # Show results
            self.show_results(prediction[0])
            
        except Exception as e:
            self.show_error(f"Prediction error: {str(e)}")

    def show_results(self, prediction):
        result_window = tk.Toplevel(self.root)
        result_window.title("Prediction Results")
        result_window.geometry("400x300")
        result_window.configure(bg='#f8fafc')
        result_window.transient(self.root)
        result_window.grab_set()
        
        frame = ttk.Frame(result_window, style='Main.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Result icon (using Unicode characters)
        icon = "✓" if prediction == 0 else "!"
        icon_label = ttk.Label(
            frame,
            text=icon,
            font=('Segoe UI', 48),
            foreground='#22c55e' if prediction == 0 else '#ef4444',
            background='#f8fafc'
        )
        icon_label.pack(pady=10)
        
        # Result text
        result_text = "No Chronic Kidney Disease Detected" if prediction == 0 else "Chronic Kidney Disease Risk Detected"
        result_label = ttk.Label(
            frame,
            text=result_text,
            style='Header.TLabel',
            font=('Segoe UI', 16, 'bold')
        )
        result_label.pack(pady=10)
        
        # Additional info
        info_text = ("Regular check-ups recommended for monitoring kidney health."
                    if prediction == 0 else
                    "Please consult with a healthcare provider for further evaluation.")
        info_label = ttk.Label(
            frame,
            text=info_text,
            style='Subheader.TLabel',
            wraplength=300
        )
        info_label.pack(pady=10)
        
        # Close button
        close_btn = ttk.Button(
            frame,
            text="Close",
            style='Primary.TButton',
            command=result_window.destroy
        )
        close_btn.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = KidneyDiseasePredictor(root)
    root.mainloop()
