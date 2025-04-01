import json
import random
import time
from datetime import datetime

# Generate sample API logs with anomalies
def generate_logs(num_logs=100):
    logs = []
    for _ in range(num_logs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "api_name": random.choice(["auth_service", "payment_gateway", "user_profile", "data_fetch"]),
            "response_time": random.randint(100, 500) if random.random() > 0.1 else random.randint(1000, 5000),  # Injecting anomalies
            "status_code": random.choice([200, 200, 200, 500, 400, 503]),
            "error_message": None if random.random() > 0.8 else "Timeout error"
        }
        logs.append(log_entry)
    return logs

# Save logs to a JSON file
def save_logs_to_file(filename="sample_logs.json"):
    logs = generate_logs()
    with open(filename, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"Sample logs saved to {filename}")

if __name__ == "__main__":
    save_logs_to_file()

