from csv import writer
from bs4 import BeautifulSoup
import requests
import spacy
import csv

# Load the spaCy language model to scan the keywords
nlp = spacy.load("en_core_web_sm")

def categorize_section(content):
    doc = nlp(content)
    for ent in doc.ents:
            if "Family Court" in content:
                return "Family Law"
            elif "Commercial" in content:
                return "Commercial Law"
            elif "Industrial" in content:
                return "Industrial Law"
            elif "Criminal" in content:
                return "Criminal Law"
    return None

URL = 'https://www.austlii.edu.au/databases.html'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-653ee3a5-66c8cdc6759257f06515fd24"
}

req = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(req.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

# sections to scrape
sections = {
    'cth': 'Commonwealth of Australia',
    'act': 'Australian Capital Territory',
    'nsw': 'New South Wales',
    'nt': 'Northern Territory',
    'qld': 'Queensland',
    'sa': 'South Australia',
    'tas': 'Tasmania',
    'vic' : 'Victoria',
}
categorized_data = []
for section_id, section_name in sections.items():
    section = soup2.find(id=section_id)
    if section:
        # Find the subheadings and associated links
        subheadings = section.find_all('h2', class_='card-title')
        for subheading in subheadings:
            links = subheading.find_next('ul').find_all('a')
            for link in links:
                link_text = link.get_text().strip()
                link_url = link['href']
                category = categorize_section(link_text)
                if category:
                    categorized_data.append([section_name, category, link_text, link_url])
# Define CSV file name
csv_file = 'categorized_data.csv'

# Convert categorized data into a CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow(["Section Name", "Category", "Link Text", "Link URL"])

    # Write the categorized data rows
    writer.writerows(categorized_data)

print(f"Data has been successfully written to {csv_file}")