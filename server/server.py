from flask import Flask
import json
import serial
import sys
import threading

serial_port = sys.argv[1]
ser = serial.Serial(serial_port, 9600, timeout=None)

app = Flask(__name__)

temperature = 20.0
humidity = 50.0

class HealthEffect:
    def __init__(self):
        self.temperature = temperature
        self.humidity = humidity

    def jsonize(self) -> str:
        return json.dumps(self.__dict__)

@app.route('/')
def index() -> str:
    return HealthEffect().jsonize() 

def fetch_from_serial():
    while True:
        line = ser.readline().decode("utf-8").rstrip()
        print("Fetched: " + line)

def main():
    threading.Thread(target=fetch_from_serial).start()
    app.debug = True
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
    ser.close()
