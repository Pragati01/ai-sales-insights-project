
import pandas as pd
import random
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import mode
from transformers import pipeline

# Load model
summarizer = pipeline("text2text-generation", model="google/flan-t5-xl")

def simulate_data():
    today = datetime.date.today().isoformat()
    data = []
    for i in range(50):
        record = {
            "order_id": 1000 + i,
            "date": today,
            "product": random.choice(["Classic Cars", "Vintage Cars", "Motorcycles", "Planes", "Ships"]),
            "quantity": random.randint(1, 5),
            "unit_price": round(random.uniform(500, 5000), 2),
            "region": random.choice(["North", "South", "East", "West"]),
            "country": random.choice(["USA", "Spain", "France", "Germany", "India"])
        }
        record["total_sales"] = round(record["quantity"] * record["unit_price"], 2)
        data.append(record)
    return pd.DataFrame(data)

def generate_summary(df):
    avg = df['total_sales'].mean()
    median = df['total_sales'].median()
    min_val = df['total_sales'].min()
    max_val = df['total_sales'].max()
    try:
        mode_val = mode(df['total_sales'])
    except:
        mode_val = "No unique mode"
    max_row = df.loc[df['total_sales'].idxmax()]
    min_row = df.loc[df['total_sales'].idxmin()]
    summary = f"""- Average sale value: ${avg:.2f}
- Median: ${median:.2f}
- Mode: {mode_val}
- Max: ${max_val:.2f} ({max_row['product']} in {max_row['country']})
- Min: ${min_val:.2f} ({min_row['product']} in {min_row['country']})"""
    return summary

def generate_ai_insight(summary):
    prompt = f"""
You are an experienced business analyst. Based on the following sales statistics and chart insights, generate a detailed business intelligence report.

Your response MUST include the following markdown sections **with actual insights**:
1. **Sales Trends**
2. **Anomalies**
3. **Observations**
4. **Recommendations**

Facts:
{summary}

Charts available:
- Sales by Product
- Product Sales by Region
- Sales Distribution per Product (Box Plot)

Write the full response.
"""
    result = summarizer(prompt, max_new_tokens=512, do_sample=True, temperature=0.7)[0]["generated_text"]
    return result.strip()

def generate_chart(df):
    os.makedirs("charts", exist_ok=True)
    df.groupby("product")["total_sales"].sum().plot(kind="bar", title="Total Sales by Product", color="skyblue")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig("charts/sales_by_product.png")

if __name__ == "__main__":
    df = simulate_data()
    summary = generate_summary(df)
    insight = generate_ai_insight(summary)
    generate_chart(df)

    print("📊 Summary:\n", summary)
    print("\n🤖 AI Insight:\n", insight)
