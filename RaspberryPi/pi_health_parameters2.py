import psutil
import subprocess
import os
import shutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory_info = psutil.virtual_memory()
    return memory_info.percent

def get_network_traffic():
    network_info = psutil.net_io_counters()
    return network_info.bytes_sent, network_info.bytes_recv

def get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    return used / total * 100  # Percentage used

def get_load_avg():
    return os.getloadavg()

def get_temperature():
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
    return temp.strip()

def main():
    print("CPU Usage: ", get_cpu_usage(), "%")
    print("Memory Usage: ", get_memory_usage(), "%")
    bytes_sent, bytes_recv = get_network_traffic()
    print(f"Network Traffic - Sent: {bytes_sent} bytes, Received: {bytes_recv} bytes")
    print("Disk Usage: ", get_disk_usage(), "%")
    load1, load5, load15 = get_load_avg()
    print(f"Load Average - 1m: {load1}, 5m: {load5}, 15m: {load15}")
    print("Temperature: ", get_temperature())

if __name__ == "__main__":
    main()
