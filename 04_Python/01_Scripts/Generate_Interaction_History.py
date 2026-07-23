# ==========================================================
# NOVATECH CUSTOMER INTERACTION GENERATOR v2.0
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
# EXCEL FILE LOCATION
# ==========================================================

EXCEL_FILE = r"C:\Users\FCI\Desktop\Customer Experience & Service Operations Intelligence\04_Python\03_Datasets\NovaTech_Customer_Experience_Dataset.xlsx"

# ==========================================================
# INPUT SHEETS
# ==========================================================

SUPPORT_TICKET_SHEET = "Support_Tickets"

CUSTOMER_SHEET = "Customers"

AGENT_SHEET = "Support_Agents"

# ==========================================================
# OUTPUT SHEET
# ==========================================================

INTERACTION_SHEET = "Interaction_History"

# ==========================================================
# DISPLAY HEADER
# ==========================================================

print("=" * 70)
print("NovaTech Customer Interaction Generator v2.0")
print("=" * 70)

print("\nLoading Master Tables...")
# ==========================================================
# LOAD MASTER TABLES
# ==========================================================

support_tickets_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name=SUPPORT_TICKET_SHEET
)

customers_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name=CUSTOMER_SHEET
)

agents_df = pd.read_excel(
    EXCEL_FILE,
    sheet_name=AGENT_SHEET
)
# ==========================================================
# VALIDATION
# ==========================================================

print(f"✓ Support Tickets Loaded : {len(support_tickets_df)}")
print(f"✓ Customers Loaded       : {len(customers_df)}")
print(f"✓ Agents Loaded          : {len(agents_df)}")

assert len(support_tickets_df) > 0
assert len(customers_df) > 0
assert len(agents_df) > 0

print("✓ Master Tables Validated")
# ==========================================================
# LOOKUP DICTIONARIES
# ==========================================================

customer_lookup = customers_df.set_index(
    "Customer_ID"
).to_dict("index")

agent_lookup = agents_df.set_index(
    "Agent_ID"
).to_dict("index")
print("\nMaster Data Ready")
print("=" * 70)

print(f"Support Tickets : {len(support_tickets_df)}")
print(f"Customers       : {len(customers_df)}")
print(f"Agents          : {len(agents_df)}")

print("=" * 70)
# ==========================================================
# MODULE 2
# BUSINESS RULES
# ==========================================================

print("\nInitializing Interaction Business Rules...")

# ----------------------------------------------------------
# Interactions by Issue Complexity
# ----------------------------------------------------------

INTERACTION_COUNT_RULES = {
    "Simple": (1, 2),
    "Medium": (2, 4),
    "Complex": (5, 8)
}

# ----------------------------------------------------------
# Communication Channels
# ----------------------------------------------------------

CHANNELS = [
    "Email",
    "Chat",
    "Phone",
    "Portal"
]

CHANNEL_WEIGHTS = [
    32,
    28,
    24,
    16
]

# ----------------------------------------------------------
# Interaction Direction
# ----------------------------------------------------------

DIRECTIONS = [
    "Inbound",
    "Outbound"
]

DIRECTION_WEIGHTS = [
    65,
    35
]

# ----------------------------------------------------------
# Interaction Types
# ----------------------------------------------------------

INTERACTION_TYPES = [
    "Customer Contact",
    "Agent Follow-up",
    "Issue Investigation",
    "Troubleshooting",
    "Status Update",
    "Escalation",
    "Resolution Confirmation"
]

INTERACTION_TYPE_WEIGHTS = [
    18,
    18,
    16,
    20,
    15,
    5,
    8
]

# ----------------------------------------------------------
# Interaction Status
# ----------------------------------------------------------

INTERACTION_STATUSES = [
    "Completed",
    "Pending",
    "Cancelled"
]

INTERACTION_STATUS_WEIGHTS = [
    93,
    5,
    2
]

# ----------------------------------------------------------
# Outcomes
# ----------------------------------------------------------

INTERACTION_OUTCOMES = [
    "Information Provided",
    "Awaiting Customer",
    "Issue Escalated",
    "Work In Progress",
    "Issue Resolved",
    "Follow-up Required"
]

OUTCOME_WEIGHTS = [
    20,
    12,
    8,
    30,
    20,
    10
]
# ==========================================================
# Duration Rules
# ==========================================================

CHANNEL_DURATION_RULES = {

    "Email": (5, 15),

    "Chat": (8, 25),

    "Phone": (10, 45),

    "Portal": (5, 20)

}
# ==========================================================
# Interaction Notes
# ==========================================================

