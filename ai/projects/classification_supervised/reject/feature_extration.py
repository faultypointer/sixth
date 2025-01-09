import requests
from bs4 import BeautifulSoup
import tldextract
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
    features['URL'] = url
    features['URLLength'] = len(url)

    # Extract domain features
    extracted = tldextract.extract(url)
    features['Domain'] = extracted.domain
    features['DomainLength'] = len(features['Domain'])
    features['IsDomainIP'] = 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', extracted.domain) else 0
    features['TLD'] = extracted.suffix
    features['TLDLength'] = len(features['TLD'])

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
    features['Title'] = title_tag
    features['DomainTitleMatchScore'] = 1 if features['Domain'] in title_tag else 0
    features['URLTitleMatchScore'] = 1 if features['URL'] in title_tag else 0

    # Extract other features
    features['HasFavicon'] = 1 if soup.find('link', rel='icon') else 0
    features['HasDescription'] = 1 if soup.find('meta', attrs={'name': 'description'}) else 0
    features['NoOfImage'] = len(soup.find_all('img'))
    features['NoOfCSS'] = len(soup.find_all('link', rel='stylesheet'))
    features['NoOfJS'] = len(soup.find_all('script'))
    features['IsHTTPS'] = 1 if url.startswith('https://') else 0

    # Additional features can be added here...

    return features

# Example usage
url = "https://example.com"  # Replace with the URL you want to analyze
features = extract_features(url)
if features:
    for key, value in features.items():
        print(f"{key}: {value}")
