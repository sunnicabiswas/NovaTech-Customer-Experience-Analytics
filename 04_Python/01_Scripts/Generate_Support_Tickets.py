# ==========================================================
# NOVATECH SUPPORT TICKET GENERATOR v2.0
# Customer Experience & Service Operations Intelligence
# ==========================================================

# ==========================================================
# MODULE 1
# IMPORTS & CONFIGURATION
# ==========================================================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

# ==========================================================
# RANDOM SEED
# ==========================================================

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

fake = Faker()

# ==========================================================
# DATASET CONFIGURATION
# ==========================================================

TOTAL_TICKETS = 5000

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)

# ==========================================================
# EXCEL FILE LOCATION
# ==========================================================

EXCEL_FILE = r"C:\Users\FCI\Desktop\Customer Experience & Service Operations Intelligence\04_Python\03_Datasets\NovaTech_Customer_Experience_Dataset.xlsx"

# ==========================================================
# OUTPUT SHEETS
# ==========================================================

SUPPORT_TICKET_SHEET = "tbl_Support_Tickets"
INTERACTION_SHEET = "tbl_Interaction_History"

# ==========================================================
# CUSTOMER TYPE DISTRIBUTION
# ==========================================================

CUSTOMER_TYPE_WEIGHTS = {
    "Enterprise": 20,
    "SMB": 45,
    "Startup": 25,
    "Individual": 10
}

# ==========================================================
# PRODUCT POPULARITY
# ==========================================================

PRODUCT_POPULARITY = {

    "P001":18,   # Nova CRM
    "P002":12,   # Nova Analytics
    "P003":10,   # Nova HR
    "P004":15,   # Nova Cloud
    "P005":13,   # Nova AI
    "P006":10,   # Nova Service Desk
    "P007":8,    # Nova Finance
    "P008":6,    # Nova Payroll
    "P009":5,    # Nova Marketing
    "P010":5,    # Nova Projects
    "P011":5,    # Nova Security
    "P012":3     # Nova Insights

}

# ==========================================================
# PRIORITY DISTRIBUTION
# ==========================================================

PRIORITY_WEIGHTS = {

    "Critical":8,
    "High":22,
    "Medium":45,
    "Low":25

}

# ==========================================================
# TICKET STATUS DISTRIBUTION
# ==========================================================

TICKET_STATUS_WEIGHTS = {

    "Resolved":68,
    "Closed":15,
    "Open":10,
    "Pending":5,
    "Escalated":2

}

# ==========================================================
# ISSUE CATEGORY DISTRIBUTION
# ==========================================================

ISSUE_WEIGHTS = {

    "Login & Authentication":18,
    "Performance Issue":16,
    "Technical Issue":15,
    "Billing & Subscription":12,
    "Feature Request":10,
    "Integration Issue":9,
    "Security & Compliance":8,
    "Data Sync Issue":6,
    "General Inquiry":3,
    "Account Management":3

}

# ==========================================================
# ISSUE COMPLEXITY
# ==========================================================

ISSUE_COMPLEXITY = {

    "Login & Authentication":"Simple",
    "Billing & Subscription":"Simple",
    "General Inquiry":"Simple",
    "Account Management":"Simple",

    "Feature Request":"Medium",
    "Performance Issue":"Medium",

    "Technical Issue":"Complex",
    "Integration Issue":"Complex",
    "Security & Compliance":"Complex",
    "Data Sync Issue":"Complex"

}

# ==========================================================
# ISSUE SEVERITY
# ==========================================================

ISSUE_SEVERITY = {

    "Login & Authentication":"Low",
    "Billing & Subscription":"Medium",
    "General Inquiry":"Low",
    "Account Management":"Medium",

    "Feature Request":"Medium",

    "Performance Issue":"High",
    "Technical Issue":"High",
    "Integration Issue":"High",
    "Data Sync Issue":"High",

    "Security & Compliance":"Critical"

}

# ==========================================================
# COMMUNICATION CHANNELS
# ==========================================================

CHANNEL_WEIGHTS = {

    "Email":35,
    "Chat":30,
    "Phone":25,
    "Portal":10

}

# ==========================================================
# INTERACTION DIRECTION
# ==========================================================

