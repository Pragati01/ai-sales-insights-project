
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

<img width="880" alt="image" src="https://github.com/user-attachments/assets/4a1caf3f-4736-4bfd-bfe6-f688abb4852f" />


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
