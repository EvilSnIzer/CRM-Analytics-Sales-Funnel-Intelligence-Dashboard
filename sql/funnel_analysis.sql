-- 1. Funnel Conversion by Channel
SELECT 
    l.LeadSource,
    COUNT(l.LeadID) AS TotalLeads,
    SUM(CASE WHEN l.IsConverted = 1 THEN 1 ELSE 0 END) AS ConvertedLeads,
    ROUND(CAST(SUM(CASE WHEN l.IsConverted = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(l.LeadID) * 100, 2) AS ConversionRatePct
FROM Leads l
GROUP BY l.LeadSource
ORDER BY ConversionRatePct DESC;

-- 2. Sales Rep Performance & Pipeline
SELECT 
    r.RepName,
    r.Region,
    COUNT(l.LeadID) AS LeadsAssigned,
    SUM(CASE WHEN l.IsConverted = 1 THEN 1 ELSE 0 END) AS LeadsConverted,
    COUNT(o.OppID) AS OpportunitiesCreated,
    SUM(CASE WHEN o.IsWon = 1 THEN 1 ELSE 0 END) AS DealsWon,
    SUM(CASE WHEN o.IsWon = 1 THEN o.Amount ELSE 0 END) AS TotalRevenueGenerated
FROM Sales_Reps r
LEFT JOIN Leads l ON r.RepID = l.RepID
LEFT JOIN Opportunities o ON l.LeadID = o.LeadID
GROUP BY r.RepName, r.Region
ORDER BY TotalRevenueGenerated DESC;

-- 3. Churn Risk by Product
SELECT 
    o.Product,
    COUNT(a.AccountID) AS TotalAccounts,
    SUM(CASE WHEN a.IsChurned = 1 THEN 1 ELSE 0 END) AS ChurnedAccounts,
    ROUND(CAST(SUM(CASE WHEN a.IsChurned = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(a.AccountID) * 100, 2) AS ChurnRatePct
FROM Accounts a
JOIN Opportunities o ON a.OppID = o.OppID
GROUP BY o.Product
ORDER BY ChurnRatePct DESC;
