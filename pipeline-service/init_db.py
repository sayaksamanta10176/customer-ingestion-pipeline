from database import engine, Base
from models.customer import Customer

# Create all tables defined in Base metadata
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
