# Code largely based on project (News02) https://github.com/kliewerdaniel/News02

# Installation procedure
# You will need Python > 3.8 installed
# pip install -r requirements.txt
# Sometimes Python Install Certificates script needs to be executed
# Install Ollama if you have not done already
# then pull llama KriKri LLM (ollama pull ilsp/llama-krikri-8b-instruct:latest)
# then run the script

__author__ = "Alexandros Koutsioumpas"
__date__ = "2025/09/08"
__status__ = "v0.1"

# === CONFIGURABLE MODELS ===
SUMMARY_MODEL = 'ilsp/llama-krikri-8b-instruct:latest' # alternatively use "gemma3:4b" on older machines with less RAM
BROADCAST_MODEL = 'ilsp/llama-krikri-8b-instruct:latest' # alternatively use "gemma3:4b" on older machines with less RAM
TTS_VOICE = "el-GR-NestorasNeural" # Change to "el-GR-AthinaNeural" for female voice
# ===========================

import os
import yaml
import feedparser
from newspaper import Article
from newspaper import Config
from datetime import datetime
import asyncio
import edge_tts
import ollama
from tqdm import tqdm 
from markdown_pdf import MarkdownPdf, Section
from googlenewsdecoder import gnewsdecoder

# Load feed URLs from YAML configuration
def load_feeds(config_path='feeds_gr.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config.get('feeds', [])

# Fetch and parse articles from RSS feeds
def fetch_articles(feed_urls, max_articles=25):
    articles = []
    print("Ανάκτηση και κατέβασμα άρθρων από πηγές RSS...\n")
    for url in tqdm(feed_urls, desc="Ανάκτηση πηγών", unit="πηγές"):
        feed = feedparser.parse(url)
        for entry in feed.entries[:max_articles]:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', 'N/A')
            })
    return articles

# Use Ollama to summarize text
def summarize_with_ollama(text, model=SUMMARY_MODEL):
    prompt = (
        "Συνόψισε το ακόλουθο άρθρο ειδήσεων σε 3-5 προτάσεις, εστιάζοντας στα βασικά γεγονότα, το πλαίσιο και τις επιπτώσεις. "
        "Απέφυγε τις εικασίες και την έκφραση άποψης.\n\n"
        f"{text}\n\nΠερίληψη:"
    )
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Extract and summarize article content using Ollama
def summarize_articles(articles, model=SUMMARY_MODEL):
    summaries = []
    print("\nΔημιουργία περιλήψεων των άρθρων που ανακτήθηκαν...\n")
    for article in tqdm(articles, desc="Πρόοδος", unit="άρθρο"):
        try:
            if "news.google.com" in article['link']:
                interval_time = 1  # interval is optional, default is None
                source_url = article['link']
                try:
                    decoded_url = gnewsdecoder(source_url, interval=interval_time)

                    if decoded_url.get("status"):
                        #print("Decoded URL:", decoded_url["decoded_url"])
                        article['link'] = decoded_url["decoded_url"]
                    else:
                        print("Error:", decoded_url["message"])
                        article['link'] = ""
                except Exception as e:
                    print(f"Error occurred: {e}")
                    article['link'] = ""
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            config = Config()
            config.browser_user_agent = user_agent
            news_article = Article(article['link'], config=config)
            news_article.download()
            news_article.parse()
            text = news_article.text #[:2000]
            #print(article['link'])
            summary = summarize_with_ollama(text, model=model)
            summaries.append({
                'title': article['title'],
                'link': article['link'],
                'published': article['published'],
                'summary': summary
            })
            #print(summary)
        except Exception as e:
            print(f"Error processing article: {article['link']}\n{e}")
    return summaries

# Use Ollama to generate a cohesive news broadcast from all summaries
def generate_broadcast(summaries, model=BROADCAST_MODEL):
    joined_summaries = "\n\n".join(
        f"Τίτλος: {s['title']}\nΠερίληψη: {s['summary']}" for s in summaries
    )
    prompt = (
        "Είσαι επαγγελματίας δημοσιογράφος. Δημιούργησε ένα συνεκτικό δελτίο ειδησεογραφικής ενημέρωσης με βάση τις ακόλουθες περιλήψεις άρθρων. "
        "Συνδύασε τις περιλήψεις σε μια ομαλή αφήγηση χωρίς επαναλήψεις, ομαδοποιώντας σχετικά θέματα και διατηρώντας ενημερωτικό και ουδέτερο χαρακτήρα.:\n\n"
        f"{joined_summaries}\n\nΔελτίο ειδήσεων:"
    )
    print("Αριθμός λέξεων στο prompt: ", len(prompt.split()), ".")
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Save full broadcast with timestamped filename
def save_digest(digest_text, output_dir='.'):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(output_dir, f'GR_digest_{timestamp}.md')
    with open(filename, 'w') as file:
        file.write(digest_text)
    try:
        #pdf = MarkdownPdf(toc_level=4, optimize=True)
        pdf = MarkdownPdf(optimize=True)
        pdf.add_section(Section(open(filename, encoding='utf-8').read()))
        pdf.meta["title"] = "News Bulletin"
        pdf.save('Bulletin_GR.pdf')
    except:
        print('Πρόβλημα με την παραγωγή του PDF..')
    return filename  # return path for TTS to use

# Convert broadcast to speech with timestamped filename
async def text_to_speech(text, output_path, voice=TTS_VOICE):
    communicate = edge_tts.Communicate(text.replace('*', ' ').replace('&', ' και ').replace(':', '.'), voice=voice)
    await communicate.save(output_path)

# Main workflow
def main():
    feed_urls = load_feeds()
    articles = fetch_articles(feed_urls, max_articles=25)
    summaries = summarize_articles(articles)
    print('Παραγωγή σύνοψης εισήσεων...')
    broadcast = generate_broadcast(summaries)
    # Save digest and get timestamped filename
    digest_path = save_digest(broadcast)

    # Create matching timestamped mp3 path
    mp3_path = digest_path.replace('.md', '.mp3')
    asyncio.run(text_to_speech(broadcast, output_path=mp3_path))

if __name__ == "__main__":
    main()
