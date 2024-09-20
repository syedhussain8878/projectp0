from fastapi import FastAPI
from fastapi.responses import FileResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = FastAPI()

# Load the CSV file with error handling for encoding
csv_file_path = "diwali_sales.csv"
try:
    df = pd.read_csv(csv_file_path, encoding='latin1')  # Adjust encoding if needed
except UnicodeDecodeError:
    df = pd.read_csv(csv_file_path, encoding='utf-8-sig')  # Try a different encoding if needed

# Drop unrelated/blank columns
df.drop(['Status', 'unnamed1'], axis=1, inplace=True)

# Check for null values and drop them
df.dropna(inplace=True)

# Convert 'Amount' column to integer
df['Amount'] = df['Amount'].astype(int)

# Ensure the 'plots' directory exists
if not os.path.exists('plots'):
    os.makedirs('plots')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Diwali Sales Analysis API!"}

@app.get("/plot/gender-count")
def plot_gender_count():
    plt.figure(figsize=(5, 5))
    ax = sns.countplot(x='Gender', data=df)
    ax.bar_label(ax.containers[0])
    plt.title("Count of Individuals by Gender")
    plot_path = "plots/gender_count.png"
    plt.savefig(plot_path)
    plt.close()
    summary = df['Gender'].value_counts().to_dict()
    return {
        "summary": summary,
        "plot_url": f"/plots/gender_count.png"
    }

@app.get("/plot/gender-sales")
def plot_gender_sales():
    plt.figure(figsize=(5, 5))
    sales_gen = df.groupby('Gender', as_index=False)['Amount'].sum().sort_values(by='Amount', ascending=False)
    sns.barplot(x='Gender', y='Amount', data=sales_gen)
    plt.title("Total Sales Amount by Gender")
    plot_path = "plots/gender_sales.png"
    plt.savefig(plot_path)
    plt.close()
    summary = sales_gen.to_dict(orient='records')
    return {
        "summary": summary,
        "plot_url": f"/plots/gender_sales.png"
    }

@app.get("/plot/age-group-sales")
def plot_age_group_sales():
    plt.figure(figsize=(6, 6))
    sales_age = df.groupby('Age Group', as_index=False)['Amount'].sum().sort_values(by='Amount', ascending=False)
    sns.barplot(x='Age Group', y='Amount', data=sales_age)
    plt.title("Total Sales Amount by Age Group")
    plot_path = "plots/age_group_sales.png"
    plt.savefig(plot_path)
    plt.close()
    summary = sales_age.to_dict(orient='records')
    return {
        "summary": summary,
        "plot_url": f"/plots/age_group_sales.png"
    }

@app.get("/plot/state-orders")
def plot_state_orders():
    plt.figure(figsize=(16, 5))
    sales_state = df.groupby('State', as_index=False)['Orders'].sum().sort_values(by='Orders', ascending=False).head(10)
    sns.barplot(data=sales_state, x='State', y='Orders')
    plt.title("Total Number of Orders From States")
    plot_path = "plots/state_orders.png"
    plt.savefig(plot_path)
    plt.close()
    summary = sales_state.to_dict(orient='records')
    return {
        "summary": summary,
        "plot_url": f"/plots/state_orders.png"
    }

@app.get("/plot/state-sales")
def plot_state_sales():
    plt.figure(figsize=(16, 5))
    sales_state = df.groupby('State', as_index=False)['Amount'].sum().sort_values(by='Amount', ascending=False).head(10)
    sns.barplot(data=sales_state, x='State', y='Amount')
    plt.title("Total Sales Amount by States")
    plot_path = "plots/state_sales.png"
    plt.savefig(plot_path)
    plt.close()
    summary = sales_state.to_dict(orient='records')
    return {
        "summary": summary,
        "plot_url": f"/plots/state_sales.png"
    }

@app.get("/plot/marital-status")
def plot_marital_status():
    plt.figure(figsize=(6, 6))
    ax = sns.countplot(data=df, x='Marital_Status')
    plt.title("Distribution of Marital Status Among Customers")
    for bars in ax.containers:
        ax.bar_label(bars)
    plot_path = "plots/marital_status.png"
    plt.savefig(plot_path)
    plt.close()
    summary = df['Marital_Status'].value_counts().to_dict()
    return {
        "summary": summary,
        "plot_url": f"/plots/marital_status.png"
    }

@app.get("/plot/occupation")
def plot_occupation():
    plt.figure(figsize=(6, 6))
    ax = sns.countplot(data=df, x='Occupation')
    plt.title("Distribution of Customers by Occupation")
    for bars in ax.containers:
        ax.bar_label(bars)
    plot_path = "plots/occupation.png"
    plt.savefig(plot_path)
    plt.close()
    summary = df['Occupation'].value_counts().to_dict()
    return {
        "summary": summary,
        "plot_url": f"/plots/occupation.png"
    }

@app.get("/plot/product-category")
def plot_product_category():
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Product_Category')
    plt.xlabel('Product_Category')
    plt.ylabel('Count')
    plt.title('Distribution of Product Categories')
    plt.xticks(rotation=90)
    plot_path = "plots/product_category.png"
    plt.savefig(plot_path)
    plt.close()
    summary = df['Product_Category'].value_counts().to_dict()
    return {
        "summary": summary,
        "plot_url": f"/plots/product_category.png"
    }

@app.get("/plot/top-products")
def plot_top_products():
    plt.figure(figsize=(20, 5))
    top_products = df.groupby('Product_Category', as_index=False)['Orders'].sum().sort_values(by='Orders', ascending=False).head(10)
    sns.barplot(data=top_products, x='Product_Category', y='Orders')
    plt.title("Top 10 Products by Total Orders")
    plot_path = "plots/top_products.png"
    plt.savefig(plot_path)
    plt.close()
    summary = top_products.to_dict(orient='records')
    return {
        "summary": summary,
        "plot_url": f"/plots/top_products.png"
    }

@app.get("/plot/most-ordered-products")
def plot_most_ordered_products():
    plt.figure(figsize=(12, 7))
    df.groupby('Product_ID')['Orders'].sum().nlargest(10).sort_values(ascending=False).plot(kind='bar')
    plt.title("Top 10 Most Ordered Products by ID")
    plt.xlabel('Product ID')
    plt.ylabel('Orders')
    plot_path = "plots/most_ordered_products.png"
    plt.savefig(plot_path)
    plt.close()
    summary = df.groupby('Product_ID')['Orders'].sum().nlargest(10).to_dict()
    return {
        "summary": summary,
        "plot_url": f"/plots/most_ordered_products.png"
    }

@app.get("/plot/state-distribution")
def plot_state_distribution():
    plt.figure(figsize=(20, 10))
    sns.histplot(data=df, x="State")
    plt.title("Distribution of Orders by State")
    plot_path = "plots/state_distribution.png"
    plt.savefig(plot_path)
    plt.close()
    summary = df['State'].value_counts().to_dict()
    return {
        "summary": summary,
        "plot_url": f"/plots/state_distribution.png"
    }

@app.get("/plots/{filename}")
def get_plot(filename: str):
    file_path = os.path.join("plots", filename)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}
