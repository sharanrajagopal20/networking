from scapy.all import sniff, IP
import csv
from datetime import datetime


CSV_FILE = "data/traffic.csv"


# Create CSV file and write column headings
with open(CSV_FILE, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Time",
        "Source IP",
        "Destination IP",
        "Protocol",
        "Packet Size"
    ])


def save_packet(packet):
    if IP in packet:
        source = packet[IP].src
        destination = packet[IP].dst
        size = len(packet)

        if packet.haslayer("TCP"):
            protocol = "TCP"
        elif packet.haslayer("UDP"):
            protocol = "UDP"
        elif packet.haslayer("ICMP"):
            protocol = "ICMP"
        else:
            protocol = "Other"

        current_time = datetime.now().strftime("%H:%M:%S")

        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                current_time,
                source,
                destination,
                protocol,
                size
            ])

        print(
            f"{current_time} | "
            f"{source} → {destination} | "
            f"{protocol} | "
            f"{size} bytes"
        )


print("======================================")
print(" Network Traffic Monitoring System")
print("======================================")
print("Capturing 50 packets...\n")

sniff(prn=save_packet, count=50)

print("\nCapture completed.")
print(f"Traffic data saved to: {CSV_FILE}")