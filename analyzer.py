import pandas as pd

CSV_FILE = "data/traffic.csv"

data = pd.read_csv(CSV_FILE)

total_packets = len(data)
total_bytes = data["Packet Size"].sum()
average_size = data["Packet Size"].mean()
largest_packet = data["Packet Size"].max()

protocol_counts = data["Protocol"].value_counts()
destination_counts = data["Destination IP"].value_counts()

print("======================================")
print("       NETWORK TRAFFIC ANALYSIS")
print("======================================")

print(f"Total Packets       : {total_packets}")
print(f"Total Data          : {total_bytes} bytes")
print(f"Average Packet Size : {average_size:.2f} bytes")
print(f"Largest Packet      : {largest_packet} bytes")

print("\nProtocol Statistics:")
print(protocol_counts)

print("\nTop Destinations:")
print(destination_counts.head(5))

print("\n======================================")
print("Analysis completed.")
print("======================================")