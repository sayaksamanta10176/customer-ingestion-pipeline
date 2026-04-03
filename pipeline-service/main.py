from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from services.ingestion import fetch_all_customers, upsert_customers 
from models.customer import Customer

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/api/health")
def get_health():
    return {
        "status" : "ok",
        "service" : "pipeline-service",
        "port" : 8000
    }

@app.post("/api/ingest")
def ingest_customers(db : Session = Depends(get_db)):
    customers_data = fetch_all_customers()
    if not customers_data:
        HTTPException(status_code=404, detail="No customers found from Flask mock server")

    records_processed = upsert_customers(db, customers_data)
    if records_processed == 0:
        HTTPException(status_code=404, detail="No records were processed")

    return {
        "status" : "success",
        "records_processed" : records_processed
    }

@app.get("/api/customers")
def get_customer(page : int = 1, limit : int = 10, db : Session = Depends(get_db)):
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()

    return {
        "data" : [customer.__dict__ for customer in customers],
        "total" : total,
        "page" : page,
        "limit" : limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id : str, db : Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer '{customer_id}' not found")

    return customer.__dict__