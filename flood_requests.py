import requests
import threading

# Number of requests
num_requests = 1000

def send_request():
    try:
        response = requests.get("http://192.168.0.124/")
        print(response.text)  # Print response if needed
    except Exception as e:
        print(f"Request failed: {e}")

# Create and start threads
threads = []
for _ in range(num_requests):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
