# ============================================================
# NovaTech Customer Subscription Generator v2.0
# Module 1 - Configuration & Business Rules
# ============================================================

import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

random.seed(42)
Faker.seed(42)

# ============================================================
# FILE PATH
# ============================================================

EXCEL_FILE = r"C:\Users\FCI\Desktop\Customer Experience & Service Operations Intelligence\04_Python\03_Datasets\NovaTech_Customer_Experience_Dataset.xlsx"

# ============================================================
# LOAD MASTER TABLES
# ============================================================

print("=" * 70)
print("Loading Master Tables...")
print("=" * 70)

customers_df = pd.read_excel(EXCEL_FILE, sheet_name="Customers")
products_df = pd.read_excel(EXCEL_FILE, sheet_name="Products")

print("✓ Customers Loaded :", len(customers_df))
print("✓ Products Loaded  :", len(products_df))

# ============================================================
# BASIC VALIDATION
# ============================================================

required_customer_columns = [
    "Customer_ID",
    "Customer_Type"
]

required_product_columns = [
    "Product_ID",
    "Product_Name"
]

for col in required_customer_columns:
    if col not in customers_df.columns:
        raise Exception(f"Missing column in Customers sheet : {col}")

for col in required_product_columns:
    if col not in products_df.columns:
        raise Exception(f"Missing column in Products sheet : {col}")

print("✓ Master Tables Validated")

# ============================================================
# PRODUCT POPULARITY
# (Must total 100)
# ============================================================

product_weights = {
    "P001":18,     # Nova CRM
    "P002":12,     # Nova Analytics
    "P003":9,      # Nova HR
    "P004":15,     # Nova Cloud
    "P005":13,     # Nova AI
    "P006":10,     # Nova ServiceDesk
    "P007":8,      # Nova Finance
    "P008":5,      # Nova Payroll
    "P009":4,      # Nova Marketing
    "P010":3,      # Nova Projects
    "P011":2,      # Nova Security
    "P012":1       # Nova Insights
}

product_ids = list(product_weights.keys())
product_probability = list(product_weights.values())

# ============================================================
# SUBSCRIPTION COUNT RULES
# ============================================================

subscription_rules = {

    "Enterprise": {
        "choices":[2,3,4],
        "weights":[30,50,20]
    },

    "SMB":{
        "choices":[1,2,3],
        "weights":[40,40,20]
    },

    "Startup":{
        "choices":[1,2],
        "weights":[70,30]
    },

    "Individual":{
        "choices":[1],
        "weights":[100]
    }

}

# ============================================================
# PLAN RULES
# ============================================================

plan_rules = {

    "Enterprise":{

        "plans":["Enterprise","Professional"],

        "weights":[80,20]

    },

    "SMB":{

        "plans":["Professional","Enterprise"],

        "weights":[70,30]

    },

    "Startup":{

        "plans":["Professional","Basic"],

        "weights":[60,40]

    },

    "Individual":{

        "plans":["Basic","Professional"],

        "weights":[90,10]

    }

}

# ============================================================
# MONTHLY RECURRING REVENUE
# ============================================================

plan_price = {

    "Basic":999,

    "Professional":2499,

    "Enterprise":4999

}

# ============================================================
# SUBSCRIPTION STATUS
# ============================================================

status_choices = [

    "Active",

    "Expired",

    "Cancelled"

]

status_weights = [

    88,

    8,

    4

]

# ============================================================
# AUTO RENEWAL
# ============================================================

def get_auto_renewal(status):

    if status == "Active":

        return random.choices(

            ["Yes","No"],

            weights=[85,15],

            k=1

        )[0]

    return "No"

# ============================================================
# DATE GENERATOR
# ============================================================

def generate_subscription_dates():

    start_date = fake.date_between(

        start_date="-5y",

        end_date="today"

    )

    end_date = start_date + timedelta(days=365)

    return start_date,end_date

# ============================================================
# STORAGE
# ============================================================

subscriptions=[]

subscription_counter=1

print("\n✓ Business Rules Loaded")
print("=" * 70)
print(f"Customers : {len(customers_df)}")
print(f"Products  : {len(products_df)}")
print("=" * 70)
# ============================================================
# MODULE 2
# Subscription Generation Engine
# ============================================================

print("\nGenerating Customer Subscriptions...")
print("=" * 70)

