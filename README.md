
# 📈 AI-Powered Sales Insight Automation

This project automatically generates daily sales insights by combining **Python analytics** with **AI-generated narratives**, and sends them via email — fully automated using **GitHub Actions**.

---

## 🚀 Features

- ✅ **Simulated sales dataset** with realistic fields
- 📊 Insight generation using **pandas**:
  - Average, Median, Mode
  - Highest/Lowest transactions
  - Top products & countries
  - Outlier detection
  - Smart recommendations
- 🤖 Insight **narratives written by AI** (using Hugging Face `flan-t5-xl`)
- ✉️ **Emails the insights daily** via Gmail SMTP
- 🕒 Fully **automated using GitHub Actions**
- 🔐 Sensative credentials stored in Secrets variables

---

## 📦 Dependencies

Add these to your `requirements.txt`:

```
transformers
pandas
matplotlib
seaborn
```

Also installed in GitHub Actions via:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## 🧠 Example Output (in email)

```
📊 Python-Generated Insights:
- Average sale value: $8318.37
- Median: $7304.39, Max: $19772.30, Min: $566.45, Mode: 5059.7
- Highest transaction: $19772.3 (Motorcycles in France)
- Lowest transaction: $566.45 (Motorcycles in Germany)
- Top 3 product lines: Planes, Classic Cars, Vintage Cars
- Top performing countries: USA, Germany, Spain
- Outliers detected: 0 transactions
- Recommendation: Sales of 'Planes' have dropped significantly in the South region.

🤖 AI-Powered Narrative:
The top 3 performing countries and products are: Germany ($60,000.68) - Spain ($24,674.95) - France ($4,342) The top performing products are: Ships in Spain - Cars in France
```

---

## 🛠 How to Deploy

1. Upload files to your GitHub repo
2. Set the required secrets (see above)
3. Push `.github/workflows/schedule.yml` to enable daily automation
4. Sit back and let the AI deliver your sales report every morning!

---

## 🧠 Built With

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Python, pandas, matplotlib, seaborn]
