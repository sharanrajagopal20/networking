import pandas as pd

# Load traffic data
data = pd.read_csv("data/traffic.csv")

print("======================================")
print("       NETWORK TRAFFIC OPTIMIZER")
print("======================================")

# Total traffic
total_bytes = data["Packet Size"].sum()
total_packets = len(data)

print(f"\nTotal Packets : {total_packets}")
print(f"Total Traffic : {total_bytes} bytes")

# Protocol analysis
protocol_counts = data["Protocol"].value_counts()

print("\nProtocol Usage:")
print(protocol_counts)

# Traffic level
if total_bytes > 50000:
    print("\n⚠ HIGH TRAFFIC DETECTED")
    print("Recommendation: Reduce unnecessary network traffic.")
elif total_bytes > 20000:
    print("\n⚠ MODERATE TRAFFIC")
    print("Recommendation: Monitor bandwidth usage.")
else:
    print("\n✓ LOW TRAFFIC")
    print("Recommendation: Network traffic is normal.")

# Find largest packets
largest = data.nlargest(5, "Packet Size")

print("\nTop 5 Largest Packets:")
print(largest[["Source IP", "Destination IP", "Protocol", "Packet Size"]])

print("\n======================================")
print("Optimization analysis completed.")
print("======================================")