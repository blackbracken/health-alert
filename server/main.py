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
    HEATSTROKE = 0
    VIRUS = 1
    NOTHING = 2

class DryEffect(Enum):
    DRYER = 0
    DRY = 1
    NORMAL = 2

# TODO: should be in class as repository
temperature = 20.0
humidity = 50.0

"""
A data object to represents effects of health as json.
"""
class HealthEffectData:
    def __init__(self, temperature, humidity, climate_effect, dry_effect) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.climate_effect = climate_effect.name
        self.dry_effect = dry_effect.name

    @staticmethod
    def from_health_effect(health_effect): # -> HealthEffectData
        return HealthEffectData(health_effect.temperature, health_effect.humidity, health_effect.climate_effect, health_effect.dry_effect)

    def jsonize(self) -> str:
        return json.dumps(self.__dict__)

class HealthEffect:
    def __init__(self) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.climate_effect = ClimateEffect.NOTHING
        self.dry_effect = DryEffect.NORMAL

def fetch_from_serial() -> None:
    while True:
        line = ser.readline().decode("utf-8").rstrip()
        try:
            if line.startswith("t"):
                temperature = float(line[1:])
                print(f"Changed a temperature: {temperature}")
            elif line.startswith("h"):
                humidity = float(line[1:])
                print(f"Changed a humidity: {humidity}")
            else:
                raise ValueError()
        except ValueError:
            print(f"Received an invalid message: {line}")

@app.route('/')
def index() -> str:
    return HealthEffectData.from_health_effect(HealthEffect()).jsonize()

def main() -> None:
    threading.Thread(target=fetch_from_serial).start()
    app.debug = True
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
    ser.close()
