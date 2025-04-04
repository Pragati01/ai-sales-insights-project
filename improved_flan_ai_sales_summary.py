
import pandas as pd
import random
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns
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

def compute_pandas_insights(df):
    summary = []

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

    top_products = df.groupby("product")["total_sales"].sum().sort_values(ascending=False).head(3).index.tolist()
    top_countries = df.groupby("country")["total_sales"].sum().sort_values(ascending=False).head(3).index.tolist()

    Q1 = df['total_sales'].quantile(0.25)
    Q3 = df['total_sales'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['total_sales'] < Q1 - 1.5 * IQR) | (df['total_sales'] > Q3 + 1.5 * IQR)]

    recommendation = "Sales of 'Planes' have dropped significantly in the South region."

    summary.append(f"- Average sale value: ${avg:.2f}")
    summary.append(f"- Median: ${median:.2f}, Max: ${max_val:.2f}, Min: ${min_val:.2f}, Mode: {mode_val}")
    summary.append(f"- Highest transaction: ${max_row['total_sales']} ({max_row['product']} in {max_row['country']})")
    summary.append(f"- Lowest transaction: ${min_row['total_sales']} ({min_row['product']} in {min_row['country']})")
    summary.append(f"- Top 3 product lines: {', '.join(top_products)}")
    summary.append(f"- Top performing countries: {', '.join(top_countries)}")
    summary.append(f"- Outliers detected: {len(outliers)} transactions")
    summary.append(f"- Recommendation: {recommendation}")

    return "\n".join(summary)

def generate_ai_narrative(df, summary):
    df_sample = df[['product', 'region', 'country', 'quantity', 'unit_price', 'total_sales']].head(20)
    markdown = df_sample.to_markdown(index=False)

    prompt = f"""
You are a business analyst. Based on the following summary, write a short, professional narrative summary describing the sales performance, trends, anomalies, and recommendations.
Include top 3 performing countries and products, bottom 3 performing countries and products, max, min, avg sale values. 

Sales data Summary:
{summary}
"""

    result = summarizer(prompt, max_new_tokens=300, do_sample=True, temperature=0.7)[0]["generated_text"]
    return result.strip()

def generate_charts(df):
    os.makedirs("charts", exist_ok=True)

    df.groupby("product")["total_sales"].sum().plot(kind="bar", title="Total Sales by Product", color="skyblue")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig("charts/sales_by_product.png")
    plt.close()

    plt.figure(figsize=(10,6))
    sns.barplot(data=df, x="product", y="total_sales", hue="region")
    plt.title("Product Sales by Region")
    plt.tight_layout()
    plt.savefig("charts/sales_by_product_region.png")
    plt.close()

    plt.figure(figsize=(8,6))
    sns.boxplot(x="product", y="total_sales", data=df)
    plt.title("Sales Distribution per Product (Box Plot)")
    plt.tight_layout()
    plt.savefig("charts/sales_boxplot.png")
    plt.close()

def send_email(subject, body, attachments=[]):
    sender_email = os.environ["EMAIL_USERNAME"]
    app_password = os.environ["EMAIL_APP_PASSWORD"]
    receiver_email = os.environ["EMAIL_RECEIVER"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    for attachment_path in attachments:
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
    df["date"] = pd.to_datetime(df["date"])
    max_date = df["date"].max().strftime("%b %d, %Y")

    pandas_summary = compute_pandas_insights(df)
    ai_narrative = generate_ai_narrative(df, pandas_summary)
    generate_charts(df)

    subject = f"📈 AI Sales Report – {max_date}"
    full_report = f"📊 Python-Generated Insights:\n{pandas_summary}\n\n🤖 AI-Powered Narrative:\n{ai_narrative}"

    print(subject)
    print(full_report)

    send_email(
        subject=subject,
        body=full_report,
        attachments=[
            "charts/sales_by_product.png",
            "charts/sales_by_product_region.png",
            "charts/sales_boxplot.png"
        ]
    )
