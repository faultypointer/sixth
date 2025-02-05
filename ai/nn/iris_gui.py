import torch
import torch.nn as nn
import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton

# Define the model class
class IrisModel(nn.Module):
    def __init__(self, hidden_layer_neurons=8):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_features=4, out_features=hidden_layer_neurons),
            nn.ReLU(),
            nn.Linear(in_features=hidden_layer_neurons, out_features=hidden_layer_neurons),
            nn.ReLU(),
            nn.Linear(in_features=hidden_layer_neurons, out_features=3)
        )

    def forward(self, x):
        return self.layers(x)

# Load the trained model
model = IrisModel()
model.load_state_dict(torch.load("iris_model", weights_only=True))
model.eval()

# Function to predict the iris class
def predict_iris_class():
    try:
        # Get the input values from the entries
        sepal_length = float(entry_sepal_length.get())
        sepal_width = float(entry_sepal_width.get())
        petal_length = float(entry_petal_length.get())
        petal_width = float(entry_petal_width.get())

        # Convert the input to a tensor
        input_tensor = torch.tensor([[sepal_length, sepal_width, petal_length, petal_width]], dtype=torch.float32)

        # Make a prediction
        with torch.no_grad():
            output = model(input_tensor)
            predicted_class = torch.argmax(output, dim=1).item()

        # Map the predicted class to the iris species
        iris_species = ["Setosa", "Versicolor", "Virginica"]
        result_label.configure(text=f"Predicted Iris Species: {iris_species[predicted_class]}", text_color="green")

    except ValueError:
        result_label.configure(text="Please enter valid numbers", text_color="red")

# Create the main application window
app = CTk()
app.title("Iris Species Predictor")
app.geometry("400x300")

# Set the theme (optional)
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create and place the labels and entries
CTkLabel(app, text="Sepal Length (cm):").pack(pady=5)
entry_sepal_length = CTkEntry(app)
entry_sepal_length.pack(pady=5)

CTkLabel(app, text="Sepal Width (cm):").pack(pady=5)
entry_sepal_width = CTkEntry(app)
entry_sepal_width.pack(pady=5)

CTkLabel(app, text="Petal Length (cm):").pack(pady=5)
entry_petal_length = CTkEntry(app)
entry_petal_length.pack(pady=5)

CTkLabel(app, text="Petal Width (cm):").pack(pady=5)
entry_petal_width = CTkEntry(app)
entry_petal_width.pack(pady=5)

# Create and place the predict button
predict_button = CTkButton(app, text="Predict", command=predict_iris_class)
predict_button.pack(pady=20)

# Create and place the result label
result_label = CTkLabel(app, text="", font=("Arial", 14))
result_label.pack(pady=10)

# Run the application
app.mainloop()
