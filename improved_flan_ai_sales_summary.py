
import pandas as pd
import random
import datetime
import os
import matplotlib.pyplot as plt
from statistics import mode
from transformers import pipeline
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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
1. **Sales Trends** – summarize key patterns in sales data
2. **Anomalies** – identify unusual sales or outliers
3. **Observations** – provide general analysis of what the data suggests
4. **Recommendations** – what actions should be taken next?

Facts:
{fact_block}

Charts available:
- Sales by Product
- Product Sales by Region
- Sales Distribution per Product (Box Plot)

Example:
- Sales Trends: Sales increased for Classic Cars and Planes.
- Anomalies: One transaction over $20,000 was recorded for Planes in Germany.
- Observations: Sales are consistent across all products except Ships.
- Recommendations: Focus marketing efforts on Planes in West region.

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

def send_email(subject, body, attachment_path):
    sender_email = os.environ["pragatikhedkar15@gmail.com"]
    app_password = os.environ["jlkrvlrlthmhuikw"]
    receiver_email = os.environ["pragatikhedkar15@gmail.com"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach the chart
    with open(attachment_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    df = simulate_data()
    summary = generate_summary(df)
    insight = generate_ai_insight(summary)
    generate_chart(df)

    full_text = f"{summary}\n\n---\n\n{insight}"
    print(full_text)

    send_email(
        subject="📈 Daily AI Sales Summary",
        body=full_text,
        attachment_path="charts/sales_by_product.png"
    )
