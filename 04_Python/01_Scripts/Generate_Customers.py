# 1. Import Libraries

# 2. Define Company Data

# 3. Create Region Mapping

# 4. Create Agent Distribution

# 5. Define Industries

# 6. Generate Customer Records

# 7. Create DataFrame

# 8. Save Excel File

# 9. Display Summary
import pandas as pd
import random
from faker import Faker
from datetime import datetime
from openpyxl import load_workbook
import os
fake = Faker()
print("Running Generate_Customers.py")
TOTAL_CUSTOMERS = 750
regions = {
    "R001": {
        "country": "United States",
        "cities": ["New York", "Chicago", "Dallas", "Seattle"]
    },

    "R002": {
        "country": "United Kingdom",
        "cities": ["London", "Manchester", "Birmingham"]
    },

    "R003": {
        "country": "Singapore",
        "cities": ["Singapore"]
    },

    "R004": {
        "country": "India",
        "cities": ["Bengaluru", "Mumbai", "Hyderabad", "Pune"]
    },

    "R005": {
        "country": "United Arab Emirates",
        "cities": ["Dubai", "Abu Dhabi"]
    },

    "R006": {
        "country": "Australia",
        "cities": ["Sydney", "Melbourne", "Brisbane"]
    },

    "R007": {
        "country": "Brazil",
        "cities": ["São Paulo", "Rio de Janeiro"]
    },

    "R008": {
        "country": "South Africa",
        "cities": ["Johannesburg", "Cape Town"]
    }
}
industries = [
    "Technology",
    "Healthcare",
    "Finance",
    "Retail",
    "Manufacturing",
    "Education",
    "Telecommunications",
    "Logistics",
    "Government"
]
customer_types = ["Enterprise", "SMB", "Startup"]
premium_statuses = ["Yes", "No"]
customer_statuses = ["Active", "Inactive"]
company_prefix = [
    "Apex",
    "Vertex",
    "Orion",
    "Global",
    "Prime",
    "Bright",
    "Elite",
    "Zenith",
    "NextGen",
    "Infinity",
    "BlueSky",
    "Fusion",
    "Core",
    "Vision",
    "Pioneer"
]

company_suffix = [
    "Technologies",
    "Healthcare",
    "Finance",
    "Retail",
    "Manufacturing",
    "Logistics",
    "Solutions",
    "Systems",
    "Industries",
    "Consulting",
    "Corporation",
    "Enterprises"
]
customers = []
for i in range(1, TOTAL_CUSTOMERS + 1):
    customer_id = f"C{i:06d}"

    company_name = (
        random.choice(company_prefix)
        + " "
        + random.choice(company_suffix)
        + "Ltd."
    )
    contact_person = fake.name()
    email = fake.company_email()
    phone_number = fake.phone_number()
    region_id = random.choice(list(regions.keys()))
    country = regions[region_id]["country"]
    city = random.choice(regions[region_id]["cities"])
    industry = random.choices(
        population=industries,
        weights=[20, 18, 15, 12, 10, 8, 7, 5, 5],
        k=1
    )[0]
    customer_type = random.choices(
            population=customer_types,
            weights=[50, 30, 20],
            k=1
        )[0]
    premium_status = random.choices(
            population=premium_statuses,
            weights=[20, 80],
            k=1
        )[0]
    customer_status = random.choices(
            population=customer_statuses,
            weights=[92, 8],
            k=1
        )[0]
    agent_id = f"A{random.randint(1,25):03d}"
    join_date = fake.date_between(
            start_date="-5y",
            end_date="today"
        )
    customers.append({
            "Customer_ID": customer_id,
            "Customer_Name": company_name,
            "Contact_Person": contact_person,
            "Email": email,
            "Phone_Number": phone_number,
            "City": city,
            "Region_ID": region_id,
            "Country": country,
            "Industry": industry,
            "Customer_Type": customer_type,
            "Premium_Status": premium_status,
            "Agent_ID": agent_id,
            "Join_Date": join_date,
            "Customer_Status": customer_status
        })
print("Loop completed")
print("Length of customers list:", len(customers))
df = pd.DataFrame(customers)

excel_file = r"C:\Users\FCI\Desktop\Customer Experience & Service Operations Intelligence\04_Python\03_Datasets\NovaTech_Customer_Experience_Dataset.xlsx"

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:
    df.to_excel(writer, sheet_name="Customers", index=False)

print("Customers sheet updated successfully in NovaTech_Customer_Experience_Dataset.xlsx!")
print(f"Total Customers: {len(df)}")

