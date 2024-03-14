def customer_serializer(customer) -> dict:
    return {
        "id" : str(customer["_id"]),
        "name" : customer["name"],
        "role" : customer["role"],
        "address" : customer["address"],
        "contact" : customer["contact"]
    }

def customers_serializer(customers) -> list:
    return [customer_serializer(customer)for customer in customers]