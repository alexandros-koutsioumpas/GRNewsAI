# 📰 Greek News AI Digest

![alt text](GRnewsAI_image.jpeg?raw=true)

Python script το οποίο ανακτά άρθρα από RSS feed που καθορίζονται από τον χρήστη, τα συνοψίζει τοπικά στον υπολογιστή του χρήστη χρησιμοποιώντας το LLM [Llama Krikri](https://ollama.com/ilsp/llama-krikri-8b-instruct) (μέσω Ollama), και τελικά παράγει ένα συνθετικό σύντομο δελτίο ειδήσεων σε PDF format και σε MP3 audio στα ελληνικά για αυστηρά προσωπική χρήση. Αποτελεί ευθύνη του χρήστη ο σεβασμός των κανόνων πνευματικής ιδιοκτησίας των πηγών που χρησιμοποιεί. Ο κώδικας βασίστηκε εκτεταμένα στο project [News02](https://github.com/kliewerdaniel/News02) και σε αυτό το στάδιο αποτελεί ένα πείραμα για το πως μπορεί κάποιος τοπικά στο μηχάνημα του (άρα με ασφάλεια και κόστος μόνο την ενέργεια που καταναλώνει η GPU/CPU) να χρησιμοποιεί μεγάλα γλωσσικά μοντέλα για τη "διύλιση" πληροφορίας.

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

Οι πηγές RSS στο αρχείο είναι ενδεικτικές, μπορείτε να προσθέσετε/αφαιρέσετε RSS links. Με `#` στην αρχή της γραμμής η πηγή θα αγνοηθεί. **Πριν την πρώτη εκτέλεση του script** ο χρήστης οφείλει να διαμορφώσει το αρχείο με τις πηγές που επιθυμεί.

```yaml
feeds:
#  - "https://www.tanea.gr/feed/"
#  - "https://www.tovima.gr/feed/"
#  - "https://www.news.gr/rss.ashx"
#  - "https://www.902.gr/feed/featured"
#  - "https://www.newsbomb.gr/oles-oi-eidhseis?format=feed&type=rss"
#  - "https://www.protagon.gr/feed"
```

Αν ο κώδικας αργεί στο μηχάνημα σας, αφαιρέστε πηγές.

---

## 🚀 Εκτέλεση του Script

αφού έχετε κατάλληλα διαμορφώσει το αρχείο `feeds_gr.yaml`

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

Με 10 RSS feed και `max_articles=25` σε ένα MacBook Pro M4 η παραγωγή του δελτίου διαρκεί ~30min. Γενικά σε PC που δεν έχουν GPU και VRAM αρκετή να "σηκώσει" το Llama KriKri αναμένεται το runtime να είναι αρκετά μεγαλύτερο.

- Με λιγότερα `max_articles` ο κώδικας τρέχει γρηγορότερα
- Αλλάζοντας το `SUMMARY_MODEL` και `BROADCAST_MODEL` σε "ελαφρύτερο" μοντέλο (π.χ. [gemma3:4b]([https://ollama.com/ilsp/meltemi-instruct](https://ollama.com/library/gemma3:4b))) και περιορίζοντας τα RSS feed βοηθάει για να τρέξει κάποιος τον κώδικα σε σχετικά παλιά μηχανήματα με λιγότερη RAM και χωρίς GPU, αλλά το Llama KriKri κάνει πολύ καλύτερη δουλειά..

---

## 🔒 License

MIT License
