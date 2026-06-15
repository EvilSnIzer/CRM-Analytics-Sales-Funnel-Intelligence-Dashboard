import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load Data
leads = pd.read_csv('leads.csv')
opps = pd.read_csv('opportunities.csv')
accounts = pd.read_csv('accounts.csv')

print("--- LEAD CONVERSION PREDICTION ---")
# Features: LeadSource, Industry, CompanySize
X_leads = leads[['LeadSource', 'Industry', 'CompanySize']]
y_leads = leads['IsConverted']

# Preprocessing for categorical data
categorical_features = ['LeadSource', 'Industry', 'CompanySize']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ])

# Create pipeline with Logistic Regression
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression(max_iter=1000))])

X_train, X_test, y_train, y_test = train_test_split(X_leads, y_leads, test_size=0.2, random_state=42)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(f"Conversion Prediction Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))

# Add conversion probabilities back to leads for PowerBI
leads['ConversionProbability'] = clf.predict_proba(X_leads)[:, 1]
leads.to_csv('leads_scored.csv', index=False)
print("Saved scored leads to leads_scored.csv\n")


print("--- CHURN PREDICTION ---")
# Merge accounts with opportunities to get product data
acc_opps = pd.merge(accounts, opps, on='OppID')

X_churn = acc_opps[['OnboardingScore', 'SupportTickets', 'Product', 'Amount']]
y_churn = acc_opps['IsChurned']

numeric_features_churn = ['OnboardingScore', 'SupportTickets', 'Amount']
numeric_transformer_churn = StandardScaler()

categorical_features_churn = ['Product']
categorical_transformer_churn = OneHotEncoder(handle_unknown='ignore')

preprocessor_churn = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer_churn, numeric_features_churn),
        ('cat', categorical_transformer_churn, categorical_features_churn)
    ])

clf_churn = Pipeline(steps=[('preprocessor', preprocessor_churn),
                            ('classifier', LogisticRegression(max_iter=1000))])

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_churn, y_churn, test_size=0.2, random_state=42)
clf_churn.fit(X_train_c, y_train_c)
y_pred_c = clf_churn.predict(X_test_c)

print(f"Churn Prediction Accuracy: {accuracy_score(y_test_c, y_pred_c):.2%}")
print(classification_report(y_test_c, y_pred_c))

# Add churn probabilities back for PowerBI
accounts['ChurnProbability'] = clf_churn.predict_proba(X_churn)[:, 1]
accounts.to_csv('accounts_scored.csv', index=False)
print("Saved scored accounts to accounts_scored.csv")
