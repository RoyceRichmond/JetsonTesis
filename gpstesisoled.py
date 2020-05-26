# Simple GPS module demonstration. Will wait for a fix and print a message every second with the current location 
# and other details.}
#libraries for the OLED
import Adafruit_SSD1306   # This is the driver chip for the Adafruit PiOLED
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
#
import time
import board
import busio
import adafruit_gps
import serial
uart = serial.Serial("/dev/ttyTHS1", baudrate=9600, timeout=10)
# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
# gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Turn on just minimum info (RMC only, location):
# gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
# gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Tuen on everything (not all of it is parsed!)
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
# gps.send_command(b'PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing.  This would be twice a second (2hz, 500ms delay):
# gps.send_command(b'PMTK220,500')

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
counter=0
filename='logging.txt'



disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()



with open(filename,'w') as file_object:
    while counter<=50:     
    # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # 1.0 = 1 second; The divisor is the desired updates (frames) per second
    #time.sleep(1.0/4)        
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
        gps.update()
    # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:
                # Try again if we don't have a fix yet.
                print("Waiting for fix...")
                draw.text((x, top),"Waiting for fix...", font=font, fill=255)
                disp.image(image)
                disp.display()
                time.sleep(1.0/6)        
                continue
            # We have a fix! (gps.has_fix is true)
            # Print out details about the fix like location, date, etc.
            
            print("=" * 40)  # Print a separator line.
            
            print("Latitude: {0:.6f} degrees".format(gps.latitude))
            draw.text((x, top+6),"lat:{0:.6f}".format(gps.latitude), font=font, fill=255)#OLED PRINTING
            
            print("Longitude: {0:.6f} degrees".format(gps.longitude))
            draw.text((x, top+20),"lng:{0:.6f}".format(gps.longitude), font=font, fill=255)#OLED PRINTING
            
            texto="[{}]".format(counter)+"{0:.6f},".format(gps.latitude)+"{0:.6f},".format(gps.longitude)+"{0:.6f}\n".format(gps.altitude_m)
            print(texto)
            if gps.altitude_m is not None:
                print("Altitude: {} meters".format(gps.altitude_m))
                draw.text((x, top+30),"altitud:{}".format(gps.altitude_m), font=font, fill=255)#OLED PRINTING
            disp.image(image)
            disp.display()
            #time.sleep(1.0/6)   
            counter=counter+1
            file_object.write(texto)
file_object.close()
