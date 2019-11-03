from enum import Enum
from flask import Flask
import json
import serial
import sys
import threading

serial_port = sys.argv[1]
ser = serial.Serial(serial_port, 9600, timeout=None)

app = Flask(__name__)

class ClimateEffect(Enum):
    HEATSTROKE = "heatstroke"
    VIRUS = "virus"
    NOTHING = "nothing"

class Dry(Enum):
    DRYER = "dryer"
    DRY = "dry"
    NORMAL = "normal"

# TODO: should be in class as repository
temperature = 20.0
humidity = 50.0
climate_effect = ClimateEffect.NOTHING
dry = Dry.NORMAL

class HealthEffect:
    def __init__(self):
        self.temperature = temperature
        self.humidity = humidity
        self.climate_effect = climate_effect.name
        self.dry = dry.name

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