DIRECTION_WEIGHTS = {

    "Inbound":55,
    "Outbound":45

}

# ==========================================================
# AGENT PERFORMANCE TIERS
# ==========================================================

AGENT_TIERS = {

    "Top Performer":20,
    "Average":60,
    "Needs Improvement":20

}

# ==========================================================
# BUSINESS RULES
# ==========================================================

RESPONSE_TIME_RULES = {

    "Critical":(0.25,1),
    "High":(1,4),
    "Medium":(4,12),
    "Low":(8,24)

}

RESOLUTION_TIME_RULES = {

    "Critical":(4,12),
    "High":(12,30),
    "Medium":(24,72),
    "Low":(48,120)

}

# ==========================================================
# INTERACTION RULES
# ==========================================================

INTERACTION_RULES = {

    "Simple":(1,2),
    "Medium":(2,4),
    "Complex":(5,8)

}

# ==========================================================
# PRINT CONFIGURATION
# ==========================================================

print("=" * 70)
print("NovaTech Support Ticket Generator v2.0")
print("=" * 70)

print(f"Total Tickets : {TOTAL_TICKETS}")
print(f"Date Range    : {START_DATE.date()} to {END_DATE.date()}")

print("=" * 70)
# ==========================================================
# MODULE 2
# LOAD MASTER DATA & LOOKUP DICTIONARIES
# ==========================================================

print("\nLoading Master Tables...")

# ----------------------------------------------------------
# Read Master Sheets
# ----------------------------------------------------------

customers_df = pd.read_excel(EXCEL_FILE, sheet_name="Customers")

products_df = pd.read_excel(EXCEL_FILE, sheet_name="Products")

subscriptions_df = pd.read_excel(EXCEL_FILE, sheet_name="Customer_Subscriptions")

agents_df = pd.read_excel(EXCEL_FILE, sheet_name="Support_Agents")

regions_df = pd.read_excel(EXCEL_FILE, sheet_name="Regions")

departments_df = pd.read_excel(EXCEL_FILE, sheet_name="Departments")

priority_df = pd.read_excel(EXCEL_FILE, sheet_name="Priority_Levels")

sla_df = pd.read_excel(EXCEL_FILE, sheet_name="SLA_Rules")

issue_df = pd.read_excel(EXCEL_FILE, sheet_name="Issue_Categories")

print("✓ Master Tables Loaded Successfully")
print("\n========== COLUMN NAMES ==========")

print("\nCustomers")
print(customers_df.columns.tolist())

print("\nProducts")
print(products_df.columns.tolist())

print("\nSupport Agents")
print(agents_df.columns.tolist())

print("\nCustomer Subscriptions")
print(subscriptions_df.columns.tolist())

print("\nPriority Levels")
print(priority_df.columns.tolist())

print("\nSLA Rules")
print(sla_df.columns.tolist())

print("\nIssue Categories")
print(issue_df.columns.tolist())

print("\n==================================")

# ==========================================================
# VALIDATE MASTER TABLES
# ==========================================================

assert len(customers_df) > 0, "Customers table is empty."

assert len(products_df) == 12, "Products table must contain 12 products."

assert len(agents_df) == 25, "Support Agents table must contain 25 agents."

print("✓ Master Table Validation Successful")

# ==========================================================
# MERGE SLA WITH PRIORITY TABLE
# ==========================================================

sla_df = sla_df.merge(

    priority_df[["Priority_ID","Priority_Level"]],

    on="Priority_ID",

    how="left"

)

print("✓ SLA Rules Linked Successfully")

# ==========================================================
# CUSTOMER LOOKUP
# ==========================================================

customer_lookup = customers_df.set_index("Customer_ID").to_dict("index")

customer_ids = customers_df["Customer_ID"].tolist()

# ==========================================================
# PRODUCT LOOKUP
# ==========================================================

product_lookup = products_df.set_index("Product_ID").to_dict("index")

product_ids = products_df["Product_ID"].tolist()

product_weights = [PRODUCT_POPULARITY[p] for p in product_ids]

# ==========================================================
# CUSTOMER SUBSCRIPTION LOOKUP
# ==========================================================

subscription_lookup = {}

