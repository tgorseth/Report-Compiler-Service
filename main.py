from fastapi import FastAPI
import httpx
from aggregator import compile_report  # pluggable version

app = FastAPI(title="Report Compiler Service")

SERVICES = {
    "orders": "http://orders-service:8001",
    "customers": "http://customers-service:8002",
    "inventory": "http://inventory-service:8003"
}

@app.get("/report")
async def generate_report():
    async with httpx.AsyncClient() as client:
        orders = (await client.get(f"{SERVICES['orders']}/orders")).json()
        customers = (await client.get(f"{SERVICES['customers']}/customers")).json()
        inventory = (await client.get(f"{SERVICES['inventory']}/inventory")).json()

    report = compile_report(
        data={
            "orders": orders,
            "customers": customers,
            "inventory": inventory,
        },
        aggregations={
            "total_orders": lambda d: len(d["orders"]),
            "total_customers": lambda d: len(d["customers"]),
            "inventory_count": lambda d: sum(i["quantity"] for i in d["inventory"]),
        },
        groupings={
            "orders_by_customer": {
                "source": "orders",
                "keys": [c["id"] for c in customers],
                "fn": lambda order, cid: order["customer_id"] == cid
            }
        }
    )

    return {"report": report}
