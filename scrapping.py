import streamlit as st
import requests
from bs4 import BeautifulSoup
from googletrans import Translator, LANGUAGES

# Initialize the translator
translator = Translator()

# Define a function to translate text to English
def translate_text(text):
    # Detect the language of the text
    detected_lang = translator.detect(text).lang
    if detected_lang != 'en':
        # Translate to English if the text is not in English
        translated = translator.translate(text, dest='en').text
        return translated
    return text

# Define the function to perform web scraping
def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        return None

# Streamlit UI
st.title("Webpage Content Scraper with Translation")
url_input = st.text_input("Enter the URL of a webpage to scrape:", "")

if url_input:
    soup = scrape_website(url_input)
    if soup:
        # Displaying images
        st.header("Images:")
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url:
                st.image(img_url, caption=img_url)

        # Displaying header tags and paragraphs
        headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        for header in headers:
            for tag in soup.find_all(header):
                header_text = translate_text(tag.text.strip())
                st.subheader(f"{tag.name.upper()}: {header_text}")
                p_after = tag.find_next_sibling('p')
                if p_after:
                    translated_p = translate_text(p_after.text.strip())
                    st.write(translated_p)

        # Extracting banner information
        banner = soup.find('div', class_='banner')
        if banner:
            translated_banner = translate_text(banner.get_text(strip=True))
            st.subheader("Banner Text:")
            st.write(translated_banner)

        # Extracting FAQs
        faq_section = soup.find('section', id='faqs')
        if faq_section:
            st.subheader("FAQs:")
            faqs = faq_section.find_all('h3')
            for faq in faqs:
                question = translate_text(faq.text.strip())
                answer = faq.find_next_sibling('p')
                if answer:
                    translated_answer = translate_text(answer.text.strip())
                    st.write("Q: " + question)
                    st.write("A: " + translated_answer)

        # Extracting special offers
        special_offers = soup.find('div', class_='special-offers')
        if special_offers:
            st.subheader("Special Offers:")
            offers = special_offers.find_all('h2')
            for offer in offers:
                offer_text = translate_text(offer.text.strip())
                st.write("Offer: " + offer_text)
                details = offer.find_next_siblings('p')
                for detail in details:
                    translated_detail = translate_text(detail.text.strip())
                    st.write(translated_detail)
    else:
        st.error("Failed to retrieve the page. Please check the URL or try again later.")
else:
    st.write("Please enter a URL to begin scraping.")
