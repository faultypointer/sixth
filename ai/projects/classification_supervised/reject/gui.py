import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd
import tldextract
import requests
from bs4 import BeautifulSoup
import re

def extract_features(url):
    features = {}

    # Fetch the webpage
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    # Extract URL features
    # features['URL'] = url
    features['URLLength'] = len(url)

    # Extract domain features
    extracted = tldextract.extract(url)
    # features['Domain'] = extracted.domain
    features['DomainLength'] = len(extracted.domain)
    features['IsDomainIP'] = 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', extracted.domain) else 0
    # features['TLD'] = extracted.suffix
    features['TLDLength'] = len(extracted.suffix)

    # Calculate character features
    features['NoOfLettersInURL'] = sum(c.isalpha() for c in url)
    features['NoOfDegitsInURL'] = sum(c.isdigit() for c in url)
    features['NoOfSpecialCharsInURL'] = len(re.findall(r'[^a-zA-Z0-9]', url))
    features['LetterRatioInURL'] = features['NoOfLettersInURL'] / features['URLLength'] if features['URLLength'] > 0 else 0
    features['DegitRatioInURL'] = features['NoOfDegitsInURL'] / features['URLLength'] if features['URLLength'] > 0 else 0

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title_tag = soup.title.string if soup.title else ''
    features['HasTitle'] = 1 if title_tag else 0
    # features['Title'] = title_tag
    features['DomainTitleMatchScore'] = 1 if extracted.domain in title_tag else 0
    features['URLTitleMatchScore'] = 1 if url in title_tag else 0

    # Extract other features
    features['HasFavicon'] = 1 if soup.find('link', rel='icon') else 0
    features['HasDescription'] = 1 if soup.find('meta', attrs={'name': 'description'}) else 0
    features['NoOfImage'] = len(soup.find_all('img'))
    features['NoOfCSS'] = len(soup.find_all('link', rel='stylesheet'))
    features['NoOfJS'] = len(soup.find_all('script'))
    features['IsHTTPS'] = 1 if url.startswith('https://') else 0

    # Additional features can be added here...

    return features

# Function to predict if the URL is phishing
def predict_phishing():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Input Error", "Please enter a URL.")
        return
    
    # Extract features from the URL
    features = extract_url_features(url)
    
    # Convert features to DataFrame
    feature_df = pd.DataFrame([features])
    
    # Load the trained model
    model = joblib.load('model.pkl')
    
    # Make prediction
    prediction = model.predict(feature_df)
    
    # Show result
    if prediction[0] == 1:
        messagebox.showinfo("Prediction Result", "The website is phishing!")
    else:
        messagebox.showinfo("Prediction Result", "The website is safe.")

# Create the main window
root = tk.Tk()
root.title("Phishing URL Detector")

# Create and place the URL entry
url_label = tk.Label(root, text="Enter URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

# Create and place the predict button
predict_button = tk.Button(root, text="Predict", command=predict_phishing)
predict_button.pack(pady=20)

# Run the application
root.mainloop()