for _, row in subscriptions_df.iterrows():

    customer_id = row["Customer_ID"]

    product_id = row["Product_ID"]

    if customer_id not in subscription_lookup:

        subscription_lookup[customer_id] = []

    subscription_lookup[customer_id].append(product_id)

print(f"✓ Subscription Lookup Created ({len(subscription_lookup)} customers)")
print("\nProducts in Customer Subscription Table")

print(
    subscriptions_df["Product_ID"]
    .value_counts()
    .sort_index()
)

# ==========================================================
# REGION LOOKUP
# ==========================================================

region_lookup = regions_df.set_index("Region_ID").to_dict("index")

# ==========================================================
# DEPARTMENT LOOKUP
# ==========================================================

department_lookup = departments_df.set_index("Department_ID").to_dict("index")

# ==========================================================
# ISSUE LOOKUP
# ==========================================================

issue_lookup = issue_df.set_index("Issue_Category").to_dict("index")

issue_categories = list(ISSUE_WEIGHTS.keys())

issue_weights = list(ISSUE_WEIGHTS.values())

# ==========================================================
# PRIORITY LOOKUP
# ==========================================================

priority_lookup = priority_df.set_index("Priority_Level").to_dict("index")

priority_levels = list(PRIORITY_WEIGHTS.keys())

priority_weights = list(PRIORITY_WEIGHTS.values())

# ==========================================================
# SLA LOOKUP
# ==========================================================

sla_lookup = sla_df.set_index("Priority_Level").to_dict("index")

# ==========================================================
# TICKET STATUS
# ==========================================================

ticket_statuses = list(TICKET_STATUS_WEIGHTS.keys())

ticket_status_weights = list(TICKET_STATUS_WEIGHTS.values())

# ==========================================================
# AGENT PERFORMANCE TIERS
# ==========================================================

agents_df = agents_df.sort_values(
    by="Experience_Years",
    ascending=False
).reset_index(drop=True)

total_agents = len(agents_df)

top_count = int(total_agents * 0.20)

weak_count = int(total_agents * 0.20)

average_count = total_agents - top_count - weak_count

agents_df.loc[0:top_count-1, "Performance_Tier"] = "Top Performer"

agents_df.loc[top_count:top_count+average_count-1, "Performance_Tier"] = "Average"

agents_df.loc[top_count+average_count:, "Performance_Tier"] = "Needs Improvement"

print("✓ Agent Performance Tiers Assigned")

# ==========================================================
# AGENT PROFILE LOOKUP
# ==========================================================

agent_profiles = {}

for _, row in agents_df.iterrows():

    tier = row["Performance_Tier"]

    if tier == "Top Performer":

        profile = {

            "Response_Factor":0.70,
            "Resolution_Factor":0.75,
            "FCR_Rate":0.92,
            "CSAT_Bonus":0.40

        }

    elif tier == "Average":

        profile = {

            "Response_Factor":1.00,
            "Resolution_Factor":1.00,
            "FCR_Rate":0.78,
            "CSAT_Bonus":0.10

        }

    else:

        profile = {

            "Response_Factor":1.35,
            "Resolution_Factor":1.30,
            "FCR_Rate":0.60,
            "CSAT_Bonus":-0.35

        }

    agent_profiles[row["Agent_ID"]] = profile

agent_ids = agents_df["Agent_ID"].tolist()

# ==========================================================
# SUMMARY
# ==========================================================

print("\nMaster Data Ready")

print("="*70)

print(f"Customers          : {len(customer_ids)}")

print(f"Products           : {len(product_ids)}")

print(f"Support Agents     : {len(agent_ids)}")

print(f"Issue Categories   : {len(issue_categories)}")

print(f"Subscriptions       : {len(subscription_lookup)}")

print("="*70)
# ==========================================================
# MODULE 3A
# BUSINESS RULE ENGINE
# ==========================================================

print("\nInitializing Business Rules...")

# ----------------------------------------------------------
# Weighted Random Selection
# ----------------------------------------------------------

def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]


# ----------------------------------------------------------
# Generate Ticket ID
# ----------------------------------------------------------

def generate_ticket_id(ticket_number):
    return f"TKT{ticket_number:05d}"


