from fastapi import FastAPI
from routes.customer_route import customer
app = FastAPI()
app.include_router(customer)