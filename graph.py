import pandas as pd
import matplotlib.pyplot as plt
import os
import psutil
import time

CSV_FILE = "data/traffic.csv"
GRAPH_FOLDER = "static/graphs"

# Create graph folder
os.makedirs(GRAPH_FOLDER, exist_ok=True)


# =========================================================
# READ TRAFFIC DATA
# =========================================================

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


# =========================================================
# GRAPH 5 - BANDWIDTH USAGE
# =========================================================

print("Measuring current bandwidth...")

# Get network counters before measurement
before = psutil.net_io_counters()

# Wait for 1 second
time.sleep(1)

# Get network counters after measurement
after = psutil.net_io_counters()

# Calculate speed in KB/s
download_speed = (
    after.bytes_recv - before.bytes_recv
) / 1024

upload_speed = (
    after.bytes_sent - before.bytes_sent
) / 1024


plt.figure(figsize=(8, 5))

labels = ["Download", "Upload"]
values = [download_speed, upload_speed]

bars = plt.bar(
    labels,
    values
)

plt.title("Bandwidth Usage")
plt.xlabel("Connection")
plt.ylabel("Speed (KB/s)")
plt.grid(axis="y")

# Show values above bars
for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    f"{GRAPH_FOLDER}/bandwidth_graph.png"
)

plt.close()


# =========================================================
# COMPLETION MESSAGE
# =========================================================

print("======================================")
print("       GRAPH GENERATION COMPLETE")
print("======================================")

print("1. Packet Size Over Time       : OK")
print("2. Protocol Distribution       : OK")
print("3. Top 5 Destination IPs       : OK")
print("4. Data Usage by Protocol      : OK")
print("5. Bandwidth Usage             : OK")

print()
print(f"Download Speed : {download_speed:.2f} KB/s")
print(f"Upload Speed   : {upload_speed:.2f} KB/s")

print()
print("Graphs saved in:")
print("static/graphs/")
print("======================================")