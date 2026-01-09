import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

customers=pd.read_csv("data/customers.csv")
products=pd.read_csv("data/products.csv")
orders=pd.read_csv("data/orders.csv", parse_dates=["order_date","delivery_date", "return_date"])
order_details=pd.read_csv("data/order_details.csv")

#Check the data
'''
print(customers.shape)
print(products.shape)
print(orders.shape)
print(order_details.shape)

print(order_details.head())

print(orders["status"].value_counts(normalize=True))
print(order_details["quantity"].describe())
print(products["price_usd"].describe)
'''

#Order Details add cost and margin
order_details=order_details.merge(
    products[["product_id", "cost_usd"]],
    on="product_id",
    how="left"
)

order_details["line_revenue"]=order_details["quantity"]*order_details["unit_price"]
order_details["line_cost"]=order_details["quantity"]* order_details["cost_usd"]
order_details["line_margin"]=order_details["line_revenue"] - order_details["line_cost"]

print(order_details[["line_revenue", "line_cost", "line_margin"]].describe())

#Summary table order based
order_summary=order_details.groupby("order_id").agg(
    revenue=("line_revenue", "sum"),
    cost=("line_cost", "sum"),
    margin=("line_margin", "sum"),
    items=("quantity", "sum")
).reset_index()

orders=orders.merge(order_summary, on="order_id", how="left")
print(orders[["revenue", "cost", "margin", "items"]].isnull().sum())

#Net Revenue
orders["net_revenue"]=np.where(
    orders["status"]== "Delivered",
    orders["revenue"],
    0
)
orders["net_margin"] = np.where(
    orders["status"]== "Delivered",
    orders["margin"],
    0
)

print(orders[["net_revenue", "net_margin"]].describe())
print(orders["net_revenue"].sum())

#Company-Level KPI 
kpi_summary = {
    "Total Net Revenue": orders["net_revenue"].sum(),
    "Total Orders": orders["order_id"].nunique(),
    "Total Customer": orders["customer_id"].nunique(),
    "Average Order Value":orders.loc[orders["net_revenue"] >0, "net_revenue"].mean(),
    "Orders per Customer": orders["order_id"].nunique() / orders["customer_id"].nunique(),
    "Return Rate (%)": (orders["status"] == "Returned").mean()* 100
}

pd.DataFrame.from_dict(kpi_summary, orient="index", columns=["Value"])

print(kpi_summary)

#Revenue Trend Graph
orders["order_month"] = orders["order_date"].dt.to_period("M").astype(str)
monthly_revenue=orders.groupby("order_month")["net_revenue"].sum().reset_index()
plt.figure(figsize=(12,5))
plt.plot(monthly_revenue["order_month"], monthly_revenue["net_revenue"])
plt.xticks(rotation=45)
plt.title("Monthly Net Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Net Revenue")
plt.tight_layout()
plt.show()

