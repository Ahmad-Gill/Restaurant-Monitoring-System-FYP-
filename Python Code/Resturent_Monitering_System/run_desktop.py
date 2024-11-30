import subprocess
import webbrowser
import time

def start_django_server():
    """Start the Django server in a separate process."""
    return subprocess.Popen(['python', 'manage.py', 'runserver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    # Start the Django server
    server_process = start_django_server()

    # Allow some time for the server to start
    time.sleep(5)  # Wait for the server to start

    # Open the default web browser to the Django server URL
    webbrowser.open('http://127.0.0.1:8000')

    # Keep the script running to maintain the server
    print("Press Ctrl+C to stop the server.")
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the server...")
        server_process.terminate()

if __name__ == "__main__":
    main()
