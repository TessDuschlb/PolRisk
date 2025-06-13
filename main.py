import streamlit as st
import pandas as pd
import spacy
from spacy import displacy
import requests
from bs4 import BeautifulSoup
import openpyxl

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Function to scrape news articles
def scrape_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    return [article.get_text() for article in articles]

# Function to analyze text with spaCy
def analyze_text(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Function to export data to Excel
def export_to_excel(data, filename='political_risk_analysis.xlsx'):
    df = pd.DataFrame(data, columns=['Entity', 'Label'])
    df.to_excel(filename, index=False)

# Streamlit app
st.title("Political Risk Analysis Dashboard")

# Scrape articles
dw_articles = scrape_articles("https://www.dw.com/en/top-stories/s-9097")
euronews_articles = scrape_articles("https://www.euronews.com/news")

# Display articles
st.header("DW Articles")
for article in dw_articles:
    st.write(article)

st.header("Euronews Articles")
for article in euronews_articles:
    st.write(article)

# Analyze articles
st.header("NLP Analysis")
all_articles = dw_articles + euronews_articles
all_entities = []
for article in all_articles:
    st.write(f"Article: {article}")
    analysis = analyze_text(article)
    st.write(f"Entities: {analysis}")
    all_entities.extend(analysis)

# Export to Excel
if st.button("Export to Excel"):
    export_to_excel(all_entities)
    st.success("Exported to political_risk_analysis.xlsx")