for _, customer in customers_df.iterrows():

    customer_id = customer["Customer_ID"]
    customer_type = customer["Customer_Type"]

    # ---------------------------------------------
    # Number of subscriptions based on customer type
    # ---------------------------------------------

    rule = subscription_rules[customer_type]

    subscription_count = random.choices(
        rule["choices"],
        weights=rule["weights"],
        k=1
    )[0]

    # ---------------------------------------------
    # Prevent duplicate products for same customer
    # ---------------------------------------------

    assigned_products = set()

    while len(assigned_products) < subscription_count:

        product_id = random.choices(
            product_ids,
            weights=product_probability,
            k=1
        )[0]

        if product_id in assigned_products:
            continue

        assigned_products.add(product_id)

    # ---------------------------------------------
    # Create subscriptions
    # ---------------------------------------------

    for product_id in assigned_products:

        # -----------------------------
        # Subscription ID
        # -----------------------------

        subscription_id = f"S{subscription_counter:06d}"

        # -----------------------------
        # Plan based on customer type
        # -----------------------------

        plan_rule = plan_rules[customer_type]

        subscription_plan = random.choices(
            plan_rule["plans"],
            weights=plan_rule["weights"],
            k=1
        )[0]

        # -----------------------------
        # Revenue
        # -----------------------------

        monthly_revenue = plan_price[subscription_plan]

        # -----------------------------
        # Dates
        # -----------------------------

        start_date, end_date = generate_subscription_dates()

        # -----------------------------
        # Status
        # -----------------------------

        subscription_status = random.choices(
            status_choices,
            weights=status_weights,
            k=1
        )[0]

        # -----------------------------
        # Auto Renewal
        # -----------------------------

        auto_renewal = get_auto_renewal(subscription_status)

        # -----------------------------
        # Store record
        # -----------------------------

        subscriptions.append({

            "Subscription_ID": subscription_id,

            "Customer_ID": customer_id,

            "Product_ID": product_id,

            "Subscription_Plan": subscription_plan,

            "Subscription_Start_Date": start_date,

            "Subscription_End_Date": end_date,

            "Subscription_Status": subscription_status,

            "Monthly_Recurring_Revenue": monthly_revenue,

            "Auto_Renewal": auto_renewal

        })

        subscription_counter += 1

print("✓ Customer Subscription Records Generated")
print(f"Total Records : {len(subscriptions)}")
print("=" * 70)
# ============================================================
# MODULE 3
# Validation • Export • Summary Report
# ============================================================

print("\nCreating Customer Subscription DataFrame...")

subscriptions_df = pd.DataFrame(subscriptions)

print("✓ DataFrame Created Successfully")

# ============================================================
# DATA QUALITY CHECKS
# ============================================================

print("\n" + "="*70)
print("Running Data Quality Checks...")
print("="*70)

print(f"Total Subscription Records : {len(subscriptions_df)}")

print(f"Duplicate Subscription IDs : {subscriptions_df['Subscription_ID'].duplicated().sum()}")

duplicate_pairs = subscriptions_df.duplicated(
    subset=["Customer_ID","Product_ID"]
).sum()

print(f"Duplicate Customer-Product Records : {duplicate_pairs}")

print("\nMissing Values")

print(subscriptions_df.isnull().sum())

# ============================================================
# CUSTOMER COVERAGE
# ============================================================

customers_used = subscriptions_df["Customer_ID"].nunique()

print("\nCustomer Coverage")

print(f"Customers Used : {customers_used} / {len(customers_df)}")

# ============================================================
# PRODUCT COVERAGE
# ============================================================

products_used = subscriptions_df["Product_ID"].nunique()

print("\nProduct Coverage")

print(f"Products Used : {products_used} / {len(products_df)}")

print("\nProduct Distribution")

print(
    subscriptions_df["Product_ID"]
    .value_counts()
    .sort_index()
)

# ============================================================
# PLAN DISTRIBUTION
# ============================================================

print("\nSubscription Plan Distribution (%)")

print(

    round(

        subscriptions_df["Subscription_Plan"]

        .value_counts(normalize=True)

        *100,

        2

    )

)

# ============================================================
# STATUS DISTRIBUTION
# ============================================================

print("\nSubscription Status Distribution (%)")

print(

    round(

        subscriptions_df["Subscription_Status"]

        .value_counts(normalize=True)

        *100,

        2

    )

)

# ============================================================
# REVENUE SUMMARY
# ============================================================

print("\nRevenue Summary")

print(

    subscriptions_df

    .groupby("Subscription_Plan")["Monthly_Recurring_Revenue"]

    .agg(["count","sum","mean"])

)

print("\nTotal Monthly Recurring Revenue")

print(f"₹ {subscriptions_df['Monthly_Recurring_Revenue'].sum():,.0f}")

# ============================================================
# EXPORT TO EXCEL
# ============================================================

print("\nExporting Customer_Subscriptions Sheet...")

