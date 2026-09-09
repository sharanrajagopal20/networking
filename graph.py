import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_FILE = "data/traffic.csv"
GRAPH_FOLDER = "static/graphs"

# Create graph folder
os.makedirs(GRAPH_FOLDER, exist_ok=True)

# Read traffic data
df = pd.read_csv(CSV_FILE)

# Make sure Packet Size is numeric
df["Packet Size"] = pd.to_numeric(
    df["Packet Size"],
    errors="coerce"
).fillna(0)


# =========================================================
# GRAPH 1 - PACKET SIZE OVER TIME
# =========================================================

df["Packet Number"] = range(1, len(df) + 1)

plt.figure(figsize=(10, 5))
plt.plot(
    df["Packet Number"],
    df["Packet Size"],
    marker="o"
)

plt.title("Network Traffic - Packet Size Over Time")
plt.xlabel("Packet Number")
plt.ylabel("Packet Size (Bytes)")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    f"{GRAPH_FOLDER}/packet_size.png"
)

plt.close()


# =========================================================
# GRAPH 2 - PROTOCOL DISTRIBUTION
# =========================================================

protocol_counts = df["Protocol"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(
    protocol_counts.index,
    protocol_counts.values
)

plt.title("Network Traffic - Protocol Distribution")
plt.xlabel("Protocol")
plt.ylabel("Number of Packets")
plt.grid(axis="y")
plt.tight_layout()

plt.savefig(
    f"{GRAPH_FOLDER}/protocol_distribution.png"
)

plt.close()


# =========================================================
# GRAPH 3 - TOP 5 DESTINATION IPS
# =========================================================

destination_counts = (
    df["Destination IP"]
    .value_counts()
    .head(5)
)

plt.figure(figsize=(10, 5))
plt.bar(
    destination_counts.index,
    destination_counts.values
)

plt.title("Top 5 Destination IPs")
plt.xlabel("Destination IP")
plt.ylabel("Number of Packets")
plt.xticks(rotation=30)

plt.grid(axis="y")
plt.tight_layout()

plt.savefig(
    f"{GRAPH_FOLDER}/top_destinations.png"
)

plt.close()


# =========================================================
# GRAPH 4 - DATA USAGE BY PROTOCOL
# =========================================================

protocol_traffic = (
    df.groupby("Protocol")["Packet Size"]
    .sum()
)

plt.figure(figsize=(8, 5))
plt.bar(
    protocol_traffic.index,
    protocol_traffic.values
)

plt.title("Network Traffic - Data Usage by Protocol")
plt.xlabel("Protocol")
plt.ylabel("Total Data (Bytes)")
plt.grid(axis="y")
plt.tight_layout()

plt.savefig(
    f"{GRAPH_FOLDER}/protocol_traffic.png"
)

plt.close()


print("======================================")
print("       GRAPH GENERATION COMPLETE")
print("======================================")
print("1. Packet Size Over Time       : OK")
print("2. Protocol Distribution       : OK")
print("3. Top 5 Destination IPs       : OK")
print("4. Data Usage by Protocol      : OK")
print()
print("Graphs saved in:")
print("static/graphs/")
print("======================================")