INTERACTION_NOTES = [

    "Customer reported issue.",

    "Issue verified by support engineer.",

    "Requested additional information from customer.",

    "Provided troubleshooting instructions.",

    "Logs collected for investigation.",

    "Issue reproduced successfully.",

    "Escalated to engineering team.",

    "Follow-up call completed.",

    "Temporary workaround shared.",

    "Customer confirmed resolution.",

    "Monitoring issue after deployment.",

    "Waiting for customer confirmation."

]
# ==========================================================
# Helper Functions
# ==========================================================

def random_datetime(start_date, end_date):

    seconds = int((end_date - start_date).total_seconds())

    if seconds <= 0:
        return start_date

    return start_date + timedelta(
        seconds=random.randint(0, seconds)
    )


def random_duration(channel):

    low, high = CHANNEL_DURATION_RULES[channel]

    return random.randint(low, high)


def interaction_count(complexity):

    low, high = INTERACTION_COUNT_RULES[complexity]

    return random.randint(low, high)
print("✓ Interaction Business Rules Loaded")

print("=" * 70)

print("Channels           :", len(CHANNELS))
print("Interaction Types  :", len(INTERACTION_TYPES))
print("Possible Outcomes  :", len(INTERACTION_OUTCOMES))
print("Sample Notes       :", len(INTERACTION_NOTES))

print("=" * 70)
# ==========================================================
# MODULE 3
# GENERATE CUSTOMER INTERACTIONS
# ==========================================================

print("\nGenerating Customer Interactions...")
print("=" * 70)

interaction_records = []

interaction_counter = 1

current_datetime = datetime.now()
# ==========================================================
# LOOP THROUGH SUPPORT TICKETS
# ==========================================================

for _, ticket in support_tickets_df.iterrows():

    ticket_id = ticket["Ticket_ID"]
    customer_id = ticket["Customer_ID"]
    agent_id = ticket["Agent_ID"]

    issue_complexity = ticket["Issue_Complexity"]
    ticket_status = ticket["Ticket_Status"]

    created_date = pd.to_datetime(ticket["Created_Date"])

    closed_date = ticket["Closed_Date"]

    if pd.isna(closed_date):

        interaction_end = current_datetime

    else:

        interaction_end = pd.to_datetime(closed_date)

    total_interactions = interaction_count(issue_complexity)
        # ------------------------------------------------------
    # Create interaction records
    # ------------------------------------------------------

    for sequence in range(1, total_interactions + 1):

        interaction_id = f"INT{interaction_counter:07d}"

        channel = random.choices(
            CHANNELS,
            weights=CHANNEL_WEIGHTS,
            k=1
        )[0]

        direction = random.choices(
            DIRECTIONS,
            weights=DIRECTION_WEIGHTS,
            k=1
        )[0]

        interaction_type = random.choices(
            INTERACTION_TYPES,
            weights=INTERACTION_TYPE_WEIGHTS,
            k=1
        )[0]

        duration = random_duration(channel)

        interaction_datetime = random_datetime(
            created_date,
            interaction_end
        )
        # --------------------------------------------------
        # Last interaction should reflect ticket status
        # --------------------------------------------------

        if sequence == total_interactions:

            if ticket_status in ["Resolved", "Closed"]:

                interaction_status = "Completed"

                outcome = "Issue Resolved"

                interaction_type = "Resolution Confirmation"

            elif ticket_status == "Escalated":

                interaction_status = "Completed"

                outcome = "Issue Escalated"

                interaction_type = "Escalation"

            elif ticket_status == "Pending":

                interaction_status = "Pending"

                outcome = "Awaiting Customer"

            else:

                interaction_status = "Pending"

                outcome = "Work In Progress"

        else:

            interaction_status = random.choices(
                INTERACTION_STATUSES,
                weights=INTERACTION_STATUS_WEIGHTS,
                k=1
            )[0]

            outcome = random.choices(
                INTERACTION_OUTCOMES,
                weights=OUTCOME_WEIGHTS,
                k=1
            )[0]
        note = random.choice(INTERACTION_NOTES)

        interaction_records.append({

            "Interaction_ID": interaction_id,

            "Ticket_ID": ticket_id,

            "Customer_ID": customer_id,

            "Agent_ID": agent_id,

            "Interaction_Sequence": sequence,

            "Interaction_DateTime": interaction_datetime,

            "Channel": channel,

            "Direction": direction,

            "Interaction_Type": interaction_type,

            "Duration_Minutes": duration,

            "Interaction_Status": interaction_status,

            "Interaction_Outcome": outcome,

            "Interaction_Notes": note

        })

        interaction_counter += 1
