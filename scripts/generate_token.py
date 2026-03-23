import jwt
import argparse
from datetime import datetime, timedelta
from src.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY_HOURS

def generate_token(tenant_id: str):
    payload = {
        "tenant_id": tenant_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(f"JWT for tenant {tenant_id}:")
    print(token)
    return token

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", required=True, help="Tenant ID")
    args = parser.parse_args()
    generate_token(args.tenant)