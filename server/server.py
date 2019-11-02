import serial
import sys
import threading
import time

serial_port = sys.argv[1]
ser = serial.Serial(serial_port, 9600, timeout=None)

def fetch_from_serial():
    while True:
        line = ser.readline().decode("utf-8").rstrip()
        print("Fetched: " + line)

def main():
    threading.Thread(target=fetch_from_serial).start()

if __name__ == '__main__':
    main()
    ser.close()
