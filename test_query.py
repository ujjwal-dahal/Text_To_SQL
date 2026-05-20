#!/usr/bin/env python3
import requests
import json
import sys

try:
    response = requests.post(
        "http://localhost:8000/agent/sql",
        json={"question": "Get payments with customer country"},
        timeout=30,
    )
    data = response.json()

    print("Status:", data.get("status"))
    print("Attempts:", data.get("attempts"))
    print("Execution Time:", data.get("execution_time_ms"), "ms")
    print("\nGenerated SQL:")
    print(data.get("sql"))
    print("\nResult Sample:")
    if data.get("result"):
        print(
            data.get("result")[0]
            if isinstance(data.get("result"), list)
            else data.get("result")
        )
    print("\nSummary:")
    print(data.get("summary", "N/A"))
    print("\nError:", data.get("error", "None"))

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
