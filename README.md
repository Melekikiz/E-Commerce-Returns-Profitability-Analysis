# E-Commerce-Returns-Profitability-Analysis
📌 Project Overview

This project presents an end-to-end business-driven e-commerce analytics case study, focusing on return behavior, profitability impact, and customer segmentation.

Rather than only visualizing data, the analysis investigates why returns occur, where they financially hurt the business, and which customer and product segments require strategic action.

The dataset simulates a global premium e-commerce company operating across multiple countries, channels, and product categories.

# 🎯 Business Questions Addressed

Are product returns driven by channels, countries, or categories?

Do returns indicate systematic abuse or fraud?

Which products create disproportionate margin loss?

How do customer value and return behavior interact?

Which customer segments require different operational strategies?

# 🗂️ Dataset Structure

The project uses relational CSV datasets resembling a real-world production environment:

customers.csv  customer demographics & geography

products.csv  product prices, costs, and categories

orders.csv  order lifecycle, status, dates, channels

order_details.csv  line-item order breakdown

# Total scale:

450,000 orders

~80,000 customers

1.1M+ order line items

Global multi-channel setup

# 🔧 Tools & Technologies

Python

Pandas: data transformation & aggregation

NumPy: numerical operations

Matplotlib: data visualization


# 🧮 Key KPIs Calculated

Net Revenue & Net Margin

Average Order Value (AOV)

Orders per Customer

Return Rate (%)

Returned Revenue & Margin Impact

Product-level return cost

Customer lifetime value & behavior metrics

# 📈 Analysis Flow

The analysis follows a structured business logic, not ad-hoc exploration:

1️⃣ Company-Level Performance

Revenue trends

Order volume stability

Return rate evolution over time

2️⃣ Operational Return Analysis

Return rate by:

Country

Channel

Category

Finding:
Return rates remain consistently around ~4%, indicating no structural operational issues.

3️⃣ Revenue & Margin Impact of Returns

Returned revenue by channel

Revenue impact ratio

Margin loss analysis

Finding:
Returns are channel-agnostic. The problem is not frequency it’s financial impact.

4️⃣ Product-Level Risk Detection

Product return rates

Returned revenue & margin loss per product

Key Insight:
A small subset of high-margin products accounts for a disproportionate share of total margin loss.

5️⃣ Customer Return Behavior

Customers with returns: ~20%

Median returned orders: 1

Max returned orders: 4

Finding:
There is no return abuse or fraud pattern. Returns are isolated, one-off events.

6️⃣ Business-Oriented Customer Segmentation

Customers are segmented by:

Value (High / Low)

Return behavior (Returned / No Return)

Final segments:

High Value – No Return

High Value – Returned

Low Value – No Return

Low Value – Returned

# 🧠 Strategic Insights

High-value customers remain profitable even if they return products.

Low-value returning customers generate low revenue and high operational cost.

Return behavior is not related to spending power, but to product-level issues.

The core problem is expectation mismatch on high-margin products, not customer abuse.

# 📌 Actionable Business Recommendations
🔹 High Value – No Return

VIP loyalty programs

Early access & premium support

🔹 High Value – Returned

Improved product descriptions

Size/fit guidance

Exchange-over-return incentives

Proactive support

🔹 Low Value – Returned

Return policy optimization

Minimum basket thresholds

Return fee experiments

Cost control focus

🔹 Low Value – No Return

Upsell & cross-sell strategies

Conversion into high-value customers

# 🏆Conclusion

The business demonstrates strong customer loyalty with high order frequency and premium basket value.
Return rates remain under control at ~4% and are not driven by operational or regional factors.
Profitability risk is concentrated in a limited number of high-margin products rather than customer behavior.
Optimization efforts should focus on product experience and segment-based strategies, not restrictive return policies.

# 🚀 Author

Melek Ikiz
Data Analyst | Business-Oriented Analytics | Python
GitHub: https://github.com/Melekikiz

# ⭐ Final Note

This project emphasizes decision-making, profitability, and business impact, not just descriptive analytics.
It is designed to reflect real stakeholder expectations in consulting, analytics, and freelance environments.
