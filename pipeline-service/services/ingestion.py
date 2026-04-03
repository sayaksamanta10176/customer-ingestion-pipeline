import requests
from database import get_db
from datetime import datetime
from sqlalchemy.orm import Session
from models.customer import Customer

FLASK_BASE_URL = "http://mock-server:5000"

def fetch_all_customers():
    all_customers = []
    page = 1
    limit = 10

    while True:
        response = requests.get(f"{FLASK_BASE_URL}/api/customers", params={"page":page,"limit":limit})
        data = response.json()

        customers = data["data"]
        all_customers.extend(customers)

        total = data["total"]
        if len(all_customers) >= total: 
            break        

        page += 1

    return all_customers

def upsert_customers(db: Session, customers: list):
    records_processed = 0

    for c in customers:
        existing = db.query(Customer).filter(Customer.customer_id == c["customer_id"]).first()

        if existing:
            # Update existing customer
            existing.first_name      = c["first_name"]
            existing.last_name       = c["last_name"]
            existing.email           = c["email"]
            existing.address         = c["address"]
            existing.date_of_birth   = datetime.strptime(c["date_of_birth"], "%Y-%m-%d").date()
            existing.account_balance = c["account_balance"]
            existing.created_at      = datetime.strptime(c["created_at"], "%Y-%m-%dT%H:%M:%S")
        else:
            # Insert new customer
            new_customer = Customer(
                customer_id     = c["customer_id"],
                first_name      = c["first_name"],
                last_name       = c["last_name"],
                email           = c["email"],
                address         = c["address"],
                date_of_birth   = datetime.strptime(c["date_of_birth"], "%Y-%m-%d").date(),
                account_balance = c["account_balance"],
                created_at      = datetime.strptime(c["created_at"], "%Y-%m-%dT%H:%M:%S")
            )
            db.add(new_customer)

        records_processed += 1

    db.commit()
    return records_processed