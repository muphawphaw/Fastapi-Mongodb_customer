from fastapi import APIRouter,HTTPException
from models.customer_model import Customer
from schemas.customer_schema import customers_serializer
from bson import ObjectId
from config.db import collection
import pymongo


customer = APIRouter()

#route to create customer
@customer.post("/")
async def create_customer(customer : Customer):
    _id = collection.insert_one(dict(customer))
    customer = customers_serializer(collection.find({"_id" : _id.inserted_id}))
    return {"status" : "OK", "data" : customer}

#route to find all customers
@customer.get("/")
async def find_all_customers():
    customers = customers_serializer(collection.find())
    if customers:
        return customers
    else : HTTPException(status_code=404,detail="Customers not found!!!")

#route for sorting name
@customer.get("/customers/sort_by_name/{sort}")
async def sorting_name(sort : str):
    if sort == "asc" :
         ascending_name = customers_serializer(collection.find().sort("name" , pymongo.ASCENDING))
         return ascending_name
    elif sort == "desc":
        descending_name = customers_serializer(collection.find().sort("name", pymongo.DESCENDING))
        return descending_name

#route to get by role
@customer.get("/customers/role/{role}")
async def customer_admin_role(role : str ):
    customer = customers_serializer(collection.find({"role" : role }))
    return customer

#route to find one customer
@customer.get("/customers/{id}")
async def get_one_customer(id : str):
    customer = customers_serializer(collection.find({"_id": ObjectId(id)}))
    if customer:
        if customer[0]["id"] == id:
            return {"Status" :"Found it!!","data" : customer}
        raise HTTPException(status_code=404,detail = "Customer not found!!!")

#route to update customer
@customer.put("/customers/{id}")
async def update_customer(id : str, customer : Customer):
    collection.find_one_and_update(
        {
            "_id" : ObjectId(id)},
        {   "$set" : dict(customer)
        }
    )
    customer = customers_serializer(collection.find({"_id":ObjectId(id)}))
    if customer:
        if customer[0]["id"] == id:
            return {"Successfully updated!!", customer}
        raise HTTPException(status_code=404,detail="Custer not found")

#route to delete customer
@customer.delete("/customers/{id}")
async def delete_customer(id : str):
    collection.find_one_and_delete({"_id" : ObjectId(id)})
    customers_serializer(collection.find())
    return {"Status" : "deleted!!!", "data" : []}

