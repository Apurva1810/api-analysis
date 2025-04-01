import json

# Thresholds for anomaly detection
RESPONSE_TIME_THRESHOLD = 1000  # ms (e.g., response time above 1000ms is considered slow)
ERROR_STATUS_CODES = {500, 503, 400}  # Define what errors we care about

# Function to analyze logs
def analyze_logs(filename="sample_logs.json"):
    with open(filename, "r") as f:
        logs = json.load(f)
    
    anomalies = []
    for log in logs:
        if log["response_time"] > RESPONSE_TIME_THRESHOLD:
            anomalies.append(f"High response time detected: {log}")
        if log["status_code"] in ERROR_STATUS_CODES:
            anomalies.append(f"Error detected: {log}")
    
    # Save anomalies to a report
    with open("anomaly_report.txt", "w") as f:
        for anomaly in anomalies:
            f.write(anomaly + "\n")
    
    print(f"Analysis complete! {len(anomalies)} anomalies found. Check anomaly_report.txt")

if __name__ == "__main__":
    analyze_logs()

