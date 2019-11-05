from datetime import datetime
from enum     import Enum
from flask    import Flask
import json
import serial
import sys
import threading

serial_port = sys.argv[1]
ser = serial.Serial(serial_port, 9600, timeout=None)

app = Flask(__name__)

class ClimateEffect(Enum):
    HEATSTROKE_NOTICE = 0
    HEATSTROKE_ALERT = 1
    VIRUS_NOTICE = 2
    VIRUS_ALERT = 3
    NOTHING = 4

class DryEffect(Enum):
    DRY = 0
    NOTHING = 1

"""
A data object to represents effects of health as json.
"""
class HealthEffectData:
    def __init__(self, temperature: float, humidity: float, climate_effect: ClimateEffect, dry_effect: DryEffect) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.climate_effect = climate_effect.name
        self.dry_effect = dry_effect.name

    @staticmethod
    def from_health_effect(health_effect: HealthEffect): # -> HealthEffectData
        return HealthEffectData(health_effect.temperature, health_effect.humidity, health_effect.climate_effect, health_effect.dry_effect)

    def jsonize(self) -> str:
        return json.dumps(self.__dict__)

# TODO: should be in class as repository
temperature = 20.0
humidity = 50.0

class HealthEffect:
    def __init__(self) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.climate_effect = ClimateEffect.NOTHING
        self.dry_effect = DryEffect.NOTHING

        print(f"now temperature: {temperature}")
        print(f"now humidity: {humidity}")

        # TODO: refactor
        now = datetime.now()
        if now.month in range(5, 10 + 1):
            # in summer
            if temperature >= 29.0:
                self.climate_effect = ClimateEffect.HEATSTROKE_ALERT
            elif temperature >= 26.0:
                self.climate_effect = ClimateEffect.HEATSTROKE_NOTICE
            
            if humidity <= 40.0:
                self.dry_effect = DryEffect.DRY
        else:
            # in winter
            in_cold = temperature <= 18.0
            in_dry = humidity <= 40.0
            
            if in_cold and in_dry:
                self.climate_effect = ClimateEffect.VIRUS_ALERT
            elif in_cold or in_dry:
                self.climate_effect = ClimateEffect.VIRUS_NOTICE

def fetch_from_serial() -> None:
    global temperature
    global humidity

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
