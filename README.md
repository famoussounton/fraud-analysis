# 🛡️ FraudSense Analytics

**FraudSense Analytics** is a comprehensive data analysis and visualization project designed to detect, analyze, and investigate fraudulent financial transactions. This project utilizes a modern tech stack including **Polars** for high-performance data processing and **Streamlit** for an interactive, enterprise-grade dashboard.

## 🚀 Features

*   **⚡ High-Performance Processing**: Uses Polars to handle millions of transactions efficiently.
*   **📊 Executive Dashboard**: Real-time overview of transaction volumes, fraud rates, and operational metrics.
*   **🔍 Deep Dive Analysis**: Advanced visualizations to uncover fraud patterns (e.g., Transfer -> Cash Out schemes).
*   **🕵️ Forensic Investigation Tool**: Search and trace specific account activities across the entire dataset.
*   **🎨 Premium UI**: "Midnight Pro" dark theme designed for professional financial environments.

## 📂 Project Structure

```bash
fraud-analysis/
├── data/                   
│   └── fraud_data_chunks/  # Split parquet files
├── notebooks/              # Jupyter Notebooks for analysis
│   ├── 01_data_loading.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   └── 04_feature_engineering.ipynb
├── streamlit_app/          # Streamlit Dashboard Application
│   ├── app.py              # Main entry point
│   ├── utils.py            # Shared styling and logic
│   └── pages/              # Dashboard pages
│       ├── 1_Overview.py
│       ├── 2_Fraud_Analysis.py
│       └── 3_Account_Investigation.py
├── fraud_db.sql            # Database schema/queries
├── requirements.txt        # Python dependencies
├── split_data.py           # Script to split data
└── README.md               # Project documentation
```

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/fraud-analysis.git
    cd fraud-analysis
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare Data:**
    Ensure you have the dataset in the `data/` folder. You can download the initial dataset from this link:
    👉 **[Download Initial Dataset (Google Drive)](https://drive.google.com/file/d/1ZVtrvkTPbM1_SytmHRu0wcYcJHhfqQif/view?usp=sharing)**
    
    If starting from raw CSV, run the notebooks in order (01 to 04) to generate `final.parquet`.

## 🖥️ Running the Dashboard

To launch the FraudSense Analytics dashboard:

```bash
streamlit run streamlit_app/app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 📈 Key Insights

*   **Fraud Vectors**: The majority of fraud occurs via `TRANSFER` and `CASH_OUT` transaction types.
*   **Account Draining**: High correlation found between `oldBalanceOrg` and `amount`, indicating attackers drain accounts completely.
*   **Detection Gaps**: A significant portion of high-value fraud is missed by traditional flagging systems (visualized in the app).

## ☁️ Deployment

Check out the live application on Streamlit Cloud:
👉 **[FraudSense Analytics Live App](https://sountonfamous-fraud-analysis.streamlit.app)**

This app is ready for deployment:
1.  Push code to GitHub.
2.  Connect your repository to Streamlit Cloud.
3.  Deploy!

---
*Created for Portfolio purposes.*
