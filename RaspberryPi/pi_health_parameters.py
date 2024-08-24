import psutil
from gpiozero import CPUTemperature
import requests
import json
import time
from datetime import datetime
# Constants
MAX_READINGS = 10

# CPU usage percentage
def get_cpu_usage():
    usage = psutil.cpu_percent()
    return usage

# Free memory
def get_free_memory():
    free_memory = psutil.virtual_memory()
    free_memory = list(free_memory)[1]  # Index 1 corresponds to available memory
    return free_memory

# Network parameters
def get_network_params():
    network_params = psutil.net_io_counters()
    network_params = list(network_params)
    packets_recv = network_params[3]  # Index 3 corresponds to packets received
    err_in = network_params[4]  # Index 4 corresponds to input errors
    drop_in = network_params[5]  # Index 5 corresponds to incoming packets dropped
    return packets_recv, err_in, drop_in

# CPU temperature
def get_cpu_temperature():
    cpu = CPUTemperature()
    return cpu.temperature

# Collect device parameters
def collect_device_parameters():

    packets_recv, err_in, drop_in = get_network_params()
    data = {
        "device_time": datetime.now(),
        "cpu_usage": get_cpu_usage(),
        "free_memory": get_free_memory(),
        "packets_recv": packets_recv,
        "err_in": err_in,
        "drop_in": drop_in,
        "cpu_temperature": get_cpu_temperature()
    }
    return data

# Send data via HTTP POST request
def send_data_to_server(data):
    url = "https://grand-grown-swine.ngrok-free.app"
    headers = {"Content-Type": "application/json"}
    
    payload = {"batch data": data}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    readings = []
    
    while True:
        # Collect and store data
        device_data = collect_device_parameters()
        readings.append(device_data)
        
        # If we have enough readings, send them to the server
        if len(readings) >= MAX_READINGS:
            print(f"Sending {len(readings)} readings to the server...")
            print(readings)
            #send_data_to_server(readings)
            readings.clear()  # Clear the list after sending
            
        # Wait for 1 second before the next reading
        time.sleep(1)
