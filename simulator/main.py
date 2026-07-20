import json
import logging
import random
import time

import paho.mqtt.client as mqtt

# Configuration

ACCESS_TOKEN = "5T3KNrR0AE16I29QxksP"

BROKER = "localhost"
PORT = 1883

SEND_INTERVAL = 1  # seconds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

# MQTT

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(BROKER, PORT, 60)

# Initial state

setpoint = 22.0

outside_temp = 6.0
supply_temp = 18.0

humidity = 45.0

filter_pressure = 20.0

running = True

last_toggle = time.time()

# Simulation loop

try:

    while True:

        # Start / Stop every minute
        if time.time() - last_toggle > 60:
            running = not running
            last_toggle = time.time()

            logging.info(
                f"System {'STARTED' if running else 'STOPPED'}"
            )

        # Outdoor temperature
        outside_temp += random.uniform(-0.15, 0.15)
        outside_temp = max(-20, min(35, outside_temp))

        # Supply temperature
        if running:
            supply_temp += (setpoint - supply_temp) * 0.05
            supply_temp += (outside_temp - supply_temp) * 0.01
        else:
            supply_temp += (outside_temp - supply_temp) * 0.03

        # Humidity
        humidity += random.uniform(-0.2, 0.2)
        humidity = max(35, min(65, humidity))

        # Fans
        if running:
            supply_fan = random.randint(1180, 1220)
            exhaust_fan = random.randint(1170, 1210)
        else:
            supply_fan = 0
            exhaust_fan = 0

        # Damper
        damper = 100 if running else 0

        # Heating / Cooling valves
        if running:

            if supply_temp < setpoint:
                heating = min(100, (setpoint - supply_temp) * 25)
                cooling = 0

            else:
                heating = 0
                cooling = min(100, (supply_temp - setpoint) * 25)

        else:

            heating = 0
            cooling = 0

        # Filter clogging
        if running:
            filter_pressure += 0.08
        else:
            filter_pressure += 0.01

        filter_clogged = filter_pressure >= 80
        alarm = filter_pressure >= 100

        # Maintenance
        if filter_pressure > 120:

            logging.info("Filter replaced")

            filter_pressure = 20

        telemetry = {

            "outsideTemp": round(outside_temp, 1),
            "supplyTemp": round(supply_temp, 1),
            "setpoint": setpoint,

            "humidity": round(humidity, 1),

            "filterPressure": round(filter_pressure, 1),

            "supplyFan": supply_fan,
            "exhaustFan": exhaust_fan,

            "damper": damper,

            "heatingValve": round(heating, 1),
            "coolingValve": round(cooling, 1),

            "running": running,
            "alarm": alarm,
            "filterClogged": filter_clogged

        }

        client.publish(
            "v1/devices/me/telemetry",
            json.dumps(telemetry)
        )

        logging.info(telemetry)

        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:

    logging.info("Simulator stopped")

finally:

    client.disconnect()