# ----------------------------------------------------------
# Random Date Generator
# ----------------------------------------------------------

def random_date(start_date, end_date):

    total_days = (end_date - start_date).days

    random_days = random.randint(0, total_days)

    return start_date + timedelta(days=random_days)


# ----------------------------------------------------------
# Select Product for Customer
# ----------------------------------------------------------

def get_customer_product(customer_id):

    subscribed_products = subscription_lookup.get(customer_id, [])

    if subscribed_products:

        available_products = []
        available_weights = []

        for product in subscribed_products:

            available_products.append(product)
            available_weights.append(PRODUCT_POPULARITY[product])

        return weighted_choice(
            available_products,
            available_weights
        )

    return weighted_choice(
        product_ids,
        product_weights
    )


# ----------------------------------------------------------
# Select Issue Category
# ----------------------------------------------------------

def get_issue_category():

    return weighted_choice(
        issue_categories,
        issue_weights
    )


# ----------------------------------------------------------
# Select Priority
# ----------------------------------------------------------

def get_priority():

    return weighted_choice(
        priority_levels,
        priority_weights
    )


# ----------------------------------------------------------
# Select Ticket Status
# ----------------------------------------------------------

def get_ticket_status():

    return weighted_choice(
        ticket_statuses,
        ticket_status_weights
    )


# ----------------------------------------------------------
# Get Issue Complexity
# ----------------------------------------------------------

def get_complexity(issue):

    return ISSUE_COMPLEXITY[issue]


# ----------------------------------------------------------
# Get Issue Severity
# ----------------------------------------------------------

def get_severity(issue):

    return ISSUE_SEVERITY[issue]


print("✓ Business Rule Engine Ready")
# ==========================================================
# MODULE 3B - PART 1
# SUPPORT TICKET GENERATION
# INITIALIZATION & CORE TICKET DETAILS
# ==========================================================

print("\nGenerating Support Tickets...")

ticket_records = []

ticket_counter = 1