# ==========================================================
# CREATE DATAFRAME
# ==========================================================

print("\nCreating Interaction DataFrame...")

interaction_df = pd.DataFrame(interaction_records)

print("✓ Customer Interaction DataFrame Created")

print(f"Total Interaction Records : {len(interaction_df)}")

print("=" * 70)
# ==========================================================
# MODULE 4
# VALIDATION & EXPORT
# ==========================================================

print("\nRunning Data Quality Checks...")
print("=" * 70)

# ----------------------------------------------------------
# Basic Validation
# ----------------------------------------------------------

print(f"Total Interaction Records : {len(interaction_df)}")
print(f"Duplicate Interaction IDs : {interaction_df['Interaction_ID'].duplicated().sum()}")

print("\nMissing Values")

print(interaction_df.isnull().sum())

# ----------------------------------------------------------
# Foreign Key Validation
# ----------------------------------------------------------

invalid_tickets = (
    ~interaction_df["Ticket_ID"].isin(
        support_tickets_df["Ticket_ID"]
    )
).sum()

invalid_customers = (
    ~interaction_df["Customer_ID"].isin(
        customers_df["Customer_ID"]
    )
).sum()

invalid_agents = (
    ~interaction_df["Agent_ID"].isin(
        agents_df["Agent_ID"]
    )
).sum()

print("\nForeign Key Validation")

print(f"Invalid Tickets    : {invalid_tickets}")
print(f"Invalid Customers  : {invalid_customers}")
print(f"Invalid Agents     : {invalid_agents}")

# ----------------------------------------------------------
# Coverage
# ----------------------------------------------------------

print("\nCoverage Summary")

print(
    f"Tickets Used     : {interaction_df['Ticket_ID'].nunique()} / {len(support_tickets_df)}"
)

print(
    f"Customers Used   : {interaction_df['Customer_ID'].nunique()} / {len(customers_df)}"
)

print(
    f"Agents Used      : {interaction_df['Agent_ID'].nunique()} / {len(agents_df)}"
)

# ----------------------------------------------------------
# Channel Distribution
# ----------------------------------------------------------

print("\nChannel Distribution (%)")

print(
    round(
        interaction_df["Channel"]
        .value_counts(normalize=True) * 100,
        2
    )
)

# ----------------------------------------------------------
# Interaction Type Distribution
# ----------------------------------------------------------

print("\nInteraction Type Distribution (%)")

print(
    round(
        interaction_df["Interaction_Type"]
        .value_counts(normalize=True) * 100,
        2
    )
)

# ----------------------------------------------------------
# Outcome Distribution
# ----------------------------------------------------------

print("\nInteraction Outcome Distribution (%)")

print(
    round(
        interaction_df["Interaction_Outcome"]
        .value_counts(normalize=True) * 100,
        2
    )
)

# ----------------------------------------------------------
# Average Duration
# ----------------------------------------------------------

print("\nAverage Call Duration")

print(
    interaction_df.groupby("Channel")["Duration_Minutes"].mean().round(2)
)

# ----------------------------------------------------------
# Export
# ----------------------------------------------------------

print("\nExporting Customer_Interactions Sheet...")

with pd.ExcelWriter(
    EXCEL_FILE,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    interaction_df.to_excel(
        writer,
        sheet_name=INTERACTION_SHEET,
        index=False
    )

print("✓ Customer_Interactions Sheet Updated Successfully")

# ----------------------------------------------------------
# Final Report
# ----------------------------------------------------------

print("\n")
print("=" * 65)
print("NovaTech Customer Interaction Generator Report")
print("=" * 65)

print(f"Interactions Generated : {len(interaction_df)}")
print(f"Tickets Covered        : {interaction_df['Ticket_ID'].nunique()}")
print(f"Customers Covered      : {interaction_df['Customer_ID'].nunique()}")
print(f"Agents Covered         : {interaction_df['Agent_ID'].nunique()}")

print(f"\nAverage Duration       : {interaction_df['Duration_Minutes'].mean():.2f} mins")

print("=" * 65)
print("CUSTOMER INTERACTION GENERATOR COMPLETED SUCCESSFULLY")
print("=" * 65)
