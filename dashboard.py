from flask import Flask, render_template, jsonify
import pandas as pd
import os
import psutil
import time
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


app = Flask(__name__)


# ============================================================
# FILE PATH
# ============================================================

CSV_FILE = "data/traffic.csv"

previous_network = None
previous_time = None


# ============================================================
# READ TRAFFIC DATA
# ============================================================

def get_traffic_data():

    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(
            columns=[
                "Time",
                "Source IP",
                "Destination IP",
                "Protocol",
                "Packet Size"
            ]
        )

    try:

        df = pd.read_csv(CSV_FILE)

        if "Packet Size" in df.columns:
            df["Packet Size"] = pd.to_numeric(
                df["Packet Size"],
                errors="coerce"
            )

            df = df.dropna(
                subset=["Packet Size"]
            )

        return df

    except Exception as e:

        print("Error reading traffic data:", e)

        return pd.DataFrame(
            columns=[
                "Time",
                "Source IP",
                "Destination IP",
                "Protocol",
                "Packet Size"
            ]
        )


# ============================================================
# BANDWIDTH CALCULATION
# ============================================================

def calculate_bandwidth():

    global previous_network
    global previous_time

    current_network = psutil.net_io_counters()
    current_time = time.time()

    download_speed = 0
    upload_speed = 0

    if previous_network is not None:

        time_difference = (
            current_time - previous_time
        )

        if time_difference > 0:

            download_speed = (
                current_network.bytes_recv
                - previous_network.bytes_recv
            ) / time_difference

            upload_speed = (
                current_network.bytes_sent
                - previous_network.bytes_sent
            ) / time_difference

    previous_network = current_network
    previous_time = current_time

    return (
        round(download_speed / 1024, 2),
        round(upload_speed / 1024, 2)
    )


# ============================================================
# TRAFFIC GRAPH
# ============================================================

def create_traffic_graph(df):

    os.makedirs(
        "static/graphs",
        exist_ok=True
    )

    graph_path = (
        "static/graphs/traffic_graph.png"
    )

    plt.figure(figsize=(10, 5))

    if len(df) > 0:

        plt.plot(
            range(1, len(df) + 1),
            df["Packet Size"],
            marker="o"
        )

        plt.xlabel("Packet Number")
        plt.ylabel("Packet Size (Bytes)")
        plt.title("Network Traffic Analysis")
        plt.grid(True)

    else:

        plt.text(
            0.5,
            0.5,
            "No traffic data available",
            ha="center",
            va="center"
        )

        plt.title("Network Traffic Analysis")

    plt.tight_layout()

    plt.savefig(graph_path)

    plt.close()


# ============================================================
# PROTOCOL GRAPH
# ============================================================

def create_protocol_graph(df):

    os.makedirs(
        "static/graphs",
        exist_ok=True
    )

    graph_path = (
        "static/graphs/protocol_graph.png"
    )

    plt.figure(figsize=(8, 5))

    if len(df) > 0:

        protocol_counts = (
            df["Protocol"]
            .value_counts()
        )

        protocol_counts.plot(
            kind="bar"
        )

        plt.xlabel("Protocol")
        plt.ylabel("Number of Packets")
        plt.title("Protocol Distribution")
        plt.xticks(rotation=0)

    else:

        plt.text(
            0.5,
            0.5,
            "No protocol data available",
            ha="center",
            va="center"
        )

        plt.title("Protocol Distribution")

    plt.tight_layout()

    plt.savefig(graph_path)

    plt.close()


# ============================================================
# BANDWIDTH GRAPH
# ============================================================

def create_bandwidth_graph(
    download_speed,
    upload_speed
):

    os.makedirs(
        "static/graphs",
        exist_ok=True
    )

    graph_path = (
        "static/graphs/bandwidth_graph.png"
    )

    plt.figure(figsize=(8, 5))

    labels = [
        "Download",
        "Upload"
    ]

    values = [
        download_speed,
        upload_speed
    ]

    plt.bar(
        labels,
        values
    )

    plt.ylabel("Speed (KB/s)")
    plt.title("Current Bandwidth Usage")

    plt.tight_layout()

    plt.savefig(graph_path)

    plt.close()


# ============================================================
# ANOMALY GRAPH
# ============================================================

def create_anomaly_graph(
    normal_count,
    anomaly_count
):

    os.makedirs(
        "static/graphs",
        exist_ok=True
    )

    graph_path = (
        "static/graphs/anomaly_graph.png"
    )

    plt.figure(figsize=(8, 5))

    labels = [
        "Normal",
        "Anomaly"
    ]

    values = [
        normal_count,
        anomaly_count
    ]

    plt.bar(
        labels,
        values
    )

    plt.ylabel("Number of Packets")
    plt.title("Network Anomaly Analysis")

    plt.tight_layout()

    plt.savefig(graph_path)

    plt.close()


