from fastapi import FastAPI, Depends, HTTPException, status
from src.auth import get_current_tenant
from src.database import get_db_cursor
from src.audit import log_context_access
from src.models import Order, Customer
from typing import List

app = FastAPI(title="MCP Context Server")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/context/orders", response_model=List[Order])
async def get_orders(tenant: str = Depends(get_current_tenant)):
    log_context_access(tenant, "/context/orders")
    with get_db_cursor() as cur:
        cur.execute("SELECT id, customer_name, total FROM orders WHERE tenant_id = %s", (tenant,))
        rows = cur.fetchall()
        return [Order(id=r[0], customer_name=r[1], total=r[2]) for r in rows]

@app.get("/context/customers", response_model=List[Customer])
async def get_customers(tenant: str = Depends(get_current_tenant)):
    log_context_access(tenant, "/context/customers")
    with get_db_cursor() as cur:
        cur.execute("SELECT id, name, email FROM customers WHERE tenant_id = %s", (tenant,))
        rows = cur.fetchall()
        return [Customer(id=r[0], name=r[1], email=r[2]) for r in rows]

# Optional: If you want to accept a dynamic query from an LLM, you could add:
# @app.post("/context/query")
# async def query_context(tenant: str = Depends(get_current_tenant), query: str = Body(...)):
#     ... but ensure you sanitize input to prevent SQL injection.