with pd.ExcelWriter(
    EXCEL_FILE,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    subscriptions_df.to_excel(
        writer,
        sheet_name="Customer_Subscriptions",
        index=False
    )

print("✓ Customer_Subscriptions Sheet Updated Successfully")

# ============================================================
# FINAL REPORT
# ============================================================

print("\n")
print("="*70)
print("NovaTech Customer Subscription Generator Report")
print("="*70)

print(f"Customers                : {len(customers_df)}")
print(f"Products                 : {len(products_df)}")
print(f"Subscriptions Generated  : {len(subscriptions_df)}")
print(f"Unique Products Used     : {products_used}")
print(f"Unique Customers Used    : {customers_used}")

print(f"\nTotal Monthly Revenue    : ₹ {subscriptions_df['Monthly_Recurring_Revenue'].sum():,.0f}")

print(f"Average Revenue/Subscription : ₹ {subscriptions_df['Monthly_Recurring_Revenue'].mean():,.2f}")

print("="*70)
print("CUSTOMER SUBSCRIPTION GENERATOR COMPLETED SUCCESSFULLY")
print("="*70)
# ============================================================
# MODULE 4
# BUSINESS VALIDATION REPORT
# ============================================================

print("\n")
print("=" * 75)
print("NovaTech Customer Subscription Business Validation Report")
print("=" * 75)

# ------------------------------------------------------------
# Average Products per Customer
# ------------------------------------------------------------

avg_products = (
    subscriptions_df.groupby("Customer_ID")
    .size()
    .mean()
)

print(f"\nAverage Products per Customer : {avg_products:.2f}")

# ------------------------------------------------------------
# Customer Type Distribution
# ------------------------------------------------------------

print("\nCustomer Type Distribution")

customer_type_summary = (
    customers_df["Customer_Type"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(customer_type_summary)

# ------------------------------------------------------------
# Average Subscriptions by Customer Type
# ------------------------------------------------------------

customer_subscription_summary = (
    subscriptions_df
    .merge(
        customers_df[
            ["Customer_ID","Customer_Type"]
        ],
        on="Customer_ID"
    )
)

avg_subscription = (

    customer_subscription_summary

    .groupby("Customer_Type")

    .size()

    /

    customers_df.groupby("Customer_Type").size()

).round(2)

print("\nAverage Subscriptions by Customer Type")

print(avg_subscription)

# ------------------------------------------------------------
# Product Popularity
# ------------------------------------------------------------

print("\nTop Products")

top_products = (

    subscriptions_df

    .merge(

        products_df[
            ["Product_ID","Product_Name"]
        ],

        on="Product_ID"

    )

    .groupby("Product_Name")

    .size()

    .sort_values(ascending=False)

)

print(top_products)

# ------------------------------------------------------------
# Revenue by Product
# ------------------------------------------------------------

print("\nMonthly Revenue by Product")

product_revenue = (

    subscriptions_df

    .merge(

        products_df[
            ["Product_ID","Product_Name"]
        ],

        on="Product_ID"

    )

    .groupby("Product_Name")["Monthly_Recurring_Revenue"]

    .sum()

    .sort_values(ascending=False)

)

print(product_revenue)

# ------------------------------------------------------------
# Auto Renewal
# ------------------------------------------------------------

print("\nAuto Renewal")

print(

    subscriptions_df["Auto_Renewal"]

    .value_counts(normalize=True)

    .mul(100)

    .round(2)

)

# ------------------------------------------------------------
# Active Subscription Rate
# ------------------------------------------------------------

active_rate = (

    subscriptions_df["Subscription_Status"]

    .eq("Active")

    .mean()

    *100

)

print(f"\nActive Subscription Rate : {active_rate:.2f}%")

# ------------------------------------------------------------
# Final Business Checks
# ------------------------------------------------------------

print("\nBusiness Validation")

print(f"✓ Customers                  : {len(customers_df)}")

print(f"✓ Products                   : {len(products_df)}")

print(f"✓ Subscriptions              : {len(subscriptions_df)}")

print(f"✓ Products Used              : {subscriptions_df['Product_ID'].nunique()}")

print(f"✓ Customers Covered          : {subscriptions_df['Customer_ID'].nunique()}")

print(f"✓ Duplicate Customer/Product : {duplicate_pairs}")

print(f"✓ Total MRR                  : ₹{subscriptions_df['Monthly_Recurring_Revenue'].sum():,.0f}")

print("\n")

print("=" * 75)

print("CUSTOMER SUBSCRIPTION DATASET VERIFIED SUCCESSFULLY")

print("=" * 75)