# 📊 CRM Analytics & Sales Funnel Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=Power%20BI&logoColor=white)

An end-to-end CRM analytics pipeline processing 50K+ lead records to generate actionable sales intelligence. This project engineers relational datasets, applies machine learning for lead scoring and churn prediction, and culminates in a comprehensive Business Intelligence dashboard.

## 🎯 Business Value Generated
* **Pipeline Visibility:** Engineered SQL joins across 4 relational tables (Reps, Leads, Opportunities, Accounts) to expose funnel bottlenecks.
* **Lead Scoring (ML):** Applied logistic regression for conversion prediction (85% accuracy), allowing the sales team to prioritize high-intent leads.
* **Churn Prevention:** Modeled customer churn risk based on onboarding scores and support tickets.
* **Actionable BI:** Designed a multi-tab Power BI dashboard with rep-level and regional drill-down capabilities.

## 🗄️ Relational Data Schema
This project mirrors a real-world Salesforce / HubSpot CRM database structure:
1. `Sales_Reps` (1:N with Leads)
2. `Leads` (1:1 with Opportunities)
3. `Opportunities` (1:1 with Accounts)
4. `Accounts` (Post-sale customer health)

## 📂 Repository Structure
```text
├── scripts/
│   ├── generate_crm_data.py        # Generates a 50k+ record synthetic CRM dataset
│   └── predict_conversion_churn.py # Scikit-Learn ML pipeline for lead/churn scoring
├── sql/
│   └── funnel_analysis.sql         # Complex SQL aggregations for funnel metrics
├── requirements.txt                # Python dependencies
├── .gitignore
└── README.md
```

## 🚀 Quickstart: Running the Project Locally

### 1. Set up the environment
```bash
pip install -r requirements.txt
```

### 2. Generate the CRM Database
Run the data generation script. This will create realistic, relational CSV files simulating years of CRM history.
```bash
python scripts/generate_crm_data.py
```

### 3. Run the Machine Learning Pipeline
Train the Logistic Regression models and append AI-driven probabilities to your leads and accounts.
```bash
python scripts/predict_conversion_churn.py
```


## 🧠 Machine Learning Details
* **Lead Conversion Model:** Utilizes `OneHotEncoder` and `LogisticRegression` inside a Scikit-Learn `Pipeline` to evaluate `LeadSource`, `Industry`, and `CompanySize`. 
* **Churn Prediction Model:** Uses `StandardScaler` on continuous variables like `SupportTickets` and `OnboardingScore` to flag "At-Risk" accounts before they cancel.
