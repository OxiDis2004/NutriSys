import os

HOSTNAME = 'localhost'
PORT = 8000

def get_hostname():
    global HOSTNAME
    HOSTNAME = os.getenv('HOSTNAME')

def server():
    return f"https://{HOSTNAME}:{PORT}"
