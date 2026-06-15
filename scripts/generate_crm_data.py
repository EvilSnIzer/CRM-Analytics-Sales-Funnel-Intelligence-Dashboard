import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate Sales Reps
regions = ['North America', 'EMEA', 'APAC', 'LATAM']
reps = pd.DataFrame({
    'RepID': range(1, 21),
    'RepName': [f'Rep_{i}' for i in range(1, 21)],
    'Region': np.random.choice(regions, 20),
    'TenureMonths': np.random.randint(1, 60, 20)
})
reps.to_csv('sales_reps.csv', index=False)

# Generate Leads
n_leads = 50000
sources = ['Organic Search', 'Paid Social', 'Cold Call', 'Referral', 'Webinar']
industries = ['Tech', 'Healthcare', 'Finance', 'Manufacturing', 'Retail']
sizes = ['SMB', 'Mid-Market', 'Enterprise']

leads = pd.DataFrame({
    'LeadID': range(1, n_leads + 1),
    'RepID': np.random.choice(range(1, 21), n_leads),
    'LeadSource': np.random.choice(sources, n_leads, p=[0.3, 0.2, 0.15, 0.1, 0.25]),
    'Industry': np.random.choice(industries, n_leads),
    'CompanySize': np.random.choice(sizes, n_leads, p=[0.5, 0.3, 0.2]),
    'DateCreated': [datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(n_leads)]
})

# Conversion logic: Referrals and Organic Search convert better. Tech and Enterprise convert better.
conversion_prob = np.ones(n_leads) * 0.1
conversion_prob[leads['LeadSource'] == 'Referral'] += 0.15
conversion_prob[leads['LeadSource'] == 'Organic Search'] += 0.05
conversion_prob[leads['Industry'] == 'Tech'] += 0.05
conversion_prob[leads['CompanySize'] == 'Enterprise'] += 0.05
conversion_prob[leads['CompanySize'] == 'SMB'] -= 0.02
conversion_prob = np.clip(conversion_prob, 0, 1)

leads['IsConverted'] = np.random.binomial(1, conversion_prob)
leads.to_csv('leads.csv', index=False)

# Generate Opportunities (only for converted leads)
converted_leads = leads[leads['IsConverted'] == 1].copy()
n_opps = len(converted_leads)
products = ['SaaS Basic', 'SaaS Pro', 'SaaS Enterprise', 'Consulting']

opps = pd.DataFrame({
    'OppID': range(1, n_opps + 1),
    'LeadID': converted_leads['LeadID'].values,
    'Product': np.random.choice(products, n_opps, p=[0.4, 0.3, 0.2, 0.1]),
    'Amount': np.random.choice([5000, 10000, 25000, 50000], n_opps),
})

# Win logic
win_prob = np.ones(n_opps) * 0.4
win_prob[opps['Product'] == 'SaaS Basic'] += 0.2
win_prob[opps['Product'] == 'SaaS Enterprise'] -= 0.15
win_prob = np.clip(win_prob, 0, 1)

opps['IsWon'] = np.random.binomial(1, win_prob)
opps['Stage'] = np.where(opps['IsWon'] == 1, 'Closed Won', 'Closed Lost')
opps['DateClosed'] = converted_leads['DateCreated'].values + pd.to_timedelta(np.random.randint(15, 90, n_opps), unit='D')
opps.to_csv('opportunities.csv', index=False)

# Generate Accounts (only for won opportunities)
won_opps = opps[opps['IsWon'] == 1].copy()
n_accounts = len(won_opps)

accounts = pd.DataFrame({
    'AccountID': range(1, n_accounts + 1),
    'OppID': won_opps['OppID'].values,
    'OnboardingScore': np.random.randint(1, 100, n_accounts),
    'SupportTickets': np.random.randint(0, 20, n_accounts)
})

# Churn logic: high support tickets and low onboarding score = higher churn
churn_prob = np.ones(n_accounts) * 0.05
churn_prob[accounts['SupportTickets'] > 10] += 0.15
churn_prob[accounts['OnboardingScore'] < 40] += 0.2
churn_prob = np.clip(churn_prob, 0, 1)

accounts['IsChurned'] = np.random.binomial(1, churn_prob)
accounts.to_csv('accounts.csv', index=False)

print("Generated sales_reps.csv, leads.csv, opportunities.csv, accounts.csv")
