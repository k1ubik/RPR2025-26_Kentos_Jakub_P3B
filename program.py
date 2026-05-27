import RPi.GPIO as GPIO
import time
import os

# ===== ČEKÁNÍ PO BOOTU =====
time.sleep(10)

# ===== GPIO PINY =====
PIR = 17
FLAME = 22
SOUND = 27
GAS = 24

# ===== GPIO SETUP =====
GPIO.setmode(GPIO.BCM)

GPIO.setup(PIR, GPIO.IN)
GPIO.setup(FLAME, GPIO.IN)
GPIO.setup(SOUND, GPIO.IN)
GPIO.setup(GAS, GPIO.IN)

# ===== DS18B20 =====
base_dir = '/sys/bus/w1/devices/'

device_file = ""

for item in os.listdir(base_dir):
    if item.startswith('28-'):
        device_file = base_dir + item + '/w1_slave'

# ===== ČTENÍ TEPLOTY =====
def read_temp():

    file = open(device_file, 'r')
    text = file.read()
    file.close()

    temp = text.split('t=')[1]
    temp_c = float(temp) / 1000

    return round(temp_c, 2)

# ===== POSLEDNÍ STAVY =====
last_output = ""
history = []

print("Program spuštěn", flush=True)

# ===== HLAVNÍ PROGRAM =====
try:

    while True:

        # ===== TEPLOTA =====
        temperature = read_temp()

        # ===== PIR =====
        if GPIO.input(PIR):
            pir_state = "Pohyb detekován"
        else:
            pir_state = "Žádný pohyb"

        # ===== FLAME =====
        if GPIO.input(FLAME) == 0:
            flame_state = "Plamen detekován"
        else:
            flame_state = "Žádný plamen"

        # ===== SOUND =====
        if GPIO.input(SOUND) == 1:
            sound_state = "Zvuk detekován"
        else:
            sound_state = "Žádný zvuk"

        # ===== GAS =====
        if GPIO.input(GAS) == 0:
            gas_state = "Plyn detekován"
        else:
            gas_state = "Žádný plyn"

        # ===== AKTUÁLNÍ VÝSTUP =====
        output = f"""
Teplota: {temperature} °C
PIR: {pir_state}
Flame: {flame_state}
Sound: {sound_state}
Gas: {gas_state}
"""

        # ===== POUZE PŘI ZMĚNĚ =====
        if output != last_output:

            history.append(output)

            if len(history) > 3:
                history.pop(0)

            final_output = "\n=== POSLEDNÍ 3 ZMĚNY ===\n"

            for item in reversed(history):
                final_output += item + "\n"

            # ===== ZÁPIS DO SOUBORU =====
            with open("/home/pi/hodnoty.txt", "w") as file:
                file.write(final_output)

            # ===== TERMINÁL =====
            print(final_output, flush=True)

            last_output = output

        time.sleep(0.2)

except KeyboardInterrupt:

    print("Program ukončen", flush=True)
    GPIO.cleanup()

except Exception as e:

    print("CHYBA:", e, flush=True)
    GPIO.cleanup()
