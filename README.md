# 📰 Greek News AI Digest

Python script το οποίο ανακτά άρθρα από RSS feed, τα συνοψίψει χρησιμοποιώντας το LLM [llama Krikri](https://ollama.com/ilsp/llama-krikri-8b-instruct) (μέσω Ollama), και τελικά παράγει ένα συνθετικό σύντομο δελτίο ειδήσεων σε PDF format και σε MP3 audio στα ελληνικά. Ο κώδικας βασίστηκε εκτεταμένα στο project [News02](https://github.com/kliewerdaniel/News02)

---

## 📦 Εγκατάσταση

1. **Clone repository:**
   ```bash
   git clone https://github.com/alexandros-koutsioumpas/GRNewsAI.git
   cd GRNewsAI
   ```

2. **Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Εγκατάσταση Ollama (αν δεν είναι ήδη εγκατεστημένο):**
   Οδηγίες εδώ https://ollama.com

   ακολούθως

   ```bash
   ollama pull ilsp/llama-krikri-8b-instruct:latest
   ```
4. Σε ορισμένους υπολογιστές χρειάζεται να "τρέξετε" το `Python Install Certificates script` (στο `MacOS` θα το βρείτε στο `Applications/Python/Install Certificates.command`)

---

## 📄 feeds_gr.yaml το αρχείο περιέχει τα RSS feeds

μπορείτε να προσθέσετε RSS links στο αρχείο. Με '#' στην αρχή της γραμμής η πηγή θα αγνοηθεί.

```yaml
feeds:
  - "https://news.google.com/rss?gl=GR&hl=el&ceid=GR:el"
  - "https://feeds.feedburner.com/kathimerini/DJpy"
  - "https://www.tanea.gr/feed/"
  - "https://www.tovima.gr/feed/"
  - "https://www.protothema.gr/rsscategory/rss/"
  - "https://www.naftemporiki.gr/newsroom/feed/"
  - "https://www.ethnos.gr/rss"
  - "http://feeds.feedburner.com/skai/Uulu"
  - "https://tvxs.gr/feed/"
  - "https://www.ot.gr/feed"
#  - "https://www.newsit.gr/feed/"
#  - "https://www.megatv.com/feed/"
#  - "https://www.in.gr/feed/"
#  - "https://www.news.gr/rss.ashx"
#  - "https://www.902.gr/feed/featured"
#  - "https://www.newsbomb.gr/oles-oi-eidhseis?format=feed&type=rss"
#  - "https://www.protagon.gr/feed"
```

Αν ο κώδικας αργεί στο μηχάνημα σας, αφαιρέστε πηγές.

---

## 🚀 Running the Script

```bash
python news_digest_gr.py
```

Το script θα:
- Ανακτήσει 25 άρθρα (μέγιστο) ανα feed
- θα τα συνοψίσει
- θα παράγει ένα συνεκτικό δελτίο σε μορφή markdown text, pdf document και mp3 audio

---

## 🗣️ Επιλογή Φωνής

- `el-GR-NestorasNeural` (default, ανδρική)
- `el-GR-AthinaNeural` (γυναικεία)


---

## 🧠 Tips

Με 10 RSS feed και `max_articles=25` σε ένα MacBook Pro M4 η παραγωγή του δελτίου διαρκεί ~30min.. 

- Με λιγότερα `max_articles` ο κώδικας τρέχει γρηγορότερα
- Αλλάζοντας το `SUMMARY_MODEL` και `BROADCAST_MODEL` σε quantized KriKri π.χ. (ilsp/llama-krikri-8b-instruct:q3_k_m) ίσως κάνει τον κώδικα πιο γρήγορο σε σχετικά παλιά μηχανήματα.

---

## 🔒 License

MIT License
