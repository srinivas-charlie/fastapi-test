from fastapi import FastAPI, HTTPException
app = FastAPI()

@app.get("/")
def homepage():
    return {"message" : " welcome to homepage"}

@app.get("/sub")
def internal_page():
    return {"message" : " welcome to internal webpage"}



users = {
    1: {"name": "Alice", "orders": {
        101: {"item": "Laptop", "price": 1200},
        102: {"item": "Smartphone", "price": 800}
    }},
    2: {"name": "Bob", "orders": {
        103: {"item": "Tablet", "price": 500},
        104: {"item": "Monitor", "price": 300}
    }},
    3: {"name": "Charlie", "orders": {
        105: {"item": "Headphones", "price": 100},
        106: {"item": "Keyboard", "price": 50}
    }}
}

@app.get("/users/{user_id}/orders/{order_id}")
def get_user(user_id: int, order_id: int): 
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    elif order_id not in users[user_id]["orders"]:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        return users[user_id]["orders"][order_id]