# ============================================================
# SMART RECOMMENDATION
# ============================================================

def generate_recommendation(
    total_traffic,
    average_packet,
    anomaly_count,
    tcp_count,
    udp_count,
    download_speed,
    upload_speed
):

    recommendations = []

    # --------------------------------------------------------
    # TRAFFIC LEVEL
    # --------------------------------------------------------

    if total_traffic >= 200000:

        recommendations.append(
            "High network traffic detected. "
            "Monitor high-bandwidth applications "
            "and consider optimizing network usage."
        )

    elif total_traffic >= 50000:

        recommendations.append(
            "Network traffic is moderately active. "
            "Continue monitoring bandwidth usage."
        )

    else:

        recommendations.append(
            "Network traffic is currently low "
            "and operating normally."
        )

    # --------------------------------------------------------
    # ANOMALY DETECTION
    # --------------------------------------------------------

    if anomaly_count >= 3:

        recommendations.append(
            f"{anomaly_count} unusually large packets "
            "were detected. Investigate the traffic "
            "source and destination."
        )

    elif anomaly_count > 0:

        recommendations.append(
            f"{anomaly_count} unusual packet was detected. "
            "Continue monitoring the network for "
            "repeated anomalies."
        )

    # --------------------------------------------------------
    # PACKET SIZE
    # --------------------------------------------------------

    if average_packet > 1000:

        recommendations.append(
            "The average packet size is relatively high. "
            "Monitor applications generating large packets."
        )

    # --------------------------------------------------------
    # PROTOCOL ANALYSIS
    # --------------------------------------------------------

    total_protocol_packets = (
        tcp_count + udp_count
    )

    if total_protocol_packets > 0:

        udp_percentage = (
            udp_count /
            total_protocol_packets
        ) * 100

        if udp_percentage > 60:

            recommendations.append(
                "UDP traffic is dominant. "
                "Monitor real-time, streaming, "
                "or multimedia applications."
            )

    # --------------------------------------------------------
    # DOWNLOAD BANDWIDTH
    # --------------------------------------------------------

    if download_speed > 5000:

        recommendations.append(
            "Download bandwidth usage is high. "
            "Monitor active applications and devices."
        )

    # --------------------------------------------------------
    # UPLOAD BANDWIDTH
    # --------------------------------------------------------

    if upload_speed > 2000:

        recommendations.append(
            "Upload bandwidth usage is high. "
            "Check applications generating significant "
            "outbound traffic."
        )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return " ".join(
        recommendations
    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    df = get_traffic_data()

    # --------------------------------------------------------
    # BASIC STATISTICS
    # --------------------------------------------------------

    total_packets = len(df)

    if total_packets > 0:

        total_traffic = int(
            df["Packet Size"].sum()
        )

        average_packet = round(
            df["Packet Size"].mean(),
            2
        )

    else:

        total_traffic = 0
        average_packet = 0

    # --------------------------------------------------------
    # PROTOCOL COUNTS
    # --------------------------------------------------------

    tcp_count = int(
        (
            df["Protocol"] == "TCP"
        ).sum()
    )

    udp_count = int(
        (
            df["Protocol"] == "UDP"
        ).sum()
    )

    other_count = (
        total_packets
        - tcp_count
        - udp_count
    )

    # --------------------------------------------------------
    # TRAFFIC STATUS
    # --------------------------------------------------------

    if total_traffic < 50000:

        traffic_status = "LOW TRAFFIC"

    elif total_traffic < 200000:

        traffic_status = "MEDIUM TRAFFIC"

    else:

        traffic_status = "HIGH TRAFFIC"

    # --------------------------------------------------------
    # ANOMALY DETECTION
    # --------------------------------------------------------

    if total_packets > 0:

        threshold = (
            average_packet * 3
        )

        anomaly_count = int(
            (
                df["Packet Size"] > threshold
            ).sum()
        )

    else:

        threshold = 0
        anomaly_count = 0

    if anomaly_count >= 3:

        anomaly_status = (
            "ANOMALY DETECTED"
        )

        anomaly_message = (
            f"{anomaly_count} unusually large "
            "packets detected."
        )

    elif anomaly_count > 0:

        anomaly_status = "WARNING"

        anomaly_message = (
            f"{anomaly_count} unusual "
            "packet detected."
        )

    else:

        anomaly_status = "NORMAL"

        anomaly_message = (
            "No unusual traffic detected."
        )

    # --------------------------------------------------------
    # BANDWIDTH
    # --------------------------------------------------------

    download_speed, upload_speed = (
        calculate_bandwidth()
    )

    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    recommendation = (
        generate_recommendation(
            total_traffic,
            average_packet,
            anomaly_count,
            tcp_count,
            udp_count,
            download_speed,
            upload_speed
        )
    )

    # --------------------------------------------------------
    # CREATE GRAPHS
    # --------------------------------------------------------

    create_traffic_graph(df)

    create_protocol_graph(df)

    create_bandwidth_graph(
        download_speed,
        upload_speed
    )

    normal_count = (
        total_packets - anomaly_count
    )

    create_anomaly_graph(
        normal_count,
        anomaly_count
    )

    # --------------------------------------------------------
    # RENDER DASHBOARD
    # --------------------------------------------------------

    return render_template(
        "dashboard.html",
        total_packets=total_packets,
        total_traffic=total_traffic,
        average_packet=average_packet,
        tcp_count=tcp_count,
        udp_count=udp_count,
        other_count=other_count,
        traffic_status=traffic_status,
        anomaly_status=anomaly_status,
        anomaly_message=anomaly_message,
        recommendation=recommendation,
        download_speed=download_speed,
        upload_speed=upload_speed
    )


# ============================================================
# BANDWIDTH API
# ============================================================

@app.route("/bandwidth")
def bandwidth():

    download_speed, upload_speed = (
        calculate_bandwidth()
    )

    return jsonify({

        "download": download_speed,

        "upload": upload_speed

    })


# ============================================================
# LIVE DATA API
# ============================================================

@app.route("/live-data")
def live_data():

    # --------------------------------------------------------
    # READ TRAFFIC DATA
    # --------------------------------------------------------

    df = get_traffic_data()

    total_packets = len(df)

    if total_packets > 0:

        total_traffic = int(
            df["Packet Size"].sum()
        )

        average_packet = round(
            df["Packet Size"].mean(),
            2
        )

    else:

        total_traffic = 0
        average_packet = 0

    # --------------------------------------------------------
    # PROTOCOL ANALYSIS
    # --------------------------------------------------------

    tcp_count = int(
        (
            df["Protocol"] == "TCP"
        ).sum()
    )

    udp_count = int(
        (
            df["Protocol"] == "UDP"
        ).sum()
    )

    other_count = (
        total_packets
        - tcp_count
        - udp_count
    )

    # --------------------------------------------------------
    # ANOMALY DETECTION
    # --------------------------------------------------------

    if total_packets > 0:

        threshold = (
            average_packet * 3
        )

        anomaly_count = int(
            (
                df["Packet Size"] > threshold
            ).sum()
        )

    else:

        anomaly_count = 0

    if anomaly_count >= 3:

        anomaly_status = (
            "ANOMALY DETECTED"
        )

        anomaly_message = (
            f"{anomaly_count} unusually large "
            "packets detected."
        )

    elif anomaly_count > 0:

        anomaly_status = "WARNING"

        anomaly_message = (
            f"{anomaly_count} unusual "
            "packet detected."
        )

    else:

        anomaly_status = "NORMAL"

        anomaly_message = (
            "No unusual traffic detected."
        )

    # --------------------------------------------------------
    # BANDWIDTH
    # --------------------------------------------------------

    download_speed, upload_speed = (
        calculate_bandwidth()
    )

    # --------------------------------------------------------
    # TRAFFIC STATUS
    # --------------------------------------------------------

    if total_traffic < 50000:

        traffic_status = "LOW TRAFFIC"

    elif total_traffic < 200000:

        traffic_status = "MEDIUM TRAFFIC"

    else:

        traffic_status = "HIGH TRAFFIC"

    # --------------------------------------------------------
    # SMART RECOMMENDATION
    # --------------------------------------------------------

    recommendation = (
        generate_recommendation(
            total_traffic,
            average_packet,
            anomaly_count,
            tcp_count,
            udp_count,
            download_speed,
            upload_speed
        )
    )

    # --------------------------------------------------------
    # RETURN LIVE DATA
    # --------------------------------------------------------

    return jsonify({

        "total_packets": total_packets,

        "total_traffic": total_traffic,

        "average_packet": average_packet,

        "tcp_count": tcp_count,

        "udp_count": udp_count,

        "other_count": other_count,

        "traffic_status": traffic_status,

        "anomaly_status": anomaly_status,

        "anomaly_message": anomaly_message,

        "recommendation": recommendation,

        "download_speed": download_speed,

        "upload_speed": upload_speed

    })


# ============================================================
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )