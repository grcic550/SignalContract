import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI()

users = [
    {
        "id": "user-42",
        "name": "John Does",
        "role": "user",
    },
    {
        "id": "admin-1",
        "name": "Marcus Aurelius",
        "role": "admin",
    },
]

current_user = users[0]


@app.get("/health")
async def root():
    return {
        "message": "Health is one of the most importatnt "
        "things in life. Health is wealth. "
        "Health is the first step to happiness."
    }


@app.get("/whoami")
async def whoami():
    return current_user


@app.delete("/databases/prod_db")
async def delete_database():
    id = str(uuid.uuid4())

    if current_user["role"] == "admin":
        return {"message": "Database deleted successfully."}
    else:
        event_dictionary = {
            "event_type": "authorization.denied",
            "actor": current_user["id"],
            "action": "delete_database",
            "target": "prod_db",
            "outcome": "denied",
            "reason": "insufficient_privileges",
            "timestamp": datetime.now(UTC).isoformat(),
            "correlation_id": id,
        }

        with open(
            Path(__file__).resolve().parent / "event_denied.jsonl",
            "a",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(event_dictionary) + "\n")

        raise HTTPException(
            status_code=403,
            detail=f"Forbidden: User {current_user['name']}"
            f" does not have permission to delete the database.",
            headers={"X-Correlation-ID": id},
        )
