import pandas as pd
import os

CSV_FILE = "data/traffic.csv"


def detect_anomalies():

    if not os.path.exists(CSV_FILE):
        return {
            "status": "NO DATA",
            "message": "Traffic data not available."
        }

    try:
        df = pd.read_csv(CSV_FILE)

        if df.empty:
            return {
                "status": "NO DATA",
                "message": "No network packets available."
            }

        # Convert packet size to numbers
        df["Packet Size"] = pd.to_numeric(
            df["Packet Size"],
            errors="coerce"
        ).fillna(0)

        # Calculate average packet size
        average_size = df["Packet Size"].mean()

        # Detect unusually large packets
        threshold = average_size * 3

        anomalies = df[
            df["Packet Size"] > threshold
        ]

        anomaly_count = len(anomalies)

        if anomaly_count > 0:

            return {
                "status": "ANOMALY DETECTED",
                "message": (
                    f"{anomaly_count} unusually large "
                    f"packet(s) detected."
                )
            }

        else:

            return {
                "status": "NORMAL",
                "message": "No unusual traffic detected."
            }

    except Exception as error:

        print("Anomaly detection error:", error)

        return {
            "status": "ERROR",
            "message": "Unable to analyze traffic."
        }


if __name__ == "__main__":

    result = detect_anomalies()

    print("======================================")
    print("       NETWORK ANOMALY DETECTION")
    print("======================================")
    print("Status  :", result["status"])
    print("Message :", result["message"])
    print("======================================")