#Order Count
orders["order_date"]=pd.to_datetime(orders["order_date"])
monthly_orders=(
    orders.set_index("order_date")
    .resample("M")["order_id"]
    .nunique()
)
plt.figure(figsize=(10,5))
plt.plot(monthly_orders.index, monthly_orders.values)
plt.title("Monthly Order Count")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Monthly Return Rate
monthly_status = (
    orders.set_index("order_date")
    .groupby([pd.Grouper(freq="M"), "status"])
    .size().unstack(fill_value=0)
)
monthly_status["return_rate"]= (
    monthly_status["Returned"] /
    (monthly_status["Returned"] + monthly_status["Delivered"])
) * 100
plt.figure(figsize=(10,5))
plt.plot(monthly_status.index, monthly_status["return_rate"])
plt.title("Monthly Return Rate (%)")
plt.xlabel("Month")
plt.ylabel("Return Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Category Based Return Rate
#Join the order_details, product, category
df=(
    orders
    .merge(order_details, on="order_id", how="left")
    .merge(products[["product_id", "category"]], on="product_id", how="left")
)
category_return=(
    df.groupby("category")
    .apply(lambda x: (x["status"] == "Returned").mean() * 100)
    .reset_index(name="return_rate")
    .sort_values("return_rate", ascending=False)
)
plt.figure(figsize=(10,5))
plt.bar(category_return["category"], category_return["return_rate"])
plt.title("Return Rate by Category (%)")
plt.xlabel("Category")
plt.ylabel("Return Rate(%)")
plt.xticks(rotation=45)
plt.show()

#Country Based Return Rate
orders_customers= orders.merge(
    customers[["customer_id", "country"]],
    on="customer_id",
    how="left"
)


'''print(orders_customers.isnull().sum())'''

orders_customers["is_returned"] = (
    orders_customers["status"] == "Returned"
).astype(int)
country_return_rate = (
    orders_customers
    .groupby("country")["is_returned"]
    .mean().reset_index()
)
country_return_rate["return_rate_pct"]=country_return_rate["is_returned"] * 100
print(country_return_rate.head(10))
country_return_rate=country_return_rate.sort_values(
    "return_rate_pct", ascending=False
)
plt.figure(figsize=(10,5))
plt.bar(country_return_rate["country"], country_return_rate["return_rate_pct"])
plt.title("Return Rate by Coutnry (%)")
plt.xlabel("Country")
plt.ylabel("Return Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Return Rate by Channel (%)
channel_return_rate=(
    orders_customers.groupby("channel")["is_returned"]
    .mean().reset_index()
)
channel_return_rate["return_rate_pct"]=channel_return_rate["is_returned"] * 100
print(channel_return_rate)
channel_return_rate=channel_return_rate.sort_values(
    "return_rate_pct", ascending=False
)
plt.figure(figsize=(8,5))
plt.bar(channel_return_rate["channel"], channel_return_rate["return_rate_pct"])
plt.title("Return Rate by Channel (%)")
plt.xlabel("Channel")
plt.ylabel("Return Rate (%)")
plt.tight_layout()
plt.show()

#Returned Revenue by Channel
#It differs from net_revenue. This is potential loss.
orders["returned_revenue"] = np.where(
    orders["status"] == "Returned",
    orders["revenue"],
    0
)

returned_revenue_channel=(
    orders.groupby("channel")["returned_revenue"]
    .sum().reset_index()
    .sort_values("returned_revenue", ascending=False)
)
print(returned_revenue_channel)

plt.figure(figsize=(8,5))
plt.bar(returned_revenue_channel["channel"],
        returned_revenue_channel["returned_revenue"])
plt.title("Returned Revenue by Channel")
plt.xlabel("Channel")
plt.ylabel("Returned Revenue ($)")
plt.tight_layout()
plt.show()

#Revenue impact ratio
# What percentage of the channels total revenue goes to returns?
channel_revenue_summary= (
    orders.groupby("channel")
    .agg(
        total_revenue=("revenue", "sum"),
        returned_revenue=("returned_revenue", "sum")
    ).reset_index()
)
channel_revenue_summary["returned_revenue_ratio_pct"]=(
    channel_revenue_summary["returned_revenue"] /
    channel_revenue_summary["total_revenue"]
) * 100
print(channel_revenue_summary)

#Product Based Return Analysis
product_orders = (
    orders[["order_id", "status"]]
    .merge(order_details, on="order_id", how="left")
)
print(product_orders.head(10))
print(product_orders.shape)

product_return = (
    product_orders.groupby("product_id")
    .agg(
        total_orders=("order_id", "nunique"),
        returned_orders=("status", lambda x: (x == "Returned").sum()),
        returned_revenue=("line_revenue", lambda x: x[product_orders.loc[x.index, "status"]== "Returned"].sum())
    ).reset_index()

)
product_return["return_rate_pct"]=(
    product_return["returned_orders"] / product_return["total_orders"] * 100
)
print(product_return.sort_values("return_rate_pct", ascending=False).head(10))
print(product_return.describe())

#How Much Does These Products Cost Us?
#Returned Margin Impact
product_margin_loss = (
    product_orders[product_orders["status"]=="Returned"]
    .groupby("product_id")
    .agg(
        returned_revenue=("line_revenue", "sum"),
        returned_margin=("line_margin", "sum"),
        returned_items=("quantity","sum")
    ).reset_index()
)
product_risk=product_return.merge(
    product_margin_loss,
    on="product_id",
    how="left"
).fillna(0)
print(product_risk.sort_values("returned_margin", ascending=False).head(10))

#Customer Behavior
#Who is returning the products
returned_customers=(
    df[df["status"]=="Returned"]
    .groupby("customer_id").agg(
        returned_orders=("order_id", "nunique"),
        returned_margin=("line_margin", "sum"),
        returned_revenue=("line_revenue", "sum")
    ).reset_index()
)
print(returned_customers.describe())

#Customer Level Profile
customer_profile=(
    orders.groupby("customer_id").agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("net_revenue", "sum"),
        total_margin=("net_margin", "sum"),
        returned_orders=("status", lambda x: (x == "Returned").sum())
    ).reset_index()
)
customer_profile["return_flag"]=customer_profile["returned_orders"] >0
print(customer_profile.describe())

#Business Driven Segments
customer_profile["value_segment"] = np.where(
    customer_profile["total_revenue"] >= customer_profile["total_revenue"].median(),
    "High Value",
    "Low Value"
)

customer_profile["return_segment"] = np.where(
    customer_profile["returned_orders"] > 0,
    "Returned",
    "No Return"
)

customer_profile["final_segment"] = (
    customer_profile["value_segment"] + " - " + customer_profile["return_segment"]
)

customer_profile["final_segment"].value_counts(normalize=True) * 100
print(customer_profile["final_segment"].describe())

#Segment Based Revenue and Margin Contribution
segment_summary = (
    customer_profile
    .groupby("final_segment")
    .agg(
        customers=("customer_id", "count"),
        total_revenue=("total_revenue", "sum"),
        total_margin=("total_margin", "sum"),
        avg_revenue=("total_revenue", "mean"),
        avg_margin=("total_margin", "mean")
    )
    .sort_values("total_revenue", ascending=False)
)

print(segment_summary)

return_impact = (
    customer_profile
    .groupby("final_segment")
    .agg(
        returned_orders=("returned_orders", "sum"),
        customers=("customer_id", "count")
    )
)

return_impact["avg_returns_per_customer"] = (
    return_impact["returned_orders"] / return_impact["customers"]
)

print(return_impact)

plt.figure(figsize=(10,5))
plt.bar(
    segment_summary.index,
    segment_summary["total_revenue"]
)
plt.title("Total Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))
plt.bar(
    segment_summary.index,
    segment_summary["total_margin"]
)
plt.title("Total Margin by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Margin")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10,5))
plt.bar(
    segment_summary.index,
    segment_summary["avg_revenue"]
)
plt.title("Average Revenue per Customer by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Avg Revenue per Customer")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10,5))
plt.bar(
    segment_summary.index,
    segment_summary["avg_margin"]
)
plt.title("Average Margin per Customer by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Avg Margin per Customer")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


plt.figure(figsize=(8,5))
plt.bar(
    return_impact.index,
    return_impact["avg_returns_per_customer"]
)
plt.title("Average Returned Orders per Customer")
plt.xlabel("Customer Segment")
plt.ylabel("Avg Returned Orders")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
