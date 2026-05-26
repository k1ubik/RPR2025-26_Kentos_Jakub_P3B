print("=== START DEBUGU ===", flush=True)

try:
    import RPi.GPIO as GPIO
    import time
    import os

    print("Importy OK", flush=True)

    GPIO.setmode(GPIO.BCM)

    print("GPIO OK", flush=True)

    base_dir = '/sys/bus/w1/devices/'

    print("Kontrola DS18B20...", flush=True)

    found = False

    for item in os.listdir(base_dir):
        if item.startswith('28-'):
            device_file = base_dir + item + '/w1_slave'
            found = True

    if found:
        print("DS18B20 nalezen", flush=True)
        print(device_file, flush=True)

        file = open(device_file, 'r')
        text = file.read()
        file.close()

        print("Čtení teploty OK", flush=True)
        print(text, flush=True)

    else:
        print("DS18B20 nenalezen", flush=True)

    print("Test hodnoty.txt...", flush=True)

    with open("/home/pi/hodnoty.txt", "w") as file:
        file.write("DEBUG TEST")

    print("Soubor funguje", flush=True)

    print("=== DEBUG HOTOV ===", flush=True)

except Exception as e:
    print("CHYBA:", e, flush=True)
