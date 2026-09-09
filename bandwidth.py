import psutil
import time

print("========================================")
print(" REAL-TIME BANDWIDTH MONITOR")
print("========================================")
print("Press Ctrl+C to stop.\n")

previous = psutil.net_io_counters()

try:
    while True:
        time.sleep(1)

        current = psutil.net_io_counters()

        upload = current.bytes_sent - previous.bytes_sent
        download = current.bytes_recv - previous.bytes_recv

        upload_kb = upload / 1024
        download_kb = download / 1024

        print(
            f"Download: {download_kb:8.2f} KB/s | "
            f"Upload: {upload_kb:8.2f} KB/s"
        )

        previous = current

except KeyboardInterrupt:
    print("\n\nBandwidth monitoring stopped.")