for _ in range(TOTAL_TICKETS):

    # ======================================================
    # Ticket ID
    # ======================================================

    ticket_id = generate_ticket_id(ticket_counter)

    ticket_counter += 1

    # ======================================================
    # Customer Selection
    # ======================================================

    customer = customers_df.sample(1).iloc[0]

    customer_id = customer["Customer_ID"]

    # ======================================================
    # Customer Region
    # ======================================================

    customer_region = customer["Region_ID"]

    # ======================================================
    # Product Selection
    # (Subscribed Product Preferred)
    # ======================================================

    product_id = get_customer_product(customer_id)

    product = product_lookup[product_id]


    # ======================================================
    # Issue Category
    # ======================================================

    issue_category = get_issue_category()

    # ======================================================
    # Issue Complexity
    # ======================================================

    issue_complexity = get_complexity(issue_category)

    # ======================================================
    # Issue Severity
    # ======================================================

    issue_severity = get_severity(issue_category)

    # ======================================================
    # Priority
    # ======================================================

    priority = get_priority()

    priority_id = priority_lookup[priority]["Priority_ID"]

    # ======================================================
    # Assign Support Agent
    # Same Region Preferred
    # ======================================================

    available_agents = agents_df[
        agents_df["Region_ID"] == customer_region
    ]

    if len(available_agents) == 0:

        available_agents = agents_df

    agent = available_agents.sample(1).iloc[0]

    agent_id = agent["Agent_ID"]


    performance_tier = agent["Performance_Tier"]

    agent_profile = agent_profiles[agent_id]

    # ======================================================
    # Department
    # ======================================================

    department_id = agent["Department_ID"]

    # ======================================================
    # Ticket Creation Date
    # ======================================================

    created_date = random_date(
        START_DATE,
        END_DATE
    )

    # ======================================================
    # SLA Rule
    # ======================================================

    sla = sla_lookup[priority]

    response_sla = sla["Response_Time_Hours"]

    resolution_sla = sla["Resolution_Time_Hours"]

    # ======================================================
    # Ticket Type
    # (Used Later For Interactions)
    # ======================================================

    if issue_complexity == "Simple":

        ticket_type = "Simple"

    elif issue_complexity == "Medium":

        ticket_type = "Medium"

    else:

        ticket_type = "Complex"
         # ======================================================
    # RESPONSE TIME
    # ======================================================

    response_time = round(

        random.uniform(
           RESPONSE_TIME_RULES[priority][0],
           RESPONSE_TIME_RULES[priority][1]
        )

        * agent_profile["Response_Factor"],

        2

    )

    # ======================================================
    # RESOLUTION TIME
    # ======================================================

    resolution_time = round(

        random.uniform(
            RESOLUTION_TIME_RULES[priority][0],
            RESOLUTION_TIME_RULES[priority][1]
        )

        * agent_profile["Resolution_Factor"],

        2

    )

    # ======================================================
    # COMPLEXITY ADJUSTMENT
    # ======================================================

    if issue_complexity == "Medium":

        response_time *= 1.15
        resolution_time *= 1.25

    elif issue_complexity == "Complex":

        response_time *= 1.35
        resolution_time *= 1.55

    response_time = round(response_time,2)
    resolution_time = round(resolution_time,2)

    # ======================================================
    # SLA CALCULATION
    # ======================================================

    response_sla_met = response_time <= response_sla

    resolution_sla_met = resolution_time <= resolution_sla

    sla_met = "Yes" if (
        response_sla_met and resolution_sla_met
    ) else "No"

    # ======================================================
    # FIRST CONTACT RESOLUTION
    # ======================================================

    if random.random() <= agent_profile["FCR_Rate"]:

        first_contact_resolution = "Yes"

    else:

        first_contact_resolution = "No"

    # ======================================================
    # ESCALATION
    # ======================================================

    escalation_probability = 0.02

    if priority == "Critical":

        escalation_probability += 0.20

    elif priority == "High":

        escalation_probability += 0.10

    if issue_complexity == "Complex":

        escalation_probability += 0.10

    if sla_met == "No":

        escalation_probability += 0.25

    if first_contact_resolution == "No":

        escalation_probability += 0.08

    escalated = (

        "Yes"

        if random.random() < escalation_probability

        else "No"

    )

    # ======================================================
    # REOPENED
    # ======================================================

    reopen_probability = 0.04

    if escalated == "Yes":

        reopen_probability += 0.08

    if sla_met == "No":

        reopen_probability += 0.08

    if first_contact_resolution == "No":

        reopen_probability += 0.10

    reopened = (

        "Yes"

        if random.random() < reopen_probability

        else "No"

    )

    # ======================================================
    # CLOSED DATE
    # ======================================================

    closed_date = created_date + timedelta(

        hours=resolution_time

    )
     # ======================================================
    # CSAT CALCULATION
    # ======================================================

    csat_score = 5.0

    # Response Time Impact
    if response_time > response_sla:
        csat_score -= 0.50

    # Resolution Time Impact
    if resolution_time > resolution_sla:
        csat_score -= 0.70

    # Escalation Impact
    if escalated == "Yes":
        csat_score -= 0.60

    # Reopened Impact
    if reopened == "Yes":
        csat_score -= 0.70

    # FCR Bonus
    if first_contact_resolution == "Yes":
        csat_score += 0.20

    # Agent Performance Bonus
    csat_score += agent_profile["CSAT_Bonus"]

    # Small Natural Variation
    csat_score += random.uniform(-0.20, 0.20)

    # Keep within valid range
    csat_score = round(
        min(max(csat_score, 1.0), 5.0),
        1
    )

    # ======================================================
    # FINAL TICKET STATUS
    # ======================================================

    status_random = random.random()

    if status_random <= 0.68:

        ticket_status = "Resolved"

        escalated = "Yes" if random.random() < 0.08 else "No"

    elif status_random <= 0.83:

        ticket_status = "Closed"

        escalated = "Yes" if random.random() < 0.04 else "No"

    elif status_random <= 0.93:

        ticket_status = "Open"

        escalated = "No"

    elif status_random <= 0.98:

        ticket_status = "Pending"

        escalated = "No"

    else:

        ticket_status = "Escalated"

        escalated = "Yes"
    # -----------------------------------------------------
    # Closed Date Adjustment
    # -----------------------------------------------------

    if ticket_status in ["Open", "Pending", "Escalated"]:

        closed_date = pd.NaT

    # ======================================================
    # REOPEN COUNT
    # ======================================================

    if reopened == "Yes":

        reopen_count = random.randint(1, 3)

    else:

        reopen_count = 0

    # ======================================================
    # RESOLUTION SUMMARY
    # ======================================================

    resolution_summary = random.choice([
        "Issue resolved after troubleshooting.",
        "Configuration updated successfully.",
        "Patch deployed successfully.",
        "Customer guidance provided.",
        "Escalated to Engineering.",
        "Issue fixed after backend update.",
        "Root cause identified and resolved.",
        "Duplicate ticket merged.",
        "Bug confirmed and workaround shared.",
        "Resolved after system restart."
    ])

    # ======================================================
    # TICKET RECORD
    # ======================================================

    ticket_records.append({

        "Ticket_ID": ticket_id,

        "Customer_ID": customer_id,

        "Product_ID": product_id,

        "Agent_ID": agent_id,

        "Department_ID": department_id,

        "Priority_ID": priority_id,

        "Issue_Category": issue_category,

        "Issue_Complexity": issue_complexity,

        "Issue_Severity": issue_severity,

        "Ticket_Type": ticket_type,

        "Created_Date": created_date,

        "Closed_Date": closed_date,

        "Response_Time_Hours": response_time,

        "Resolution_Time_Hours": resolution_time,

        "Response_SLA_Hours": response_sla,

        "Resolution_SLA_Hours": resolution_sla,

        "SLA_Met": sla_met,

        "First_Contact_Resolution": first_contact_resolution,

        "Escalated": escalated,

        "Reopened": reopened,

        "Reopen_Count": reopen_count,

        "CSAT_Score": csat_score,

        "Ticket_Status": ticket_status,

        "Resolution_Summary": resolution_summary

    })
# ==========================================================
# MODULE 3B - PART 4A
# CREATE SUPPORT TICKETS DATAFRAME
# VALIDATION & DATA QUALITY CHECKS
# ==========================================================

print("\nCreating Support Tickets DataFrame...")

# ----------------------------------------------------------
# Create DataFrame
# ----------------------------------------------------------

support_tickets_df = pd.DataFrame(ticket_records)

print("✓ Support Tickets DataFrame Created")

# ----------------------------------------------------------
# Basic Validation
# ----------------------------------------------------------

print("\nRunning Data Quality Checks...")

# Total Records
print(f"Total Tickets              : {len(support_tickets_df)}")

# Duplicate Ticket IDs
duplicate_ticket_ids = support_tickets_df["Ticket_ID"].duplicated().sum()
print(f"Duplicate Ticket IDs       : {duplicate_ticket_ids}")

# Missing Values
print("\nMissing Values")

print(
    support_tickets_df.isnull().sum()
)

# ----------------------------------------------------------
# Foreign Key Validation
# ----------------------------------------------------------

invalid_customers = (
    ~support_tickets_df["Customer_ID"]
    .isin(customers_df["Customer_ID"])
).sum()

invalid_products = (
    ~support_tickets_df["Product_ID"]
    .isin(products_df["Product_ID"])
).sum()

invalid_agents = (
    ~support_tickets_df["Agent_ID"]
    .isin(agents_df["Agent_ID"])
).sum()

print("\nForeign Key Validation")

print(f"Invalid Customers          : {invalid_customers}")
print(f"Invalid Products           : {invalid_products}")
print(f"Invalid Agents             : {invalid_agents}")

# ----------------------------------------------------------
# Coverage Checks
# ----------------------------------------------------------

print("\nCoverage Summary")

print(
    f"Customers Used            : "
    f"{support_tickets_df['Customer_ID'].nunique()} / "
    f"{customers_df['Customer_ID'].nunique()}"
)

print(
    f"Products Used             : "
    f"{support_tickets_df['Product_ID'].nunique()} / "
    f"{products_df['Product_ID'].nunique()}"
)

print(
    f"Agents Used               : "
    f"{support_tickets_df['Agent_ID'].nunique()} / "
    f"{agents_df['Agent_ID'].nunique()}"
)

# ----------------------------------------------------------
# Distribution Checks
# ----------------------------------------------------------

print("\nPriority Distribution")

print(
    support_tickets_df["Priority_ID"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nIssue Category Distribution")

print(
    support_tickets_df["Issue_Category"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nProduct Distribution (Top 12)")

print(
    support_tickets_df["Product_ID"]
    .value_counts()
)

print("\nAverage Metrics")

print(
    support_tickets_df[
        [
            "Response_Time_Hours",
            "Resolution_Time_Hours",
            "CSAT_Score"
        ]
    ].mean().round(2)
)

print("\n✓ Module 3B - Part 4A Completed Successfully")
# ==========================================================
# MODULE 3B - PART 4B
# FINAL DATA QUALITY REPORT & EXPORT
# ==========================================================

print("\nGenerating Final Validation Report...")

# ----------------------------------------------------------
# Ticket Status Distribution
# ----------------------------------------------------------

print("\nTicket Status Distribution")

print(
    support_tickets_df["Ticket_Status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# ----------------------------------------------------------
# SLA Compliance
# ----------------------------------------------------------

sla_pct = (
    support_tickets_df["SLA_Met"]
    .eq("Yes")
    .mean()
    * 100
)

print(f"\nSLA Compliance : {sla_pct:.2f}%")

# ----------------------------------------------------------
# First Contact Resolution
# ----------------------------------------------------------

fcr_pct = (
    support_tickets_df["First_Contact_Resolution"]
    .eq("Yes")
    .mean()
    * 100
)

print(f"First Contact Resolution : {fcr_pct:.2f}%")

# ----------------------------------------------------------
# Escalation Rate
# ----------------------------------------------------------

esc_pct = (
    support_tickets_df["Escalated"]
    .eq("Yes")
    .mean()
    * 100
)

print(f"Escalation Rate : {esc_pct:.2f}%")

# ----------------------------------------------------------
# Reopened Rate
# ----------------------------------------------------------

reopen_pct = (
    support_tickets_df["Reopened"]
    .eq("Yes")
    .mean()
    * 100
)

print(f"Reopened Rate : {reopen_pct:.2f}%")

# ----------------------------------------------------------
# Average Metrics
# ----------------------------------------------------------

print("\nAverage KPIs")

print(f"Average Response Time   : {support_tickets_df['Response_Time_Hours'].mean():.2f} hrs")
print(f"Average Resolution Time : {support_tickets_df['Resolution_Time_Hours'].mean():.2f} hrs")
print(f"Average CSAT            : {support_tickets_df['CSAT_Score'].mean():.2f}")

# ----------------------------------------------------------
# Export Support Tickets to Master Dataset
# ----------------------------------------------------------

print("\nExporting Support_Tickets Sheet...")

with pd.ExcelWriter(
    EXCEL_FILE,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    support_tickets_df.to_excel(
        writer,
        sheet_name="Support_Tickets",
        index=False
    )

print("✓ Support_Tickets Sheet Updated Successfully")

# ----------------------------------------------------------
# FINAL REPORT
# ----------------------------------------------------------

print("\n" + "="*65)
print("NovaTech Support Ticket Generator Report")
print("="*65)

print(f"Tickets Generated        : {len(support_tickets_df)}")
print(f"Customers Used           : {support_tickets_df['Customer_ID'].nunique()}")
print(f"Products Used            : {support_tickets_df['Product_ID'].nunique()}")
print(f"Agents Used              : {support_tickets_df['Agent_ID'].nunique()}")

print(f"\nAverage Response Time    : {support_tickets_df['Response_Time_Hours'].mean():.2f} hrs")
print(f"Average Resolution Time  : {support_tickets_df['Resolution_Time_Hours'].mean():.2f} hrs")
print(f"Average CSAT             : {support_tickets_df['CSAT_Score'].mean():.2f}")

print(f"\nSLA Compliance           : {sla_pct:.2f}%")
print(f"FCR                      : {fcr_pct:.2f}%")
print(f"Escalation Rate          : {esc_pct:.2f}%")
print(f"Reopened Rate            : {reopen_pct:.2f}%")

print("="*65)
print("MODULE 3 COMPLETED SUCCESSFULLY")
print("="*65)
