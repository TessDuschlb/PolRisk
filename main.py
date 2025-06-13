import streamlit as st
import pandas as pd
import spacy
import en_core_web_sm
import requests
from bs4 import BeautifulSoup
import openpyxl

# Lade spaCy
nlp = en_core_web_sm.load()

# Funktion zum Scrapen von Artikeln
def scrape_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    return [article.get_text() for article in articles]

# NLP-Analyse
def analyze_text(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Exportfunktion
def export_to_excel(data, filename='political_risk_analysis.xlsx'):
    df = pd.DataFrame(data, columns=['Entity', 'Label'])
    df.to_excel(filename, index=False)

# Streamlit App
st.title("Political Risk Analysis Dashboard")

# Scraping
dw_articles = scrape_articles("https://www.dw.com/en/top-stories/s-9097")
euronews_articles = scrape_articles("https://www.euronews.com/news")

# Anzeige
st.header("DW Articles")
for article in dw_articles:
    st.write(article)

st.header("Euronews Articles")
for article in euronews_articles:
    st.write(article)

# Analyse
st.header("NLP Analysis")
all_articles = dw_articles + euronews_articles
all_entities = []
for article in all_articles:
    st.write(f"**Article:** {article}")
    entities = analyze_text(article)
    st.write(f"**Entities:** {entities}")
    all_entities.extend(entities)

# Export
if st.button("Export to Excel"):
    export_to_excel(all_entities)
    st.success("Exported to political_risk_analysis.xlsx")
